from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/questions")

# --- FAQ content ---
faq_items = [
    {
        "question": "What is this application used for?",
        "answer": (
            "This application helps you understand the tasks and skills required for your role, "
            "identify which tasks could be automated or supported, and highlight the skills that "
            "matter most for your development. It gives you a clear picture of where your time goes "
            "and how you can focus more on high‑value work."
        )
    },
    {
        "question": "Why was this application created?",
        "answer": (
            "The platform was built to give employees clarity, confidence, and control over their work. "
            "It helps teams reduce low‑value tasks, supports fair and consistent role expectations, and "
            "provides a transparent view of the skills needed for progression. It also helps leaders make "
            "better decisions about training, automation, and workforce planning."
        )
    },
    {
        "question": "Where does the data come from?",
        "answer": (
            "The data comes from the Quality team’s analysis of job roles, tasks, and employee skills. "
            "This includes real descriptions, responsibilities, and skill requirements gathered across the organisation."
        )
    },
    {
        "question": "How can this help my career?",
        "answer": (
            "The application shows you which skills are most important for your current role and which skills "
            "you may want to develop for future roles. It highlights your strengths, identifies gaps, and helps "
            "you plan your progression. It also shows how automation could free up time for more meaningful work."
        )
    },
    {
        "question": "How accurate are the task and skill insights?",
        "answer": (
            "The insights are generated using machine learning models trained on real role data. "
            "They improve over time as more examples are added and the models are retrained. "
            "They are designed to support conversations, not replace human judgement."
        )
    },
    {
        "question": "Can I update or correct the data?",
        "answer": (
            "Yes. You can update tasks and skills when adding or editing a job profile. "
            "Maintainers can also update the underlying training data to improve the models."
        )
    },
    {
        "question": "How do I retrain the models?",
        "answer": (
            "Only a Maintainer can retrain the models. They can do this from the Training Data pages "
            "using the 'Retrain Model' buttons."
        )
    },
    {
        "question": "Who can access the training data?",
        "answer": (
            "Only Maintainers can view or edit the training data used to improve the models. "
            "Regular users will not see these pages."
        )
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
        html.H2("Help Centre", className="mt-4 mb-2"),

        html.Br(),

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
