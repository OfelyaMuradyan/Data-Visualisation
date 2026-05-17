from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import df
import plotly.graph_objs as go

layout = html.Div([
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



@callback(
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

