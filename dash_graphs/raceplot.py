import pandas as pd
from raceplotly.plots import barplot
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash
from random import sample
import plotly.graph_objects as go

Path = os.getcwd()
athlete_Event_Results = pd.read_csv(os.path.join(Path,'Dataset', 'Olympic_Athlete_Event_Results.csv'), sep=',')

athlete_Event_Results = athlete_Event_Results.replace(["na"], None)


athlete_results = athlete_Event_Results[athlete_Event_Results["edition"].str.contains("Winter") == False]   # apenas jogos de verao


athlete_results = athlete_results[athlete_results["country_noc"].str.contains("MIX")==False] # Impossivel dividir
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("EUN")==False] # Impossivel dividir
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("IOA")==False] # Impossivel dividir
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("BOH")==False]    # Eslováquia + Republica Checa
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("ANZ")==False]    # Australia + Nova Zelandia + Nova Guine + partes da Indonesia
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("TCH")==False]    # Eslováquia + Republica Checa
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("YUG")==False] # Bosnia + Croacia + Macedonia + Montenegro + Eslovenia + Servia
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("URS")==False] # Russia + Letonia + Lituania + Estonia + Georgia + Armenia + Azerbaijao + Bielorrussia + Cazaquistao + Moldavia + Quirguistao + Tajiquistao + Turquemenistao + Ucrania + Usbequistao
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("UAR")==False]  # Egypt + Syria + Faixa de Gaza
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("WIF")==False] # Antigua + Barbados + Cayman Islands + Dominica + Grenada + Jamaica + Montserrat + St Christopher-Nevis-Anguilla + Saint Lucia	+ St Vincent and the Grenadines	+ Trinidad and Tobago + Turks and Caicos Islands	

athlete_results['country_noc'] = athlete_results['country_noc'].replace(['FRG'], 'GER')
athlete_results['country_noc'] = athlete_results['country_noc'].replace(['GDR'], 'GER')

athlete_results['country_noc'] = athlete_results['country_noc'].replace(['HKG'], 'CHN')

athlete_results['country_noc'] = athlete_results['country_noc'].replace(['ROC'], 'RUS')

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

athlete_results.to_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','raceplot.csv'), index=False)

sport = athlete_results["sport"].drop_duplicates().sort_values()

app = Dash(__name__)

app.layout = html.Div(style={'font-family': 'Cabin'}, children = [
    dcc.Dropdown(id="dropdown",
            options=[ {'label': x, 'value': x}
                    for x in sport
        ],
            value='Athletics',
            clearable=False,
        ),
    dcc.Graph(id="graph"),
])


@app.callback(
Output("graph", "figure"),
[Input("dropdown", "value")])
def medals_type(sports):
        
    athlete_r = athlete_results[athlete_results['sport'] == sports]

    df = pd.DataFrame(athlete_r.groupby(['edition','country_noc']).sum()).reset_index()

    for i in df['edition'].unique():
        for j in df['country_noc'].unique():
            if df[(df['edition'] == i) & (df['country_noc'] == j)].empty:
                df.loc[len(df), ['edition','country_noc', 'medal']] = i, j, 0

    df['edition'] = df['edition'].astype(int)
    df['medal'] = df['medal'].astype(int)

    new_medal = []
    for i in range(len(df)):
        edition = df.loc[i, 'edition']
        country = df.loc[i, 'country_noc']
        medals = df.loc[i, 'medal']

        new_medal.append(df[(df['edition'] <= edition) & (df['country_noc'] == country)]['medal'].sum())

    df['medals'] = new_medal
    df.drop(columns=['medal'], inplace=True)
    
    my_raceplot = barplot(df, item_column='country_noc', value_column='medals', time_column='edition')

    my_raceplot.plot(item_label = 'Top 10 countries', value_label = 'Amount of Medals', time_label='Year ', frame_duration = 800)
    
    return my_raceplot.fig

if __name__ == '__main__':
    app.run_server(debug=True)


