from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
from io import BytesIO
from pathlib import Path
import plotly.graph_objects as go

from src import (
    get_all_profiles,
    get_skills_for_person_id,
    get_weighted_skills_for_title,
    get_tasks_for_role,
    get_tasks_for_person_id,
)

from models.classifier import classify_task

register_page(__name__, path="/skills_map")

# Template paths
BASE = Path(__file__).parent.parent / "templates"
MAIN_TEMPLATE = BASE / "skills_report.html"
CAREER_TEMPLATE = BASE / "career_section.html"


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def compute_task_distribution(tasks):
    counts = {"Automatable": 0, "Augmentable": 0, "Human-Critical": 0}
    for t in tasks:
        label = classify_task(t)
        counts[label] += 1
    total = sum(counts.values()) or 1
    return {
        "Automatable": round(counts["Automatable"] / total * 100),
        "Augmentable": round(counts["Augmentable"] / total * 100),
        "Human-Critical": round(counts["Human-Critical"] / total * 100),
    }


def fig_to_base64(fig):
    buffer = BytesIO()
    fig.write_image(buffer, format="png")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


def render(component):
    """Recursively convert Dash component dicts into HTML strings."""
    if isinstance(component, str):
        return component

    if isinstance(component, list):
        return "".join(render(c) for c in component)

    if not isinstance(component, dict):
        return ""

    t = component.get("type")
    props = component.get("props", {})
    children = props.get("children", "")

    inner = render(children)

    tag_map = {
        "H1": "h1",
        "H2": "h2",
        "H3": "h3",
        "H4": "h4",
        "H5": "h5",
        "Ul": "ul",
        "Li": "li",
        "P": "p",
        "Br": "br",
        "Div": "div",
        "Img": "img",
        "Card": "div",
        "CardBody": "div",
    }

    tag = tag_map.get(t, "div")

    if tag == "br":
        return "<br>"

    if tag == "img":
        src = props.get("src", "")
        return f'<img src="{src}">'

    return f"<{tag}>{inner}</{tag}>"


# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------
def layout():
    profiles = get_all_profiles()
    titles = sorted({p[2].title() for p in profiles})

    return dbc.Container(
        [
            html.H2("Skills Map"),

            dbc.Button(
                "Generate PDF Report",
                id="generate_report_btn",
                color="primary",
                className="mb-3",
                disabled=True
            ),

            html.Div(id="pdf_report_container", style={"visibility": "hidden"}),
            html.Iframe(id="pdf_frame", style={"display": "none"}),
            html.Div(id="pdf_trigger", style={"display": "none"}),

            dcc.Store(id="radar_store"),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Task Radar"),
                            dcc.Graph(id="skills_radar"),
                        ],
                        width=4,
                    ),

                    dbc.Col(
                        [
                            html.H4("Skill Gap Analysis"),
                            dcc.Dropdown(
                                id="role_dropdown",
                                options=[{"label": t, "value": t} for t in titles],
                                placeholder="Select a job role...",
                                clearable=True,
                            ),
                            html.Br(),
                            dcc.Dropdown(
                                id="person_dropdown",
                                placeholder="Select a person...",
                                clearable=True,
                            ),
                            html.Br(),
                            html.Div(id="skill_gap_output"),
                        ],
                        width=4,
                    ),

                    dbc.Col(
                        [
                            html.H4("Career Progression"),
                            dcc.Dropdown(
                                id="target_role_dropdown",
                                placeholder="Select a target role...",
                                clearable=True,
                            ),
                            html.Br(),
                            html.Div(
                                id="career_progression_section",
                                children=[html.Div(id="career_gap_output")],
                                style={"display": "none"},
                            ),
                        ],
                        width=4,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


# ------------------------------------------------------------
# ENABLE PDF BUTTON
# ------------------------------------------------------------
@callback(
    Output("generate_report_btn", "disabled"),
    Input("role_dropdown", "value"),
    Input("person_dropdown", "value"),
)
def enable_report_button(role, person):
    return not (role and person)


# ------------------------------------------------------------
# BUILD PDF REPORT
# ------------------------------------------------------------
@callback(
    Output("pdf_report_container", "children"),
    Input("generate_report_btn", "n_clicks"),
    State("role_dropdown", "value"),
    State("person_dropdown", "value"),
    State("target_role_dropdown", "value"),
    State("skill_gap_output", "children"),
    State("career_gap_output", "children"),
    State("radar_store", "data"),
    prevent_initial_call=True
)
def build_report(n, role, person, target_role, skill_gap_html, career_gap_html, radar_fig_dict):

    profiles = get_all_profiles()
    person_name = next((p[1].title() for p in profiles if p[0] == person), str(person))

    # RADAR CHART
    radar_fig = go.Figure(radar_fig_dict)
    radar_img = fig_to_base64(radar_fig)

    # TASK CLASSIFICATION
    # Build task classification table
    tasks = get_tasks_for_person_id(person)
    task_table = """
    <table style='width:100%;border-collapse:collapse;font-size:14px;'>
        <tr style='background:#e9e9e9;'>
            <th style='border:1px solid #ccc;padding:8px;text-align:left;'>Task</th>
            <th style='border:1px solid #ccc;padding:8px;text-align:left;'>Classification</th>
        </tr>
    """

    for t in tasks:
        label = classify_task(t)
        task_table += f"""
        <tr>
            <td style='border:1px solid #ccc;padding:8px;'>{t}</td>
            <td style='border:1px solid #ccc;padding:8px;font-weight:bold;'>{label}</td>
        </tr>
        """

    task_table += "</table>"

    # CURRENT ROLE SKILLS
    sg_top10, _, sg_have, _, sg_need = skill_gap_html["props"]["children"]

    # CAREER PROGRESSION 
    if target_role and isinstance(career_gap_html, dict):
        cp_top10, _, cp_have, _, cp_need = career_gap_html["props"]["children"]
    else:
        cp_top10 = cp_have = cp_need = ""

    sg_top10_html = render(sg_top10)
    sg_have_html = render(sg_have)
    sg_need_html = render(sg_need)

    cp_top10_html = render(cp_top10) if cp_top10 else ""
    cp_have_html = render(cp_have) if cp_have else ""
    cp_need_html = render(cp_need) if cp_need else ""

    # Load main template
    with open(MAIN_TEMPLATE, "r") as f:
        template = f.read()

    # Load career section if needed
    if target_role:
        with open(CAREER_TEMPLATE, "r") as f:
            career_template = f.read()

        career_section = career_template.format(
            target_role=target_role,
            cp_top10=cp_top10_html,
            cp_have=cp_have_html,
            cp_need=cp_need_html
        )
    else:
        career_section = ""

    html_string = template.format(
        person_name=person_name,
        role=role,
        date=pd.Timestamp.now().strftime("%d %B %Y"),
        radar_img=radar_img,
        sg_top10=sg_top10_html,
        sg_have=sg_have_html,
        sg_need=sg_need_html,
        task_table=task_table,
        career_section=career_section
    )

    return html_string


# ------------------------------------------------------------
# RADAR CHART
# ------------------------------------------------------------
@callback(
    Output("skills_radar", "figure"),
    Output("radar_store", "data"),
    Input("role_dropdown", "value"),
    Input("person_dropdown", "value"),
)
def update_radar(title, person):
    if not title:
        df = pd.DataFrame({
            "Category": ["Automatable", "Augmentable", "Human-Critical"],
            "Score": [33, 33, 34],
        })
        fig = px.line_polar(df, r="Score", theta="Category", line_close=True)
        fig.update_traces(fill="toself")
        return fig, fig.to_dict()

    tasks = get_tasks_for_person_id(person) if person else get_tasks_for_role(title)
    dist = compute_task_distribution(tasks)

    df = pd.DataFrame({
        "Category": list(dist.keys()),
        "Score": list(dist.values()),
    })

    fig = px.line_polar(df, r="Score", theta="Category", line_close=True)
    fig.update_traces(fill="toself")

    return fig, fig.to_dict()


# ------------------------------------------------------------
# POPULATE PERSON DROPDOWN
# ------------------------------------------------------------
@callback(
    Output("person_dropdown", "options"),
    Input("role_dropdown", "value"),
)
def update_people(title):
    if not title:
        return []

    profiles = get_all_profiles()
    people = [
        {"label": p[1].title(), "value": p[0]}
        for p in profiles
        if p[2].title() == title
    ]
    return sorted(people, key=lambda x: x["label"])


# ------------------------------------------------------------
# POPULATE TARGET ROLE DROPDOWN
# ------------------------------------------------------------
@callback(
    Output("target_role_dropdown", "options"),
    Input("role_dropdown", "value"),
)
def populate_target_roles(current_role):
    profiles = get_all_profiles()
    titles = sorted({p[2].title() for p in profiles})
    return [{"label": t, "value": t} for t in titles if t != current_role]


# ------------------------------------------------------------
# SKILL GAP
# ------------------------------------------------------------
@callback(
    Output("skill_gap_output", "children"),
    Input("role_dropdown", "value"),
    Input("person_dropdown", "value"),
)
def show_skill_gap(title, person):
    if not title or not person:
        return ""

    person_skills = get_skills_for_person_id(person)
    weighted = get_weighted_skills_for_title(title)
    top10 = [s for s, count in weighted[:10]]
    missing = sorted(set(top10) - set(person_skills))

    return html.Div(
        [
            dbc.Card(dbc.CardBody([html.H5(f"Top 10 Skills for {title}"), html.Ul([html.Li(s) for s in top10])])),

            html.Br(),

            dbc.Card(dbc.CardBody([
                html.H5("Skills You Already Have"),
                html.Ul([html.Li(s) for s in person_skills]) if person_skills else "None yet."
            ])),

            html.Br(),

            dbc.Card(dbc.CardBody([
                html.H5("Skills You Should Consider Learning"),
                html.Ul([html.Li(s) for s in missing]) if missing else "You already have the top 10 skills!"
            ])),
        ]
    )


# ------------------------------------------------------------
# CAREER PROGRESSION
# ------------------------------------------------------------
@callback(
    Output("career_progression_section", "style"),
    Input("target_role_dropdown", "value"),
)
def toggle_career_section(target_role):
    return {"display": "block"} if target_role else {"display": "none"}


@callback(
    Output("career_gap_output", "children"),
    Input("role_dropdown", "value"),
    Input("person_dropdown", "value"),
    Input("target_role_dropdown", "value"),
)
def show_career_gap(current_role, person, target_role):
    if not current_role or not person or not target_role:
        return ""

    person_skills = get_skills_for_person_id(person)
    weighted = get_weighted_skills_for_title(target_role)
    top10 = [s for s, count in weighted[:10]]

    already_have = sorted(set(person_skills) & set(top10))
    missing = sorted(set(top10) - set(person_skills))

    return html.Div(
        [
            dbc.Card(dbc.CardBody([html.H5(f"Top 10 Skills for {target_role}"), html.Ul([html.Li(s) for s in top10])])),

            html.Br(),

            dbc.Card(dbc.CardBody([
                html.H5("Skills You Already Have"),
                html.Ul([html.Li(s) for s in already_have]) if already_have else "None yet."
            ])),

            html.Br(),

            dbc.Card(dbc.CardBody([
                html.H5("Skills You Need to Learn"),
                html.Ul([html.Li(s) for s in missing]) if missing else "You already have the top 10 skills!"
            ])),
        ]
    )
