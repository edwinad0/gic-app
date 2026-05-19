from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/home")

def layout():
    return dbc.Container(
        [
            html.H2("Welcome to the Skills & Task Intelligence Platform", className="mt-4"),

            html.P(
                "This platform was created to help our teams understand their work more clearly, "
                "identify opportunities for growth, and free up time for the tasks that matter most."
            ),
            html.P(
                "We believe technology should empower people, not replace them. We want to "
                "support your development, highlight your strengths, and help you focus "
                "on the work that truly matters."
            ),

            html.Hr(),

            html.H3("Why We Built This"),
            html.P([
                "Across the organisation, people spend a significant amount of time on repetitive, "
                "manual, or low‑value tasks. These tasks are important, but they often ",
                html.B("prevent us from focusing on strategic, creative, and people‑centred work."),
            ]),
            html.P(
                "This tool helps us analyse the tasks within each role, understand which ones could "
                "be automated or supported, and highlight the skills that matter for the future."
            ),

            html.Hr(),

            html.H3("How Does The Task Classifier Work?"),
            html.P(["The model has been trained on lots of real tasks, so when you give it a new one, it ",
                    html.B("recognises patterns "),
                    "in the wording and matches it to the category that most similar "
                    "tasks belonged to. It also gives a confidence score to show how sure it is about its choice.​"
            ]),
            html.P("Maintainers of the application can update the training data and retrain the model"),

            html.Hr(),

            html.Img(
                src="/assets/user-guide.png",
                style={
                    "width": "100%",
                    "maxWidth": "1600px",
                    "display": "block",
                    "margin": "30px auto",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.25)"
                }
            )
        ],
        fluid=True,
        className="p-4"
    )
