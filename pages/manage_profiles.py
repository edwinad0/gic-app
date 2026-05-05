import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, register_page, callback_context, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from db_helpers import get_name_for_person_id, get_all_profiles, delete_profile, get_job_profile, update_profile

register_page(__name__, path="/manage_profiles")


# ------------------------------------------------------------
# Helper: Task & Skill Pills
# ------------------------------------------------------------
def mp_task_pill(text):
    return dbc.Badge(
        [
            text,
            html.Span(" ✕", id={"type": "mp_delete_task", "task": text},
                      style={"cursor": "pointer", "marginLeft": "8px"})
        ],
        color="secondary", pill=True, className="me-1 mb-2"
    )


def mp_skill_pill(text):
    return dbc.Badge(
        [
            text,
            html.Span(" ✕", id={"type": "mp_delete_skill", "skill": text},
                      style={"cursor": "pointer", "marginLeft": "8px"})
        ],
        color="info", pill=True, className="me-1 mb-2"
    )


# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------
def layout():
    rows = get_all_profiles()

    leads = sorted({r[1] for r in rows})
    titles = sorted({r[2] for r in rows})

    return dbc.Container([

        html.H2("Manage Profiles"),
        html.P("Search, edit, or delete job profiles."),

        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="search_lead",
                    options=[{"label": l, "value": l} for l in leads],
                    placeholder="Filter by Lead",
                    clearable=True
                ),
                width=3
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="search_title",
                    options=[{"label": t, "value": t} for t in titles],
                    placeholder="Filter by Title",
                    clearable=True
                ),
                width=3
            ),
        ], className="mb-3"),

        dash_table.DataTable(
            id="manage_table",
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "Lead", "id": "lead"},
                {"name": "Title", "id": "title"},
                {"name": "Grade", "id": "grade"},
                {"name": "Created", "id": "created_at"},
                {"name": "Edit", "id": "edit"},
                {"name": "Delete", "id": "delete"},
            ],
            data=format_rows(rows),
            filter_action="none",
            page_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px"},
            style_cell_conditional=[
                {"if": {"column_id": "edit"}, "width": "40px", "textAlign": "center"},
                {"if": {"column_id": "delete"}, "width": "40px", "textAlign": "center"},
            ],
            style_header={"fontWeight": "bold"},
        ),

        html.Div(id="manage_msg", className="mt-3"),

        # ------------------------------------------------------------
        # EDIT MODAL
        # ------------------------------------------------------------
        dbc.Modal([
            dbc.ModalHeader("Edit Profile"),
            dbc.ModalBody([
                dbc.Label("Lead"),
                dbc.Input(id="mp_edit_lead", className="mb-2"),

                dbc.Label("Title"),
                dbc.Input(id="mp_edit_title", className="mb-2"),

                dbc.Label("Grade"),
                dbc.Input(id="mp_edit_grade", className="mb-2"),

                dbc.Label("Description"),
                dbc.Textarea(id="mp_edit_description", style={"height": "120px"}, className="mb-3"),

                html.H5("Tasks"),
                dcc.Store(id="mp_task_store", data=[]),
                dbc.Textarea(id="mp_task_input", placeholder="Add task and press Enter", className="mb-2"),
                html.Div(id="mp_task_list", className="mb-3"),

                html.H5("Skills"),
                dcc.Store(id="mp_skill_store", data=[]),
                dbc.Input(id="mp_skill_input", placeholder="Add skill and press Enter", className="mb-2"),
                html.Div(id="mp_skill_list", className="mb-3"),

                dcc.Store(id="mp_edit_id"),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="mp_save_btn", color="success"),
                dbc.Button("Cancel", id="mp_cancel_btn", color="secondary"),
            ])
        ], id="mp_edit_modal", is_open=False),

        # ------------------------------------------------------------
        # DELETE CONFIRMATION MODAL
        # ------------------------------------------------------------
        dbc.Modal([
            dbc.ModalHeader("Confirm Delete"),
            dbc.ModalBody(id="delete_confirm_body"),
            dbc.ModalFooter([
                dbc.Button("Delete", id="confirm_delete_btn", color="danger"),
                dbc.Button("Cancel", id="cancel_delete_btn", color="secondary"),
            ])
        ], id="delete_confirm_modal", is_open=False),

        # ------------------------------------------------------------
        # HIDDEN STORE FOR DELETE ID (your requested location)
        # ------------------------------------------------------------
        dcc.Store(id="delete_job_id"),

    ], fluid=True)


# ------------------------------------------------------------
# Format rows for the table
# ------------------------------------------------------------
def format_rows(rows):
    return [
        {
            "id": r[0],
            "lead": r[1],
            "title": r[2],
            "grade": r[3],
            "created_at": r[4],
            "edit": "✏️",
            "delete": "🗑️",
        }
        for r in rows
    ]


# ------------------------------------------------------------
# OPEN EDIT MODAL
# ------------------------------------------------------------
@callback(
    Output("mp_edit_modal", "is_open"),
    Output("mp_edit_lead", "value"),
    Output("mp_edit_title", "value"),
    Output("mp_edit_grade", "value"),
    Output("mp_edit_description", "value"),
    Output("mp_task_store", "data"),
    Output("mp_skill_store", "data"),
    Output("mp_edit_id", "data"),
    Input("manage_table", "active_cell"),
    State("manage_table", "data"),
    prevent_initial_call=True
)
def open_edit_modal(active_cell, table_data):
    if not active_cell:
        raise PreventUpdate

    if active_cell.get("column_id") != "edit":
        return (dash.no_update,) * 8

    row = table_data[active_cell["row"]]
    job_id = row["id"]

    profile = get_job_profile(job_id)

    return (
        True,
        profile["lead"],
        profile["title"],
        profile["grade"],
        profile["description"],
        profile["tasks"],
        profile["skills"],
        job_id
    )


# ------------------------------------------------------------
# FILTER TABLE
# ------------------------------------------------------------
@callback(
    Output("manage_table", "data"),
    Input("search_lead", "value"),
    Input("search_title", "value"),
)
def filter_table(lead_query, title_query):
    rows = get_all_profiles()
    formatted = format_rows(rows)

    lead_query = (lead_query or "").strip().lower()
    title_query = (title_query or "").strip().lower()

    filtered = []
    for row in formatted:
        if lead_query in row["lead"].lower() and title_query in row["title"].lower():
            filtered.append(row)

    return filtered


# ------------------------------------------------------------
# TASKS — ADD / DELETE
# ------------------------------------------------------------
@callback(
    Output("mp_task_store", "data", allow_duplicate=True),
    Output("mp_task_input", "value"),
    Input("mp_task_input", "n_submit"),
    Input({"type": "mp_delete_task", "task": ALL}, "n_clicks"),
    State("mp_task_input", "value"),
    State("mp_task_store", "data"),
    prevent_initial_call=True
)
def modify_tasks(add_submit, delete_clicks, new_task, tasks):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if "mp_task_input" in trigger:
        if new_task:
            tasks.append(new_task.strip())
        return tasks, ""

    if "mp_delete_task" in trigger:
        triggered_id = eval(trigger.split(".")[0])
        task_to_delete = triggered_id["task"]
        tasks = [t for t in tasks if t != task_to_delete]
        return tasks, ""

    raise PreventUpdate


@callback(
    Output("mp_task_list", "children"),
    Input("mp_task_store", "data")
)
def show_tasks(tasks):
    if not tasks:
        return []
    return [mp_task_pill(t) for t in tasks]


# ------------------------------------------------------------
# SKILLS — ADD / DELETE
# ------------------------------------------------------------
@callback(
    Output("mp_skill_store", "data", allow_duplicate=True),
    Output("mp_skill_input", "value"),
    Input("mp_skill_input", "n_submit"),
    Input({"type": "mp_delete_skill", "skill": ALL}, "n_clicks"),
    State("mp_skill_input", "value"),
    State("mp_skill_store", "data"),
    prevent_initial_call=True
)
def modify_skills(add_submit, delete_clicks, new_skill, skills):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if "mp_skill_input" in trigger:
        if new_skill:
            skills.append(new_skill.strip().title())
        return skills, ""

    if "mp_delete_skill" in trigger:
        triggered_id = eval(trigger.split(".")[0])
        skill_to_delete = triggered_id["skill"]
        skills = [s for s in skills if s != skill_to_delete]
        return skills, ""

    raise PreventUpdate


@callback(
    Output("mp_skill_list", "children"),
    Input("mp_skill_store", "data")
)
def show_skills(skills):
    if not skills:
        return []
    return [mp_skill_pill(s) for s in skills]


# ------------------------------------------------------------
# SAVE CHANGES
# ------------------------------------------------------------
@callback(
    Output("mp_edit_modal", "is_open", allow_duplicate=True),
    Output("manage_table", "data", allow_duplicate=True),
    Output("manage_msg", "children"),
    Input("mp_save_btn", "n_clicks"),
    State("mp_edit_id", "data"),
    State("mp_edit_lead", "value"),
    State("mp_edit_title", "value"),
    State("mp_edit_grade", "value"),
    State("mp_edit_description", "value"),
    State("mp_task_store", "data"),
    State("mp_skill_store", "data"),
    prevent_initial_call=True
)
def save_profile(n, job_id, lead, title, grade, description, tasks, skills):
    update_profile(job_id, lead, title, grade, description, tasks, skills)
    rows = get_all_profiles()

    return (
        False,
        format_rows(rows),
        dbc.Alert("Profile updated successfully!", color="success")
    )


# ------------------------------------------------------------
# DELETE — OPEN CONFIRMATION MODAL
# ------------------------------------------------------------
@callback(
    Output("delete_confirm_modal", "is_open"),
    Output("delete_confirm_body", "children"),
    Output("mp_edit_modal", "is_open", allow_duplicate=True),
    Output("delete_job_id", "data"),
    Input("manage_table", "active_cell"),
    State("manage_table", "data"),
    prevent_initial_call=True
)
def ask_delete_confirmation(active_cell, table_data):
    if not active_cell:
        raise PreventUpdate

    if active_cell.get("column_id") != "delete":
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    row = table_data[active_cell["row"]]
    job_id = row["id"]
    lead = row["lead"]
    title = row["title"]

    return (
        True,
        dcc.Markdown(f"Are you sure you want to delete profile for **{lead}** — **{title}**?"),
        False,
        job_id
    )


# ------------------------------------------------------------
# CANCEL DELETE
# ------------------------------------------------------------
@callback(
    Output("delete_confirm_modal", "is_open", allow_duplicate=True),
    Input("cancel_delete_btn", "n_clicks"),
    prevent_initial_call=True
)
def cancel_delete(n):
    return False


# ------------------------------------------------------------
# CONFIRM DELETE
# ------------------------------------------------------------
@callback(
    Output("delete_confirm_modal", "is_open", allow_duplicate=True),
    Output("manage_table", "data", allow_duplicate=True),
    Output("manage_msg", "children", allow_duplicate=True),
    Input("confirm_delete_btn", "n_clicks"),
    State("delete_job_id", "data"),
    prevent_initial_call=True
)
def confirm_delete(n, job_id):
    if not n:
        raise PreventUpdate

    job_id = int(job_id)
    name = get_name_for_person_id(job_id)
    delete_profile(job_id)
    rows = get_all_profiles()

    return (
        False,
        format_rows(rows),
        dbc.Alert(f"Deleted profile {job_id} - {name}", color="success")
    )


# ------------------------------------------------------------
# CLOSE EDIT MODAL
# ------------------------------------------------------------
@callback(
    Output("mp_edit_modal", "is_open", allow_duplicate=True),
    Input("mp_cancel_btn", "n_clicks"),
    prevent_initial_call=True
)
def close_edit_modal(n):
    return False
