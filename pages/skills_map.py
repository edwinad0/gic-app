from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from db_helpers import (
    get_all_profiles,
    get_skills_for_person_id,
    get_skills_for_title,
    get_weighted_skills_for_title,
    get_tasks_for_role,
    get_tasks_for_person_id,
)

from models.classifier import classify_task

register_page(__name__, path="/skills_map")


# ------------------------------------------------------------
# TASK DISTRIBUTION HELPER
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


# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------
def layout():
    profiles = get_all_profiles()
    titles = sorted({p[2].title() for p in profiles})

    return dbc.Container(
        [
            html.H2("Skills Map"),

            dbc.Row(
                [
                    # COLUMN 1 — TASK RADAR
                    dbc.Col(
                        [
                            html.H4("Task Radar"),
                            dcc.Graph(id="skills_radar"),
                        ],
                        width=4,
                    ),

                    # COLUMN 2 — CURRENT ROLE SKILL GAP
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

                    # COLUMN 3 — CAREER PROGRESSION
                    dbc.Col(
                        [
                            html.H4("Career Progression"),

                            dcc.Dropdown(
                                id="target_role_dropdown",
                                placeholder="Select a target role...",
                                clearable=True,
                            ),

                            html.Br(),

                            html.Div(id="career_gap_output"),
                        ],
                        width=4,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


# ------------------------------------------------------------
# TASK RADAR FOR ROLE OR PERSON
# ------------------------------------------------------------
@callback(
    Output("skills_radar", "figure"),
    Input("role_dropdown", "value"),
    Input("person_dropdown", "value"),
)
def update_radar(title, person):
    # Default radar
    if not title:
        df = pd.DataFrame(
            {
                "Category": ["Automatable", "Augmentable", "Human-Critical"],
                "Score": [33, 33, 34],
            }
        )
        fig = px.line_polar(df, r="Score", theta="Category", line_close=True)
        fig.update_traces(fill="toself")
        return fig

    # Person selected → use their tasks
    if person:
        tasks = get_tasks_for_person_id(person)
    else:
        tasks = get_tasks_for_role(title)

    dist = compute_task_distribution(tasks)

    df = pd.DataFrame(
        {
            "Category": list(dist.keys()),
            "Score": list(dist.values()),
        }
    )

    fig = px.line_polar(df, r="Score", theta="Category", line_close=True)
    fig.update_traces(fill="toself")
    return fig


# ------------------------------------------------------------
# POPULATE PERSON DROPDOWN WHEN ROLE SELECTED
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
        {"label": p[1].title(), "value": p[0]}   # label = name, value = ID
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

    return [
        {"label": t, "value": t}
        for t in titles
        if t != current_role
    ]


# ------------------------------------------------------------
# CURRENT ROLE SKILL GAP
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
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(f"Top 10 Skills for {title}"),
                        html.Ul([html.Li(s) for s in top10]),
                    ]
                )
            ),
            html.Br(),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Skills You Already Have"),
                        html.Ul([html.Li(s) for s in person_skills])
                        if person_skills
                        else "None yet.",
                    ]
                )
            ),
            html.Br(),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Skills You Should Consider Learning"),
                        html.Ul([html.Li(s) for s in missing])
                        if missing
                        else "You already have the top 10 skills!",
                    ]
                )
            ),
        ]
    )


# ------------------------------------------------------------
# CAREER PROGRESSION GAP
# ------------------------------------------------------------
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
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(f"Top 10 Skills for {target_role}"),
                        html.Ul([html.Li(s) for s in top10]),
                    ]
                )
            ),
            html.Br(),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Skills You Already Have"),
                        html.Ul([html.Li(s) for s in already_have])
                        if already_have
                        else "None yet.",
                    ]
                )
            ),
            html.Br(),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Skills You Need to Learn"),
                        html.Ul([html.Li(s) for s in missing])
                        if missing
                        else "You already have the top 10 skills!",
                    ]
                )
            ),
        ]
    )
