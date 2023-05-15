from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash
Path = os.getcwd()

athlete_Event_Results = pd.read_csv(os.path.join(Path,'Dataset', 'Olympic_Athlete_Event_Results.csv'), sep=',')
country_n = pd.read_csv(os.path.join(Path,'Dataset', 'Olympics_Country.csv'), sep=',')

#merge on country_noc

athlete_Event_Results = athlete_Event_Results.replace(["na"], None)


athlete_results = athlete_Event_Results[athlete_Event_Results["edition"].str.contains("Winter") == False]   # apenas jogos de verao

athlete_results = athlete_results.reset_index()

athlete_results = athlete_results.drop(columns=['result_id','athlete','athlete_id','pos'])


repeat = []
i=0
while(i < len(athlete_results)):
    if athlete_results.loc[i, 'isTeamSport'] == True:
        auxi = i + 1 
        p = athlete_results.loc[i, 'country_noc']
        e = athlete_results.loc[i, 'event']
        a = athlete_results.loc[i, 'edition_id']
        while((athlete_results.loc[auxi, 'country_noc'] == p) and (athlete_results.loc[auxi, 'event'] == e) and (athlete_results.loc[auxi, 'edition_id'] == a)):
            repeat.append(auxi)
            auxi += 1
        i = auxi-1
    i+=1

athlete_results.drop(repeat, inplace=True)
athlete_results.drop(columns=['edition_id', 'isTeamSport', 'index'], inplace=True)
athlete_results['edition'] = athlete_results['edition'].str.split().str[0].astype(int)

athlete_results["medal"] = athlete_results["medal"].notnull().mul(1)

athlete_results = athlete_results.merge(country_n, on='country_noc', how='left')

gr = pd.DataFrame(athlete_results.groupby(['country', 'sport', 'edition', 'event']).sum()).reset_index()

countries = athlete_results['country'].drop_duplicates().sort_values()

app = Dash(__name__)


app.layout = html.Div(style={'font-family': 'Cabin'}, children = [
    dcc.Dropdown(id="dropdown",
            options=[ {'label': x, 'value': x}
                    for x in countries
        ],
            value='Portugal',
            clearable=False,
        ),
    html.Div(children=[
        html.H4('Sports evolution'),
        dcc.Graph(id="graph"),
        dcc.Checklist(
            id='checklist',
            options=[],
            value=[],
            inline=True
        )
        ], 
    style={'backgroundColor': '#EEF1FA', 'font-family': 'Cabin'})
    
])



@app.callback(
    Output('checklist', 'options'),
    Output('graph', 'figure'),
    Input("dropdown", "value"),
    Input('checklist', 'value'))

def update_line_chart(country, sports):
    dataset = gr[gr['country'] == country].reset_index()

    new_medal = []
    for i in range(len(dataset)):
        edition = dataset.loc[i, 'edition']
        sport = dataset.loc[i, 'sport']
        event = dataset.loc[i, 'event']

        new_medal.append(dataset[(dataset['edition'] <= edition) & (dataset['sport'] == sport) & (dataset['event'] == event)]['medal'].sum())

    dataset['medal'] = new_medal


    df = dataset#px.data.gapminder()
    mask = df.sport.isin(sports)
    fig = px.line(df[mask], 
        x="edition", y="medal", color='event').update_layout({
                                                    'plot_bgcolor': '#FFFFFF',
                                                    'paper_bgcolor': '#EEF1FA'
                                                    }, font_family= 'Cabin'
                                                    )
    fig.update_xaxes(showline=True, linewidth=2, gridcolor='#c7c7c7')
    fig.update_yaxes(showline=True, linewidth=2, gridcolor='#c7c7c7')


    return [{'label': x, 'value': x} for x in pd.unique(dataset.sport)], fig



app.run_server()