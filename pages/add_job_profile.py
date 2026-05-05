from dash import html, dcc, callback, Input, Output, State, register_page, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate

from db_helpers import insert_profile
from models.task_extractor import extract_tasks  


register_page(__name__, path="/add_job_profile")


# ------------------------------------------------------------
# UI COMPONENTS
# ------------------------------------------------------------

def task_pill(text):
    return dbc.Badge(
        [
            html.Div(text, style={"whiteSpace": "normal", "display": "inline"}),
            html.Span(
                " ✕",
                id={"type": "delete_task_add", "task": text},
                style={"cursor": "pointer", "marginLeft": "10px", "fontWeight": "bold"}
            )
        ],
        color="secondary",
        pill=True,
        className="me-1 mb-2 p-3",
        style={
            "fontSize": "14px",
            "backgroundColor": "#f0f0f0",
            "color": "#333",
            "border": "1px solid #ccc",
            "maxWidth": "100%",
            "whiteSpace": "normal",
        }
    )


def skill_pill(text):
    return dbc.Badge(
        [
            text,
            html.Span(
                " ✕",
                id={"type": "delete_skill_add", "skill": text},
                style={"cursor": "pointer", "marginLeft": "8px", "fontWeight": "bold"}
            )
        ],
        color="info",
        pill=True,
        className="me-1 mb-2"
    )


# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------

layout = dbc.Container([
    html.H2("Add Job Profile"),

    dbc.Label("Lead"),
    dbc.Input(id="add_lead", placeholder="Lead name", className="mb-2"),

    dbc.Label("Title"),
    dbc.Input(id="add_title", placeholder="Job title", className="mb-2"),

    dbc.Label("Grade"),
    dbc.Input(id="add_grade", placeholder="Grade", className="mb-2"),

    # dbc.Label("Description (optional)"),
    # dbc.Textarea(
    #     id="add_description",
    #     placeholder="Paste a job description here...",
    #     style={"height": "120px"},
    #     className="mb-2"
    # ),

    # dbc.Button("Generate Tasks", id="generate_tasks_btn", color="secondary", className="mb-3"),

    # ---------------- TASKS ----------------
    html.H5("Tasks"),
    dcc.Store(id="add_task_store", data=[]),

    dbc.Textarea(
        id="add_task_input",
        placeholder="Add a task and press Enter",
        style={"height": "80px"},
        className="mb-2"
    ),

    html.Div(id="add_task_list", className="mb-3"),

    # ---------------- SKILLS ----------------
    html.H5("Skills"),
    dcc.Store(id="add_skill_store", data=[]),

    dbc.Input(
        id="add_skill_input",
        placeholder="Add a skill and press Enter",
        className="mb-2"
    ),

    html.Div(id="add_skill_list", className="mb-3"),

    dbc.Button("Save Profile", id="save_profile_btn", color="success", className="mt-3"),

    html.Div(id="add_save_msg", className="mt-3"),
])


# ------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------

# --- AI Task Extraction ---
@callback(
    Output("add_task_store", "data", allow_duplicate=True),
    Output("add_task_input", "value", allow_duplicate=True),
    Input("generate_tasks_btn", "n_clicks"),
    State("add_description", "value"),
    prevent_initial_call=True
)
def generate_tasks(n, description):
    if not description:
        return [], ""

    tasks = extract_tasks(description)
    return tasks, ""


# --- Add/Delete Tasks ---
@callback(
    Output("add_task_store", "data", allow_duplicate=True),
    Output("add_task_input", "value", allow_duplicate=True),
    Input("add_task_input", "n_submit"),
    Input({"type": "delete_task_add", "task": ALL}, "n_clicks"),
    State("add_task_input", "value"),
    State("add_task_store", "data"),
    prevent_initial_call=True
)
def modify_tasks(add_submit, delete_clicks, new_task, tasks):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if "add_task_input" in trigger:
        if new_task and len(new_task.strip()) > 3:
            tasks.append(new_task.strip())
        return tasks, ""

    if "delete_task_add" in trigger:
        triggered_id = eval(trigger.split(".")[0])
        task_to_delete = triggered_id["task"]
        tasks = [t for t in tasks if t != task_to_delete]
        return tasks, ""

    raise PreventUpdate


# --- Display Tasks ---
@callback(
    Output("add_task_list", "children"),
    Input("add_task_store", "data")
)
def show_tasks(tasks):
    return [task_pill(t) for t in tasks]


# --- Add/Delete Skills ---
@callback(
    Output("add_skill_store", "data", allow_duplicate=True),
    Output("add_skill_input", "value"),
    Input("add_skill_input", "n_submit"),
    Input({"type": "delete_skill_add", "skill": ALL}, "n_clicks"),
    State("add_skill_input", "value"),
    State("add_skill_store", "data"),
    prevent_initial_call=True
)
def modify_skills(add_submit, delete_clicks, new_skill, skills):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if "add_skill_input" in trigger:
        if new_skill and len(new_skill.strip()) > 1:
            skills.append(new_skill.strip().title())
        return skills, ""

    if "delete_skill_add" in trigger:
        triggered_id = eval(trigger.split(".")[0])
        skill_to_delete = triggered_id["skill"]
        skills = [s for s in skills if s != skill_to_delete]
        return skills, ""

    raise PreventUpdate


# --- Display Skills ---
@callback(
    Output("add_skill_list", "children"),
    Input("add_skill_store", "data")
)
def show_skills(skills):
    return [skill_pill(s) for s in skills]


# --- Save Profile ---
@callback(
    Output("add_save_msg", "children"),
    Output("add_lead", "value"),
    Output("add_title", "value"),
    Output("add_grade", "value"),
    Output("add_description", "value"),
    Output("add_task_store", "data", allow_duplicate=True),
    Output("add_skill_store", "data", allow_duplicate=True),
    Input("save_profile_btn", "n_clicks"),
    State("add_lead", "value"),
    State("add_title", "value"),
    State("add_grade", "value"),          
    State("add_description", "value"),    
    State("add_task_store", "data"),
    State("add_skill_store", "data"),
    prevent_initial_call=True
)
def save_profile(n, lead, title, grade, description, tasks, skills):
    if not lead or not title or not tasks or not skills:
        return (
            dbc.Alert("Please fill out Lead, Title, Tasks, and Skills before saving.", color="danger"),
            lead,
            title,
            grade,
            description,
            tasks,
            skills
        )

    insert_profile(lead, title, grade, description, tasks, skills)

    return (
        dbc.Alert("Profile saved!", color="success"),
        "", "", "", "", [], []
    )
