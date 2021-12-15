from sqlite3.dbapi2 import Cursor
import dash
from dash.html.Label import Label
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import sqlite3


# DB connection---------------------------------------------------------------------------

conn = sqlite3.connect(
    'C:\Islam\AHS Productivity Team\Python-Dash-Data-visualization-tool\ProductionAnalisys.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM TrendData GROUP BY ShiftDate, Category, SubCategory1, SubCategory2, SubCategory3, SubCategory4 HAVING UpdateDate=MAX(UpdateDate)")

# ---------------------------------------------------------------------------
# Retrieve data from database-------------------

fig = go.Figure(
    data=[go.Scatter(x=["ShiftDate"], y=["Category"])])
trendplot = dcc.Graph(figure=fig)
# Retrieve data from database-------------------


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[

        dbc.Button("Sidebar", outline=True, color="secondary",
                   className="mr-1", id="btn_sidebar"),
        # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        # nav=True,
        # in_navbar=True,
        # label="More",
        # ),
    ],

    brand="Intagration Visualizing Tool",
    color="#3c8dbc",
    # dark=True,
    fluid=True,
)


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#222d32",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CARD_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

KPI = dbc.Card(
    dbc.CardBody(
        [

            html.P("This is tab 1!", className="card-text"),
            # dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)
WARNING = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            # dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Trend Plot", href="/page-1", id="page-1-link"),
                dbc.NavLink("Plot Archive", href="/page-2", id="page-2-link"),
                dbc.NavLink("Upload Data", href="/page-3", id="page-3-link"),
                dbc.NavLink("Report", href="/page-4", id="page-4-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)

kpicard = dbc.Card(
    dbc.Tabs(

        [

            dbc.Tab(trendplot, label="KPI"),
            dbc.Tab(WARNING, label="Warning Detection Stop"),



        ],


    ),
    style=CARD_STYLE
)
detailcard = dbc.Card(
    dbc.Tabs(
        [
            dbc.Tab(KPI, label="KPI"),
            dbc.Tab(WARNING, label="Warning Detection Stop")


        ]

    ),
    style=CARD_STYLE
)


app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
        kpicard,
        detailcard
    ],
)

# Toggling sidebar------------------------------------------------------------------


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

        return sidebar_style, content_style, cur_nclick
# Toggling sidebar------------------------------------------------------------------

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on


@ app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]


@ app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return html.P("This is the content of Trend Plot!")
    elif pathname == "/page-2":
        return html.P("This is the content of Plot archive!")
    elif pathname == "/page-3":
        return html.P("This is the content of Upload Data!")
    elif pathname == "/page-4":
        return html.P("This is the content of Report!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=8086)
