from dash import Dash, html, dcc, page_container, callback, Input, Output
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"
    ],
)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id="url"),

    # Store the selected role (user / maintainer)
    dcc.Store(id="role_store", storage_type="session"),

    # -------------------------
    # SIDEBAR
    # -------------------------
    html.Div(
        id="sidebar",
        className="sidebar",
        style={"paddingTop": "20px"},
        children=[

            # Dynamic nav links
            html.Div(id="sidebar_links", className="sidebar-content"),

            # draggable handle
            html.Div(id="sidebar-handle", className="sidebar-handle"),

            # Role selector pinned to bottom
            html.Div(
                [
                    html.Hr(),
                    html.B("Role", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="user_role",
                        options=[
                            {"label": "Maintainer", "value": "maintainer"},
                            {"label": "User", "value": "user"},
                        ],
                        value="user",
                        clearable=False,
                        style={"marginBottom": "20px"}
                    )
                ],
                style={"position": "absolute", "bottom": "20px", "width": "90%"}
            )
        ]
    ),

    # -------------------------
    # MAIN CONTENT
    # -------------------------
    html.Div(
        id="main-content",
        className="main-content",
        children=[
            html.H1("Skills & Task Intelligence Platform", className="page-title"),
            html.Hr(),
            page_container,
            html.Div(id="pdf_trigger"),
            html.Iframe(id="pdf_frame", style={"display": "none"})
        ]
    ),
])


# -------------------------
# SIDEBAR CALLBACK
# -------------------------
@callback(
    Output("sidebar_links", "children"),
    Input("role_store", "data")
)
def update_sidebar(role):

    # Always visible
    common_links = [
        dbc.NavLink([
            html.I(className="bi bi-house me-2"),
            html.Span("Home", className="nav-text")
        ], href="/home", active="exact"),

        dbc.NavLink([
            html.I(className="bi bi-plus-circle me-2"),
            html.Span("Add Job Profile", className="nav-text")
        ], href="/add_job_profile", active="exact"),

        dbc.NavLink([
            html.I(className="bi bi-list-check me-2"),
            html.Span("Manage Profiles", className="nav-text")
        ], href="/manage_profiles", active="exact"),
    ]

    # User-only links 
    user_links = [
        dbc.NavLink([
            html.I(className="bi bi-graph-up me-2"),
            html.Span("Role Insights", className="nav-text")
        ], href="/role_analysis", active="exact"),

        dbc.NavLink([
            html.I(className="bi bi-bullseye me-2"),
            html.Span("Skill Overview", className="nav-text")
        ], href="/skills_map", active="exact"),

        dbc.NavLink([
            html.I(className="bi bi-question-circle me-2"),
            html.Span("Help Centre", className="nav-text")
        ], href="/questions", active="exact"),
    ]

    # Maintainer-only links
    maintainer_links = [
        dbc.NavLink([
            html.I(className="bi bi-book me-2"),
            html.Span("Maintainer Guide", className="nav-text")
        ], href="/maintainer_guide", active="exact"),

        dbc.NavLink([
            html.I(className="bi bi-database me-2"),
            html.Span("Classifier Model Training Data", className="nav-text")
        ], href="/training_data", active="exact"),

        dbc.NavLink([
            html.I(className="bi bi-database me-2"),
            html.Span("Extractor Model Training Data", className="nav-text")
        ], href="/extractor_training_data", active="exact"),
    ]

    if role == "maintainer":
        return dbc.Nav(common_links + maintainer_links, vertical=True, pills=True)
    
    if role == "user":
        return dbc.Nav(common_links + user_links, vertical=True, pills=True)

    return dbc.Nav(common_links, vertical=True, pills=True)


# -------------------------
# SYNC DROPDOWN → STORE
# -------------------------
@callback(
    Output("role_store", "data"),
    Input("user_role", "value")
)
def set_role(role):
    return role


# -------------------------
# Redirect "/" → "/home"
# -------------------------
@callback(
    Output("url", "pathname"),
    Input("url", "pathname")
)
def redirect_home(path):
    if path in ("/", None):
        return "/home"
    return path


# -------------------------
# PDF print callback
# -------------------------
app.clientside_callback(
    """
    function(html) {
        if (!html) return "";
        const frame = document.getElementById("pdf_frame");
        frame.srcdoc = html;
        frame.onload = function() {
            frame.contentWindow.print();
        };
        return "";
    }
    """,
    Output("pdf_trigger", "children"),
    Input("pdf_report_container", "children")
)


if __name__ == "__main__":
    app.run(debug=True)
