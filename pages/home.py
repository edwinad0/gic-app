from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/home")

def layout():
    return dbc.Container(
        [
            html.H1("Welcome to the Skills & Task Intelligence Platform", className="mt-4"),

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

            html.H2("Why We Built This"),
            html.P([
                "Across the organisation, people spend a significant amount of time on repetitive, "
                "manual, or low‑value tasks. These tasks are important, but they often ",
                html.B("prevent us from focusing on strategic, creative, and people‑centred work."),
            ]),
            html.P(
                "This tool helps us analyse the tasks within each role, understand which ones could "
                "be automated or supported, and highlight the skills that matter for the future."
            ),
            dbc.Alert(
                "This platform is NOT designed to replace jobs. Its purpose is to support people, "
                "reduce unnecessary workload, and create more time for meaningful, high‑impact work.",
                color="info",
                className="mt-3"
            ),

            html.Hr(),

            html.H2("How to Use the App"),

            html.H4("Explore Your Role"),
            html.P([
                "Go to the Role Analysis Page and select your job role. You’ll see the top skills for "
                "your role.",
                html.Br(),
                "Here you can also see how tasks for your role are classified by our model."
            ]),

            html.H4("Generate a Skills Map"),
            html.P([
                "From the Skills Map Page choose your name from the list to view your ",
                html.B("personalised "),
                "task radar, skill gap analysis, and task classification summary."
            ]),

            html.H4("Explore Career Progression"),
            html.P(
                "Choose a target role to see which skills you already have and which ones you may "
                "want to develop for future opportunities."
            ),

            html.H4("Generate Your PDF Report"),
            html.P(
                "Once your role and name are selected, you can generate a full PDF report including "
                "your task distribution, skill gaps, and career progression insights."
            ),
        ],
        fluid=True,
        className="p-4"
    )
