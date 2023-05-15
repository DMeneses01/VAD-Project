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

gr.to_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','top5_sports_country.csv'), index=False)

countries = gr['country'].drop_duplicates().sort_values()

app = Dash(__name__)

app.layout = html.Div(style={'font-family': 'Cabin'}, children = [
    dcc.Dropdown(id="dropdown",
            options=[ {'label': x, 'value': x}
                    for x in countries
        ],
            value='Portugal',
            clearable=False,
        ),
    html.H4('Top 5 Sports'),
    dcc.Graph(id="graph"),
])

@app.callback(
Output("graph", "figure"),
[Input("dropdown", "value")])
def medals_type(country):

    dataset = gr[gr['country'] == country].reset_index()

    new_medal = []
    for i in range(len(dataset)):
        edition = dataset.loc[i, 'edition']
        sport = dataset.loc[i, 'sport']
        event = dataset.loc[i, 'event']

        new_medal.append(dataset[(dataset['edition'] <= edition) & (dataset['sport'] == sport) & (dataset['event'] == event)]['medal'].sum())

    sports = pd.unique(dataset.sport)

    dataset['medal'] = new_medal

    dataset2 = dataset.copy()

    dataset2 = pd.DataFrame(dataset2.groupby(['sport']).sum()).reset_index()

    dataset2 = dataset2.sort_values(by=['medal'], ascending=False)

    dataset2 = dataset2.head(5)

    color = ['#0081C8', '#FCB131', '#000000', '#00A651', '#EE334E']
    dataset2['color'] = color

    fig = px.bar(dataset2, x="sport", y="medal", color= 'color', title="Top 5 sports for the country", width=300, height=250,
                color_discrete_sequence=['#0081C8', '#FCB131', '#000000', '#00A651', '#EE334E'] )
    fig.update_layout(font_family= 'Cabin',autosize = False, 
                        legend=dict(yanchor="top", xanchor="left", font=dict(size=15)),
                        margin=dict(l=1, r=6, b=20, t=31, pad=0), showlegend=False,)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
