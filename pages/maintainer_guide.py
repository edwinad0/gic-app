from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/maintainer_guide")

layout = dbc.Container([
    html.H2("Maintainer Guide"),
    html.Hr(),

    html.P("""
        This guide explains how to update, maintain, and retrain the machine learning model 
        used in the Skills & Task Intelligence Platform.
    """),
    html.Div([
        html.H3("1. Task Classifier Model"),
        html.P("""
            This model classifies tasks into Automatable, Augmentable, or Human-Critical.
            It is trained using the data stored in the 'Classifier Model Training Data' page.
        """),

        html.H4("How to update the classifier training data"),
        html.Ul([
            html.Li("Go to the 'Classifier Model Training Data' page."),
            html.Li("Add, edit, or delete samples as needed."),
            html.Li("Each sample must include a task and its classification."),
        ]),

        html.H4("How to retrain the classifier model"),
        html.Ul([
            html.Li("Click the 'Retrain Model' button on the training data page."),
            html.Li("The system will rebuild the TF-IDF vectorizer and Logistic Regression model."),
            html.Li("The updated model is saved automatically to models/task_classifier.pkl."),
        ]),

        html.Hr(),

        # html.H3("2. Task Extractor Model"),
        # html.P("""
        #     This model identifies which sentences in a job description are actual tasks.
        #     It is trained using the data stored in the 'Extractor Model Training Data' page.
        # """),

        # html.H4("How to update the extractor training data"),
        # html.Ul([
        #     html.Li("Go to the 'Extractor Model Training Data' page."),
        #     html.Li("Add new sentences labelled as task (1) or not-task (0)."),
        #     html.Li("Edit or delete existing samples as needed."),
        # ]),

        # html.H4("How to retrain the extractor model"),
        # html.Ul([
        #     html.Li("Click the 'Retrain Extractor Model' button on the extractor training page."),
        #     html.Li("The system will rebuild the TF-IDF vectorizer and Logistic Regression model."),
        #     html.Li("The updated model is saved automatically to models/task_extractor.pkl."),
        # ]),

        # html.Hr(),

        html.H3("2. Best Practices"),
        html.Ul([
            html.Li("Keep training data balanced between classes."),
            html.Li("Add real-world examples regularly to improve accuracy."),
            html.Li("Avoid duplicate samples."),
            html.Li("Retrain models after any significant update to training data."),
            html.Li("Test extraction and classification after retraining."),
        ]),

        html.Hr(),

        html.H3("3. Troubleshooting"),
        html.Ul([
            html.Li("If extraction accuracy drops, add more negative examples."),
            html.Li("If classification becomes inconsistent, review ambiguous samples."),
            html.Li("If a model fails to load, retrain it from the training data page."),
        ]),

        html.P("This guide is only visible to maintainers."),
    ], style={"marginLeft": "25px"})
], fluid=True)
