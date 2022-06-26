"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Mass Shooting Dashboard", className="display-4"),
        html.Hr(),
        html.P(
            "A compilation of Mass shootings within the USA in 2022", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("About", href="/page-1", active="exact"),
                dbc.NavLink("Learn More", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div(children=[
    dcc.Location(id="url"),
    sidebar,
    content
])

df = pd.read_csv("mass_shooting_2022_locations.csv")

df["Text"] = df["Incident Date"] + " " + df["Address"] + " " + df["City Or County"] + ", " + df["State"] \
             + " " + "Killed: " + df["# Killed"].astype(str) + " " + "Injured: " + df["# Injured"].astype(str)

fig = go.Figure(
    data=go.Scattergeo(
        lon=df["Longitude"],
        lat=df["Latitude"],
        text=df["Text"],
        mode="markers",
    )
)

fig.update_layout(
    geo_scope="usa",
    autosize=True,
    hovermode="closest",
    margin=dict(t=0, b=0, l=0, r=0)
)

about_page_1 = html.Div([
    html.H1("Why was this dashboard created?"),
    html.H3("This dashboard was created as a way of tracking gun violence within America as"
            " a result of the mounting gun violence within the country"),

    html.Hr(),

    html.H1("Where did this data come from?"),
    html.H3("The data for this dashboard was taken from the Gun Violence Archive (https://www.gunviolencearchive.org) "
            "more links and websites similar to the Gun Violence Archive can be found in the Learn More page"),

])

learn_more_page_2 = html.Div([
    html.H1("Gun Violence Archive"),
    html.H3("https://www.gunviolencearchive.org"),
    html.Hr(),
    html.H1("The Violence project"),
    html.H3("https://www.theviolenceproject.org"),
    html.Hr(),
    html.H1("Mass Shooting Tracker"),
    html.H3("https://massshootingtracker.site"),
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H2("USA Mass Shootings 2022"),
            dcc.Graph(
                id="mass_shooting_map",
                figure=fig
            ),
            html.Hr(),
            html.H2("330 US mass shootings in 2022"),
            html.H2("4712 mass shootings have occured in the US since 1/1/2013"),
        ])
    elif pathname == "/page-1":
        return about_page_1
    elif pathname == "/page-2":
        return learn_more_page_2
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    df.head()
    app.run_server()
