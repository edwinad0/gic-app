import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from src import (
    get_training_data,
    insert_training_sample,
    update_training_sample,
    delete_training_sample,
)

from models.classifier import TaskClassifier
classifier = TaskClassifier()

register_page(__name__, path="/training_data")


def layout():
    rows = get_training_data()

    return dbc.Container([
        html.H2("Training Data Manager"),
        html.P("Edit, add, or delete training samples used by the classifier."),

        dbc.Button("Retrain Model", id="td_retrain_btn", color="primary", className="mt-4"),
        html.Div(id="td_retrain_msg", className="mt-2"),

        # Add new sample
        dbc.Card([
            dbc.CardHeader("Add New Training Sample"),
            dbc.CardBody([
                dbc.Label("Task"),
                dbc.Textarea(id="td_new_task", style={"height": "80px"}),

                dbc.Label("Classification", className="mt-2"),
                dcc.Dropdown(
                    id="td_new_label",
                    options=[
                        {"label": "Automatable", "value": "Automatable"},
                        {"label": "Human-Critical", "value": "Human-Critical"},
                        {"label": "Augmentable", "value": "Augmentable"},
                    ],
                ),

                dbc.Button("Add Sample", id="td_add_btn", color="success", className="mt-3"),
                html.Div(id="td_add_msg", className="mt-2"),
            ])
        ], className="mb-4"),

        dbc.Card([
            dbc.CardHeader("Filter by Classification"),
            dbc.CardBody([
                dcc.Checklist(
                    id="td_filter_classes",
                    options=[
                        {"label": "Automatable", "value": "Automatable"},
                        {"label": "Human-Critical", "value": "Human-Critical"},
                        {"label": "Augmentable", "value": "Augmentable"},
                    ],
                    value=["Automatable", "Human-Critical", "Augmentable"], # default - show all 
                    inline=True,
                    inputStyle={"margin-right": "6px", "margin-left": "12px"},
                )
            ])
        ], className="mb-3"),

        # Table
        dash_table.DataTable(
            id="td_table",
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "Task", "id": "Task"},
                {"name": "Classification", "id": "Classification"},
                {"name": "Edit", "id": "edit"},
                {"name": "Delete", "id": "delete"},
            ],
            data=format_rows(rows),
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px"},
            style_header={"fontWeight": "bold"},
        ),

        html.Div(id="td_msg", className="mt-3"),

        # Edit modal
        dbc.Modal([
            dbc.ModalHeader("Edit Training Sample"),
            dbc.ModalBody([
                dbc.Label("Task"),
                dbc.Textarea(id="td_edit_task", style={"height": "80px"}),

                dbc.Label("Classification", className="mt-2"),
                dcc.Dropdown(
                    id="td_edit_label",
                    options=[
                        {"label": "Automatable", "value": "Automatable"},
                        {"label": "Human-Critical", "value": "Human-Critical"},
                        {"label": "Augmentable", "value": "Augmentable"},
                    ],
                ),

                dcc.Store(id="td_edit_id"),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="td_save_edit_btn", color="primary"),
                dbc.Button("Cancel", id="td_cancel_edit_btn", color="secondary"),
            ])
        ], id="td_edit_modal", is_open=False),
    ], fluid=True)


def format_rows(rows):
    return [
        {
            "id": r["id"],
            "Task": r["Task"],
            "Classification": r["Classification"],
            "edit": "✏️",
            "delete": "🗑️",
        }
        for r in rows
    ]


# FILTER 
@callback(
    Output("td_table", "data"),
    Input("td_filter_classes", "value"),
)
def filter_table(selected_classes):
    rows = get_training_data()

    if not selected_classes:
        # If user unticks everything, show nothing
        return []

    filtered = [r for r in rows if r["Classification"] in selected_classes]
    return format_rows(filtered)


# RETRAIN MODEL 
@callback(
    Output("td_retrain_msg", "children"),
    Input("td_retrain_btn", "n_clicks"),
    prevent_initial_call=True
)
def retrain_model_callback(n):
    try:
        classifier.train()
        return dbc.Alert("Model retrained successfully.", color="success")
    except Exception as e:
        return dbc.Alert(f"Error retraining model: {e}", color="danger")


# ADD TRAINING SAMPLE 
@callback(
    Output("td_add_msg", "children"),
    Output("td_table", "data", allow_duplicate=True),
    Input("td_add_btn", "n_clicks"),
    State("td_new_task", "value"),
    State("td_new_label", "value"),
    prevent_initial_call=True
)
def add_sample(n, task, label):
    if not task or not label:
        return dbc.Alert("Please enter both task and classification.", color="warning"), dash.no_update

    insert_training_sample(task, label)
    rows = get_training_data()
    classifier.train()

    return dbc.Alert("Sample added.", color="success"), format_rows(rows)


# EDIT TRAINING SAMPLE
@callback(
    Output("td_edit_modal", "is_open"),
    Output("td_edit_task", "value"),
    Output("td_edit_label", "value"),
    Output("td_edit_id", "data"),
    Input("td_table", "active_cell"),
    State("td_table", "data"),
    prevent_initial_call=True
)
def open_edit_modal(active_cell, table_data):
    if not active_cell or active_cell["column_id"] != "edit":
        raise PreventUpdate

    row = table_data[active_cell["row"]]

    return True, row["Task"], row["Classification"], row["id"]


# SAVE EDIT
@callback(
    Output("td_edit_modal", "is_open", allow_duplicate=True),
    Output("td_table", "data", allow_duplicate=True),
    Input("td_save_edit_btn", "n_clicks"),
    State("td_edit_id", "data"),
    State("td_edit_task", "value"),
    State("td_edit_label", "value"),
    prevent_initial_call=True
)
def save_edit(n, sample_id, task, label):
    update_training_sample(sample_id, task, label)
    rows = get_training_data()

    classifier.train()
    return False, format_rows(rows)


# DELETE ROW 
@callback(
    Output("td_table", "data", allow_duplicate=True),
    Output("td_msg", "children"),
    Input("td_table", "active_cell"),
    State("td_table", "data"),
    prevent_initial_call=True
)
def delete_row(active_cell, table_data):
    if not active_cell or active_cell["column_id"] != "delete":
        raise PreventUpdate

    row = table_data[active_cell["row"]]
    delete_training_sample(row["id"])

    rows = get_training_data()
    classifier.train()
    return format_rows(rows), dbc.Alert("Sample deleted.", color="info")
