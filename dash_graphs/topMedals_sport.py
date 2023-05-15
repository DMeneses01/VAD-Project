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

athlete_results = athlete_results.drop(columns=['result_id','athlete','athlete_id','pos', 'index'])

athlete_results['edition'] = athlete_results['edition'].str.split().str[0].astype(int)

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

athlete_results.to_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','topMedals_sport.csv'), index=False)

sport = athlete_results["sport"].drop_duplicates().sort_values()

colors = ['#D6AF36', '#A7A7AD', '#A77044']

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
        
    athleter = athlete_results[athlete_results['sport'] == sports].reset_index()

    athlete_aux = athleter.copy()

    athleter['medal'] = athleter['medal'].replace([None], 0)
    athleter['medal'] = athleter['medal'].replace(['Gold'], 1)
    athleter['medal'] = athleter['medal'].replace(['Silver'], 1)
    athleter['medal'] = athleter['medal'].replace(['Bronze'], 1)

    athleter = athleter.drop(columns=['edition_id','sport','event','isTeamSport'])

    medals = pd.DataFrame(athleter.groupby(['country_noc']).sum()).reset_index().sort_values(by=['medal'], ascending=False).head(10)

    athlete_aux = athlete_aux[athlete_aux['country_noc'].isin(medals['country_noc'])]

    medals = pd.DataFrame(athlete_aux.groupby(['country_noc' , 'medal']).count()).reset_index()
    medals.drop(columns=['edition_id','sport','event','isTeamSport'], inplace=True)
    medals.rename(columns={'edition': 'count', 'country_noc': 'country'}, inplace=True)

    fig = go.Figure()

    fig = px.bar(medals, x="country", y="count", color='medal', 
             color_discrete_map={
                'Gold': '#D6AF36',
                'Silver': '#A7A7AD',
                'Bronze': '#A77044'}, 
            title="Top Medals at Athletics by Country").update_xaxes(categoryorder="total descending").update_layout(font_family= 'Cabin')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

