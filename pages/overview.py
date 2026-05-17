from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import df


layout = html.Div([
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


@callback(
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
