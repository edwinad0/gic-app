from dash import Dash, html, dcc, page_container, callback, Input, Output
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.config.suppress_callback_exceptions = True

# Layout with navbar
app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Add Job Profile", href="/add_job_profile")),
            dbc.NavItem(dbc.NavLink("Manage Profiles", href="/manage_profiles")),
            dbc.NavItem(dbc.NavLink("Role Analysis", href="/role_analysis")),
            dbc.NavItem(dbc.NavLink("Skills Map", href="/skills_map")),
            dbc.NavItem(dbc.NavLink("FAQs", href="/questions")),
            dbc.NavItem(dbc.NavLink("Training Data", href="/training_data")),
        ],
        brand="GIC Team 27",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    page_container
])

# Redirect "/" → "/add_job_profile"
@callback(
    Output("url", "pathname"),
    Input("url", "pathname")
)
def redirect_home(path):
    if path in ("/", None):
        return "/add_job_profile"
    return path

if __name__ == "__main__":
    app.run(debug=True)
