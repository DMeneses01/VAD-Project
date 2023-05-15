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
athlete_Event_Results = pd.read_csv('../Dataset/Olympic_Athlete_Event_Results.csv', sep=',')

athlete_Event_Results = athlete_Event_Results.replace(["na"], None)


athlete_results = athlete_Event_Results[athlete_Event_Results["edition"].str.contains("Winter") == False]   # apenas jogos de verao



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

athlete_results["medal"] = athlete_results["medal"].notnull().mul(1)

athlete_results.to_csv('../react_site/src/Dataframes/raceplot.csv', index=False)

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

    # Group the athlete_r DataFrame by edition and country_noc and sum the medal column
    df = athlete_r.groupby(['edition', 'country_noc'])['medal'].sum().reset_index()

    # Create a MultiIndex with all possible combinations of edition and country_noc
    index = pd.MultiIndex.from_product([df['edition'].unique(), df['country_noc'].unique()], names=['edition', 'country_noc'])

    # Reindex the DataFrame with the new MultiIndex and fill missing values with 0
    df = df.set_index(['edition', 'country_noc']).reindex(index, fill_value=0).reset_index()

    df['edition'] = df['edition'].astype(int)
    df['medal'] = df['medal'].astype(int)

    # Sort the DataFrame by edition and country_noc
    df = df.sort_values(['edition', 'country_noc'])

    # Group the DataFrame by country_noc and calculate the cumulative sum of the medal column
    df['new_medal'] = df.groupby('country_noc')['medal'].cumsum()
    
    my_raceplot = barplot(df, item_column='country_noc', value_column='new_medal', time_column='edition')

    my_raceplot.plot(item_label = 'Top 10 countries', value_label = 'Amount of Medals', time_label='Year ', frame_duration = 800)
    
    return my_raceplot.fig

if __name__ == '__main__':
    app.run_server(debug=True)


