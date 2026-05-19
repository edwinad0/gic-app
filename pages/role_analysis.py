from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc

from src import (
    get_all_profiles,
    get_tasks_for_role,
    get_weighted_skills_for_title,
    count_people_in_role
)

from models.classifier import TaskClassifier
classifier = TaskClassifier()


register_page(__name__, path="/role_analysis")


# ------------------------------------------------------------
# BADGES
# ------------------------------------------------------------ 
def confidence_badge(conf):
    """
    Colour code confidence Scores
    """
    color = (
        "success" if conf >= 0.80 else
        "warning" if conf >= 0.60 else
        "danger"
    )
    return dbc.Badge(f"{conf:.0%}", color=color, className="ms-2")


def classification_badge(label):
    """
    Colour code classification labels
    """
    colour = {
        "Automatable": "#064789",      
        "Augmentable": "#427aa1",      
        "Human-Critical": "#ffa69e",  
    }.get(label, "secondary")

    return dbc.Badge(label, color=colour, className="ms-2")



# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------
def layout():
    profiles = get_all_profiles()

    # Extract unique job titles
    options = sorted({p[2].title() for p in profiles})

    return dbc.Container([
        html.H2("Role Insights"),
        html.P("Select a job title to view top skills and task automation classification."),

        dcc.Dropdown(
            id="role_dropdown",
            options=[{"label": title, "value": title} for title in options],
            placeholder="Select a job role...",
            clearable=True
        ),

        html.Br(),

        html.Div(id="skills_output")
    ], fluid=True)


# ------------------------------------------------------------
# CALLBACK: SHOW SKILLS + TASK CLASSIFICATION
# ------------------------------------------------------------
@callback(
    Output("skills_output", "children"),
    Input("role_dropdown", "value")
)
def show_skills(title):
    if not title:
        return ""

    # Count people in this role
    num_people = count_people_in_role(title)

    # Weighted skills for this role
    weighted_skills = get_weighted_skills_for_title(title)

    if not weighted_skills:
        return dbc.Alert("No skills found for this role.", color="warning")

    # -----------------------------
    # TOP 5 SKILLS SECTION
    # -----------------------------
    top5 = weighted_skills[:5]  # already sorted in DB

    top5_list = html.Ul([
        html.Li(f"{skill}") for skill, weight in top5
    ])

    top5_card = dbc.Card(
        dbc.CardBody([
            html.H4("Top 5 Skills for This Role"),
            top5_list
        ])
    )

    # -----------------------------
    # TASK CLASSIFICATION SECTION
    # -----------------------------
    tasks = get_tasks_for_role(title)

    classified = []
    if not tasks:
        task_card = dbc.Alert("No tasks found for this role.", color="warning")
    else:
        classified = []
        for task in tasks:
            result = classifier.predict_with_confidence(task)
            classified.append((task, result["label"], result["confidence"]))

        task_rows = [
            html.Tr([
                html.Td(task),
                html.Td(classification_badge(label)),
                html.Td(confidence_badge(confidence))
            ])
            for task, label, confidence in classified
        ]

        task_table = dbc.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Task"),
                    html.Th("Classification"),
                    html.Th("Confidence Score (%)")
                ])),
                html.Tbody(task_rows)
            ],
            bordered=True,
            striped=True,
            hover=True
        )

        task_card = dbc.Card(
            dbc.CardBody([
                html.H4("Task Automation Classification"),
                task_table
            ])
        )

    # -----------------------------
    # TASK CLASSIFICATION PERCENTAGES
    # -----------------------------
    labels = [label for _, label, _ in classified]

    total = len(labels)
    auto = labels.count("Automatable")
    aug = labels.count("Augmentable")
    human = labels.count("Human-Critical")

    auto_pct = round((auto / total) * 100, 1) if total else 0
    aug_pct = round((aug / total) * 100, 1) if total else 0
    human_pct = round((human / total) * 100, 1) if total else 0

    percentage_bar = dbc.Card(
        dbc.CardBody([
            html.H4("Task Classification Breakdown"),

            html.Div([
                # Automatable
                html.Div(
                    style={
                        "width": f"{auto_pct}%",
                        "backgroundColor": "#064789",  
                        "height": "30px",
                        "display": "inline-block",
                        "textAlign": "center",
                        "color": "white",
                        "fontWeight": "bold",
                    },
                    children=f"{auto_pct}% Automatable" if auto_pct > 5 else ""
                ),

                # Assistive
                html.Div(
                    style={
                        "width": f"{aug_pct}%",
                        "backgroundColor": "#427aa1",  
                        "height": "30px",
                        "display": "inline-block",
                        "textAlign": "center",
                        "color": "black",
                        "fontWeight": "bold",
                    },
                    children=f"{aug_pct}% Augmentable" if aug_pct > 5 else ""
                ),

                # Human-Critical
                html.Div(
                    style={
                        "width": f"{human_pct}%",
                        "backgroundColor": "#ffa69e",  
                        "height": "30px",
                        "display": "inline-block",
                        "textAlign": "center",
                        "color": "white",
                        "fontWeight": "bold",
                    },
                    children=f"{human_pct}% Human-Critical" if human_pct > 5 else ""
                ),
            ], style={
                "width": "100%",
                "borderRadius": "5px",
                "overflow": "hidden",
                "display": "flex"
            })
        ])
    )

    # -----------------------------
    # RETURN PAGE CONTENT
    # -----------------------------
    return html.Div([
        html.H5(f"Currently {num_people} employee(s) in this role.", style={"color": "blue"}),
        html.Br(),
        top5_card,
        html.Br(),
        percentage_bar,
        html.Br(),
        task_card
    ])
