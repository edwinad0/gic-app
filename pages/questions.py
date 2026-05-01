from dash import html, dcc, callback, Input, Output, State, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/questions")

# --- FAQ content ---
faq_items = [
    {
        "question": "What is this application used for?",
        "answer": "This applications ......"
    },
    {
        "question": "Where does the data come from?",
        "answer": "Data was collected through the quality team about job roles, tasks and employee skills."
    },
    {
        "question": "How do I retrain the model?",
        "answer": "Go to the Training Data page, add or edit samples, and click the 'Retrain Model' button."
    },
    {
        "question": "How can this help my career?",
        "answer": "The application allows you to visualise how to give yourself more time to complete important tasks, it also helps you to see what skills you should consider learning for career progression."
    },
]

accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            title=item["question"],
            children=html.P(item["answer"], className="mt-2")
        )
        for item in faq_items
    ],
    start_collapsed=True,
    flush=True,
)

layout = dbc.Container(
    [
        html.H2("FAQs", className="mt-4 mb-2"),
        html.P("Frequently Asked Questions about the app.", className="text-muted"),

        dbc.Card(
            dbc.CardBody([
                html.H4("Common Questions", className="mb-3"),
                accordion
            ]),
            className="shadow-sm"
        ),

        html.Div(style={"height": "40px"})  
    ],
    fluid=True
)
