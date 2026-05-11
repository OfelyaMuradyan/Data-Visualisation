import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objs as go

file_path = 'netflix_titles.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    print("Warning: netflix_titles.csv not found locally.")
    df = pd.DataFrame(columns=['type', 'country', 'date_added', 'release_year', 'rating', 'duration', 'listed_in'])

df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df = df.dropna(subset=['year_added']) 
df['country'] = df['country'].fillna('Unknown')

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

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url", refresh=False), sidebar, content])

# Page 1: Overview
def overview_layout():
    return html.Div([
        html.H1("Netflix-ի content-ի ընդհանուր տեսքը", className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Ընդհանուր քանակ"), dbc.CardBody([html.H2(len(df))])], color="danger", inverse=True), width=4),
            dbc.Col(dbc.Card([dbc.CardHeader("Movies"), dbc.CardBody([html.H2(len(df[df['type']=='Movie']))])], color="dark", inverse=True), width=4),
            dbc.Col(dbc.Card([dbc.CardHeader("TV Shows"), dbc.CardBody([html.H2(len(df[df['type']=='TV Show']))])], color="secondary", inverse=True), width=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Բովանդակության աճը (Slide to filter)"),
                    dcc.RangeSlider(
                        id='year-slider', min=int(df['year_added'].min()), max=int(df['year_added'].max()),
                        value=[df['year_added'].min(), df['year_added'].max()],
                        marks={int(i): str(int(i)) for i in range(int(df['year_added'].min()), int(df['year_added'].max())+1, 4)},
                        step=1, className="mb-4"
                    ),
                    dcc.Graph(id='growth-chart')
                ])
            ]), width=8),
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("Տեսակներ"), dcc.Graph(id='pie-chart')])]), width=4),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Ժանրերի հիերարխիա (Treemap)"),
                    dcc.Graph(id='treemap-chart')
                ])
            ]), width=12)
        ])
    ])

# Page 2: Geography
def geography_layout():
    return html.Div([
        html.H1("Աշխարհագրական վերլուծություն", className="mb-4"),
        dbc.Card([
            dbc.CardBody([
                html.Label("Ընտրեք տեսակը՝ քարտեզը թարմացնելու համար"),
                dbc.RadioItems(
                    id="geo-filter",
                    options=[
                        {"label": "Բոլորը", "value": "All"},
                        {"label": "Movie", "value": "Movie"},
                        {"label": "TV Show", "value": "TV Show"}
                    ],
                    value="All",  # Սա ապահովում է, որ քարտեզը բեռնվի հենց սկզբից
                    inline=True,
                    persistence=True,
                    persistence_type='session',
                    className="mb-3"
                ),
                # dcc.Graph(id="map-plot"), # Հիմնական քարտեզը
            ])
        ]),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Թոփ 10 երկրներ"),
                    dcc.Graph(id="top-countries-bar")
                ])
            ]), width=5),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Գլոբալ տարածման դինամիկան"),
                    dcc.Graph(id="animated-map")
                ])
            ]), width=7),

                # dcc.Loading-ը ցույց է տալիս, որ սերվերը աշխատում է
                dcc.Loading(
                    id="loading-map",
                    type="dot",
                    children=dcc.Graph(id="map-plot")
                )
            ])
        ])

# Page 3: Content
def content_layout():
    return html.Div([
        html.H1("Ժանրերի և Վարկանիշների վերլուծություն", className="mb-4"),
        dbc.Card([
            dbc.CardBody([
                html.Label("Ընտրեք ժանրը՝ մանրամասն տեսնելու համար:"),
                dcc.Dropdown(
                    id="genre-drop",
                    options=[{'label': g, 'value': g} for g in sorted(df['listed_in'].str.split(', ').explode().unique()) if g],
                    value='Dramas', clearable=False, className="mb-4"
                ),
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id="duration-hist"), width=6),
            dbc.Col(dcc.Graph(id="rating-sunburst"), width=6)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([dcc.Graph(id="rating-comparison-bar")])]), width=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([dcc.Graph(id="genre-duration-box")])]), width=6),
            dbc.Col(dbc.Card([dbc.CardBody([dcc.Graph(id="tv-seasons-avg")])]), width=6),
        ])
    ])

# --- Callbacks ---

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    print(f"Loading page: {pathname}")
    if pathname == "/geography": return geography_layout()
    elif pathname == "/content": return content_layout()
    else: return overview_layout()

@app.callback(
    [Output('growth-chart', 'figure'), 
     Output('pie-chart', 'figure'),
     Output('treemap-chart', 'figure')], 
    [Input('year-slider', 'value')]
)
def update_overview(years):
    dff = df[(df['year_added'] >= years[0]) & (df['year_added'] <= years[1])]
    growth = dff.groupby(['year_added', 'type']).size().reset_index(name='count')
    fig_growth = px.area(growth, x='year_added', y='count', color='type', 
                         color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'}, template="plotly_white")
    fig_pie = px.pie(dff, names='type', hole=0.4, color_discrete_sequence=['#E50914', '#221F1F'])
    
    genres_df = dff.assign(listed_in=dff['listed_in'].str.split(', ')).explode('listed_in')
    
    fig_treemap = px.treemap(
        genres_df, 
        path=[px.Constant("Netflix"), 'type', 'listed_in'], 
        color_discrete_sequence=['#E50914', '#221F1F'],
        template="plotly_white"
    )
    fig_treemap.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig_growth, fig_pie, fig_treemap

@app.callback(
    [Output("map-plot", "figure"),
     Output("top-countries-bar", "figure"),
     Output("animated-map", "figure")],
    [Input("geo-filter", "value")]
)
def update_map(val):
    if df is None or df.empty:
        return px.choropleth(title="Տվյալներ չկան")

    dff = df if val == 'All' else df[df['type'] == val]
    
    df_anim = dff.assign(country=dff['country'].str.split(', ')).explode('country')
    df_anim = df_anim.groupby(['year_added', 'country']).size().reset_index(name='count')
    
    fig_anim = px.choropleth(
        df_anim, locations="country", locationmode='country names',
        color="count", animation_frame="year_added",
        color_continuous_scale="Reds", title="Netflix-ի տարածման դինամիկան"
    )

    s = dff['country'].dropna().astype(str).str.split(', ').explode().str.strip()
    counts = s.value_counts().reset_index()
    counts.columns = ['country', 'count']
    
    fig_static = px.choropleth(
        counts, locations="country", locationmode='country names',
        color="count", color_continuous_scale="Reds", title="Ընդհանուր տարածվածություն"
    )

    top_10 = counts.head(10)
    fig_bar = px.bar(
        top_10, x='count', y='country', orientation='h',
        color='count', color_continuous_scale='Reds', title="Թոփ 10 երկրներ"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})

    return fig_anim, fig_static, fig_bar


@app.callback(
    [Output("duration-hist", "figure"), 
     Output("rating-sunburst", "figure"),
     Output("rating-comparison-bar", "figure"),
     Output("genre-duration-box", "figure"),
     Output("tv-seasons-avg", "figure")],
    [Input("genre-drop", "value")]
)
def update_content(genre):
    if not genre:
        empty_fig = go.Figure().update_layout(title="Խնդրում ենք ընտրել ժանր")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    dff = df[df['listed_in'].str.contains(genre, na=False)].copy()
    
    if dff.empty:
        empty_fig = go.Figure().update_layout(title="Տվյալներ չկան")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    dff_sun = dff.dropna(subset=['rating', 'type'])
    if not dff_sun.empty:
        fig_sun = px.sunburst(dff_sun, path=['type', 'rating'], color='type',
                              color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'},
                              title=f"Հիերարխիա: {genre}")
    else:
        fig_sun = go.Figure().update_layout(title="Rating-ներ չկան")

    movies_genre = dff[dff['type'] == 'Movie'].copy()
    if not movies_genre.empty:
        movies_genre['duration_min'] = movies_genre['duration'].str.extract('(\d+)').astype(float)
        fig_hist = px.histogram(movies_genre, x="duration_min", title=f"Ֆիլմերի տևողություն ({genre})",
                                color_discrete_sequence=['#E50914'], template="plotly_white")
    else:
        fig_hist = go.Figure().update_layout(title="Այս ժանրում ֆիլմեր չկան", template="plotly_white")

    rating_cnt = dff.groupby(['rating', 'type']).size().unstack(fill_value=0)
    
    movie_y = rating_cnt['Movie'] if 'Movie' in rating_cnt.columns else []
    tv_y = rating_cnt['TV Show'] if 'TV Show' in rating_cnt.columns else []
    
    fig_rating_bar = go.Figure(data=[
        go.Bar(name='Movies', x=rating_cnt.index, y=movie_y, marker_color='#E50914'),
        go.Bar(name='TV Shows', x=rating_cnt.index, y=tv_y, marker_color='#221F1F')
    ])
    fig_rating_bar.update_layout(barmode='group', title="Rating-ների համեմատություն", template="plotly_white")

    if not movies_genre.empty:
        fig_box = px.box(movies_genre, x="rating", y="duration_min", color="rating",
                         title="Տևողության տարբերությունն ըստ Rating-ի", template="plotly_white")
    else:
        fig_box = go.Figure().update_layout(title="Ֆիլմեր չկան", template="plotly_white")

    tv_genre = dff[dff['type'] == 'TV Show'].copy()
    if not tv_genre.empty:
        tv_genre['seasons'] = tv_genre['duration'].str.extract('(\d+)').astype(float)
        avg_seasons = tv_genre.groupby('rating')['seasons'].mean().reset_index()
        fig_tv_bar = px.bar(avg_seasons, x='rating', y='seasons', text='seasons',
                            title="Սեզոնների միջին քանակը", color_discrete_sequence=['#221F1F'], template="plotly_white")
        fig_tv_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    else:
        fig_tv_bar = go.Figure().update_layout(title="Սերիալներ չկան", template="plotly_white")

    return fig_hist, fig_sun, fig_rating_bar, fig_box, fig_tv_bar


# --- Run App ---
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8050, dev_tools_hot_reload=False)