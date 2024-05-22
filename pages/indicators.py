import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages import all_map, country, indicators
from data import df, all_cont
from dash import html, dcc, callback, Output, Input
import plotly.express as px

layout = dbc.Container([
    html.Div([
        html.H3("Диаграммы сравнения"),
        html.P(
            "Анализ основных показателей по странам мира с 2000 по 2015 годы."
            " Используйте фильтры, чтобы увидеть результат."
            )
        ], 
        style={'textAlign': 'center'}
        ),
html.Div([
  html.Div([
    html.Label('Континенты'),
    dcc.Dropdown(
      id = 'crossfilter-cont',
      options = [{'label': i, 'value': i} for i in all_cont],
      # значение континента, выбранное по умолчанию
      value = ['Europe'],
      # возможность множественного выбора
      multi = True
    )
  ],style = {'width': '48%', 'display': 'inline-block'}),

  html.Div([
    html.Label('Основные показатели'),
    dcc.RadioItems(
      options = [
        {'label':'Продолжительность жизни', 'value': 'Life expectancy'},
        {'label':'Население', 'value': 'Population'},
        {'label':'ВВП', 'value': 'GDP'},
        {'label':'Школьное образование', 'value': 'Schooling'},
      ],
      id = 'crossfilter-ind',
      value = 'GDP',
      labelStyle={'display': 'inline-block'})
      ],
      style = {'width': '48%',  'float': 'right', 'display': 'inline-block'}),
    ], style = {
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'}
  ),
  html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = df['Year'].min(),
                max = df['Year'].max(),
                value = 2000,
                step = None,
                marks = {str(year):
                    str(year) for year in df['Year'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),

        html.Div(
            dcc.Graph(id = 'bar'),
            style = {'width': '49%', 'display': 'inline-block'}
        ),
       
        html.Div(
            dcc.Graph(id = 'line'),
            style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Graph(id = 'choropleth'),
            style = {'width': '100%', 'display': 'inline-block'}
        ),
        
    dbc.Col([
    dbc.Row([
        html.H5("ТОП-5 стран"),
        html.Div(id="tabletop"),
            ])

    ], width=4, style={'textAlign':'center'}),
], 


fluid=True)

@callback(
    Output('bar', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['continent'].isin(continent))]
    figure = px.bar(
        filtered_data,
        x = 'Year',
        y = indication,
        color = 'Country'
        )
    return figure

@callback(
    Output('line', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['continent'].isin(continent))]
    figure = px.line(
        filtered_data,
        x = "Year",
        y = indication,
        color = "Country",
        title = "Значения показателя по странам",
        markers = True,
    )
    return figure


@callback(
    Output('tabletop', 'children'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_table(continent, indication, year):
    gdp_count = df[(df['Year'] == year) &
        (df['continent'].isin(continent))].sort_values(by=indication, ascending=False)
    gdp_table = gdp_count.iloc[0:5][['Country', indication]]
    table = dbc.Table.from_dataframe(
        gdp_table, striped=True, bordered=True, hover=True, index=False)
    return table

# @callback(
#     Output('choropleth', 'figure'),
#     Input('crossfilter-ind', 'value')
# )
# def update_choropleth(indication):
#     figure = px.choropleth(
#         df,
#         locations='Country',
#         locationmode = 'country names',
#         color=indication,
#         hover_name='Country',
#         title='Показатели по странам',
#         color_continuous_scale=px.colors.sequential.BuPu,
#         animation_frame='Year',
#         height=650
#         )
#     return figure


