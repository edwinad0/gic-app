import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd

from models.task_extractor import TaskExtractor

register_page(__name__, path="/extractor_training_data")

CSV_PATH = "models/task_training_data.csv"


def load_csv():
    return pd.read_csv(CSV_PATH).to_dict("records")


def save_csv(rows):
    df = pd.DataFrame(rows)
    df.to_csv(CSV_PATH, index=False)


def layout():
    rows = load_csv()

    return dbc.Container([
        html.H2("Task Extractor Training Data"),
        html.P("Edit, add, or delete samples used to train the task extractor."),

        dbc.Button("Retrain Extractor Model", id="etd_retrain_btn", color="primary", className="mt-4"),
        html.Div(id="etd_retrain_msg", className="mt-2"),

        # Add new sample
        dbc.Card([
            dbc.CardHeader("Add New Sample"),
            dbc.CardBody([
                dbc.Label("Sentence"),
                dbc.Textarea(id="etd_new_sentence", style={"height": "80px"}),

                dbc.Label("Is Task?", className="mt-2"),
                dcc.Dropdown(
                    id="etd_new_label",
                    options=[
                        {"label": "Task (1)", "value": 1},
                        {"label": "Not Task (0)", "value": 0},
                    ],
                ),

                dbc.Button("Add Sample", id="etd_add_btn", color="success", className="mt-3"),
                html.Div(id="etd_add_msg", className="mt-2"),
            ])
        ], className="mb-4"),

        # Table
        dash_table.DataTable(
            id="etd_table",
            columns=[
                {"name": "Sentence", "id": "sentence"},
                {"name": "Is Task", "id": "is_task"},
                {"name": "Edit", "id": "edit"},
                {"name": "Delete", "id": "delete"},
            ],
            data=format_rows(rows),
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px"},
            style_header={"fontWeight": "bold"},
        ),

        html.Div(id="etd_msg", className="mt-3"),

        # Edit modal
        dbc.Modal([
            dbc.ModalHeader("Edit Sample"),
            dbc.ModalBody([
                dbc.Label("Sentence"),
                dbc.Textarea(id="etd_edit_sentence", style={"height": "80px"}),

                dbc.Label("Is Task?", className="mt-2"),
                dcc.Dropdown(
                    id="etd_edit_label",
                    options=[
                        {"label": "Task (1)", "value": 1},
                        {"label": "Not Task (0)", "value": 0},
                    ],
                ),

                dcc.Store(id="etd_edit_index"),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="etd_save_edit_btn", color="primary"),
                dbc.Button("Cancel", id="etd_cancel_edit_btn", color="secondary"),
            ])
        ], id="etd_edit_modal", is_open=False),
    ], fluid=True)


def format_rows(rows):
    return [
        {
            "sentence": r["sentence"],
            "is_task": r["is_task"],
            "edit": "✏️",
            "delete": "🗑️",
        }
        for r in rows
    ]


# RETRAIN MODEL
@callback(
    Output("etd_retrain_msg", "children"),
    Input("etd_retrain_btn", "n_clicks"),
    prevent_initial_call=True
)
def retrain_model_callback(n):
    try:
        TaskExtractor().train()
        return dbc.Alert("Extractor model retrained successfully.", color="success")
    except Exception as e:
        return dbc.Alert(f"Error retraining model: {e}", color="danger")


# ADD SAMPLE
@callback(
    Output("etd_add_msg", "children"),
    Output("etd_table", "data", allow_duplicate=True),
    Input("etd_add_btn", "n_clicks"),
    State("etd_new_sentence", "value"),
    State("etd_new_label", "value"),
    prevent_initial_call=True
)
def add_sample(n, sentence, label):
    if not sentence or label is None:
        return dbc.Alert("Please enter both sentence and label.", color="warning"), dash.no_update

    rows = load_csv()
    rows.append({"sentence": sentence, "is_task": label})
    save_csv(rows)

    return dbc.Alert("Sample added.", color="success"), format_rows(rows)


# OPEN EDIT MODAL
@callback(
    Output("etd_edit_modal", "is_open"),
    Output("etd_edit_sentence", "value"),
    Output("etd_edit_label", "value"),
    Output("etd_edit_index", "data"),
    Input("etd_table", "active_cell"),
    State("etd_table", "data"),
    prevent_initial_call=True
)
def open_edit_modal(active_cell, table_data):
    if not active_cell or active_cell["column_id"] != "edit":
        raise PreventUpdate

    row = table_data[active_cell["row"]]
    return True, row["sentence"], row["is_task"], active_cell["row"]


# SAVE EDIT
@callback(
    Output("etd_edit_modal", "is_open", allow_duplicate=True),
    Output("etd_table", "data", allow_duplicate=True),
    Input("etd_save_edit_btn", "n_clicks"),
    State("etd_edit_index", "data"),
    State("etd_edit_sentence", "value"),
    State("etd_edit_label", "value"),
    prevent_initial_call=True
)
def save_edit(n, index, sentence, label):
    rows = load_csv()
    rows[index] = {"sentence": sentence, "is_task": label}
    save_csv(rows)

    return False, format_rows(rows)


# DELETE ROW
@callback(
    Output("etd_table", "data", allow_duplicate=True),
    Output("etd_msg", "children"),
    Input("etd_table", "active_cell"),
    State("etd_table", "data"),
    prevent_initial_call=True
)
def delete_row(active_cell, table_data):
    if not active_cell or active_cell["column_id"] != "delete":
        raise PreventUpdate

    index = active_cell["row"]
    rows = load_csv()
    rows.pop(index)
    save_csv(rows)

    return format_rows(rows), dbc.Alert("Sample deleted.", color="info")
