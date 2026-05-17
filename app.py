import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages import overview, geography, content


# --- App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "18rem", "padding": "2rem 1rem", "background-color": "#111", "color": "white"
}

CONTENT_STYLE = {
    "margin-left": "20rem", "margin-right": "2rem", "padding": "2rem 1rem",
}

sidebar = html.Div([
    html.H2("Netflix", className="display-4", style={'color': '#E50914', 'fontWeight': 'bold'}),
    html.Hr(style={'border-top': '1px solid white'}),
    dbc.Nav([
        dbc.NavLink("Ընդհանուր", href="/", active="exact", style={"color": "gray"}),
        dbc.NavLink("Աշխարհագրություն", href="/geography", active="exact", style={"color": "gray"}),
        dbc.NavLink("Ժանրեր և Տևողություն", href="/content", active="exact", style={"color": "gray"}),
    ], vertical=True),
], style=SIDEBAR_STYLE)

page_container = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url", refresh=False), sidebar, page_container])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    print(f"Loading page: {pathname}")
    if pathname == "/geography": return geography.layout
    elif pathname == "/content": return content.layout
    else: return overview.layout


# --- Run App ---
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8070, dev_tools_hot_reload=False)
