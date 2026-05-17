from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import df

layout = html.Div([
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
                    value="All", 
                    inline=True,
                    persistence=True,
                    persistence_type='session',
                    className="mb-3"
                ),
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


                dcc.Loading(
                    id="loading-map",
                    type="dot",
                    children=dcc.Graph(id="map-plot")
                )
            ])
        ])



@callback(
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
