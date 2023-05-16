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

athlete_Event_Results = pd.read_csv('../Dataset/Olympic_Athlete_Event_Results.csv', sep=',')
country_n = pd.read_csv('../Dataset/Olympics_Country.csv', sep=',')

#merge on country_noc

athlete_Event_Results = athlete_Event_Results.replace(["na"], None)


athlete_results = athlete_Event_Results[athlete_Event_Results["edition"].str.contains("Winter") == False]   # apenas jogos de verao

athlete_results = athlete_results.reset_index()

athlete_results = athlete_results.drop(columns=['result_id','athlete','athlete_id','pos'])


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

athlete_results = athlete_results.merge(country_n, on='country_noc', how='left')

athlete_results["Type_sport"] = [""] * len(athlete_results)

athlete_results.loc[athlete_results['sport'].str.contains("Athletics"), "Type_sport"] = "Athletics"
athlete_results.loc[athlete_results['sport'].str.contains("Boxing"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Diving"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Rugby"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Shooting"), "Type_sport"] = "Shooting"
athlete_results.loc[athlete_results['sport'].str.contains("Swimming"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Rowing"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Tennis"), "Type_sport"] = "Rackets"
athlete_results.loc[athlete_results['sport'].str.contains("Artistic Gymnastics"), "Type_sport"] = "Gymnastics"
athlete_results.loc[athlete_results['sport'].str.contains("Cycling Track"), "Type_sport"] = "Cycling"
athlete_results.loc[athlete_results['sport'].str.contains("Fencing"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Wrestling"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Cycling Road"), "Type_sport"] = "Cycling"
athlete_results.loc[athlete_results['sport'].str.contains("Artistic Swimming"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Judo"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Sailing"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Weightlifting"), "Type_sport"] = "Various"
athlete_results.loc[athlete_results['sport'].str.contains("Taekwondo"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Archery"), "Type_sport"] = "Shooting"
athlete_results.loc[athlete_results['sport'].str.contains("Golf"), "Type_sport"] = "Golf"
athlete_results.loc[athlete_results['sport'].str.contains("Canoe Sprint"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Cycling Mountain Bike"), "Type_sport"] = "Cycling"
athlete_results.loc[athlete_results['sport'].str.contains("Modern Pentathlon"), "Type_sport"] = "Various"
athlete_results.loc[athlete_results['sport'].str.contains("Handball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Basketball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Roller Hockey"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Beach Volleyball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Triathlon"), "Type_sport"] = "Various"
athlete_results.loc[athlete_results['sport'].str.contains("Hockey"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Football"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Badminton"), "Type_sport"] = "Rackets"
athlete_results.loc[athlete_results['sport'].str.contains("Wushu"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Rhythmic Gymnastics"), "Type_sport"] = "Gymnastics"
athlete_results.loc[athlete_results['sport'].str.contains("Equestrian Jumping"), "Type_sport"] = "Equestrian"
athlete_results.loc[athlete_results['sport'].str.contains("Canoe Slalom"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Karate"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Table Tennis"), "Type_sport"] = "Rackets"
athlete_results.loc[athlete_results['sport'].str.contains("Volleyball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Trampolining"), "Type_sport"] = "Gymnastics"
athlete_results.loc[athlete_results['sport'].str.contains("Marathon Swimming"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Equestrian Eventing"), "Type_sport"] = "Equestrian"
athlete_results.loc[athlete_results['sport'].str.contains("Equestrian Dressage"), "Type_sport"] = "Equestrian"
athlete_results.loc[athlete_results['sport'].str.contains("Cycling BMX Freestyle"), "Type_sport"] = "Cycling"
athlete_results.loc[athlete_results['sport'].str.contains("Surfing"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Water Polo"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Baseball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Cycling BMX Racing"), "Type_sport"] = "Cycling"
athlete_results.loc[athlete_results['sport'].str.contains("Waterskiing"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Rugby Sevens"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Skateboarding"), "Type_sport"] = "Skateboarding"
athlete_results.loc[athlete_results['sport'].str.contains("Bowling"), "Type_sport"] = "Various"
athlete_results.loc[athlete_results['sport'].str.contains("Softball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Sport Climbing"), "Type_sport"] = "Mountain"
athlete_results.loc[athlete_results['sport'].str.contains("Basque pelota"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Figure Skating"), "Type_sport"] = "Gymnastics"
athlete_results.loc[athlete_results['sport'].str.contains("Polo"), "Type_sport"] = "Equestrian"
athlete_results.loc[athlete_results['sport'].str.contains("Gliding"), "Type_sport"] = "Air"
athlete_results.loc[athlete_results['sport'].str.contains("Automobile Racing"), "Type_sport"] = "Motors"
athlete_results.loc[athlete_results['sport'].str.contains("Equestrian Driving"), "Type_sport"] = "Equestrian"
athlete_results.loc[athlete_results['sport'].str.contains("Equestrian Vaulting"), "Type_sport"] = "Equestrian"
athlete_results.loc[athlete_results['sport'].str.contains("Ice Hockey"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Tug-Of-War"), "Type_sport"] = "Various"
athlete_results.loc[athlete_results['sport'].str.contains("Savate"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Canoe Marathon"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("3x3 Basketball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Glíma"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Australian Rules Football"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Pesäpallo"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Lacrosse"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Bicycle Polo"), "Type_sport"] = "Cycling"
athlete_results.loc[athlete_results['sport'].str.contains("Alpinism"), "Type_sport"] = "Mountain"
athlete_results.loc[athlete_results['sport'].str.contains("Kendo"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Ballooning"), "Type_sport"] = "Air"
athlete_results.loc[athlete_results['sport'].str.contains("Cricket"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Croquet"), "Type_sport"] = "Golf"
athlete_results.loc[athlete_results['sport'].str.contains("Fishing"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Motorcycle Sports"), "Type_sport"] = "Motors"
athlete_results.loc[athlete_results['sport'].str.contains("Motorboating"), "Type_sport"] = "Aquatic"
athlete_results.loc[athlete_results['sport'].str.contains("Canne De Combat"), "Type_sport"] = "Fight"
athlete_results.loc[athlete_results['sport'].str.contains("Jeu De Paume"), "Type_sport"] = "Rackets"
athlete_results.loc[athlete_results['sport'].str.contains("Racquets"), "Type_sport"] = "Rackets"
athlete_results.loc[athlete_results['sport'].str.contains("Korfball"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Kaatsen"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Aeronautics"), "Type_sport"] = "Air"
athlete_results.loc[athlete_results['sport'].str.contains("American Football"), "Type_sport"] = "Team sport with Ball"
athlete_results.loc[athlete_results['sport'].str.contains("Roque"), "Type_sport"] = "Golf"

athlete_results = athlete_results.loc[(athlete_results["Type_sport"] != "")]

gr = pd.DataFrame(athlete_results.groupby(['country', 'Type_sport', 'edition', 'sport']).sum()).reset_index()

gr.to_csv('../react_site/src/Dataframes/linechart_country.csv', index=False)

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
        sport = dataset.loc[i, 'Type_sport']
        event = dataset.loc[i, 'sport']

        new_medal.append(dataset[(dataset['edition'] <= edition) & (dataset['Type_sport'] == sport) & (dataset['sport'] == event)]['medal'].sum())

    dataset['medal'] = new_medal


    df = dataset#px.data.gapminder()
    mask = df.Type_sport.isin(sports)
    fig = px.line(df[mask], 
        x="edition", y="medal", color='sport').update_layout({
                                                    'plot_bgcolor': '#FFFFFF',
                                                    'paper_bgcolor': '#EEF1FA'
                                                    }, font_family= 'Cabin'
                                                    )
    fig.update_xaxes(showline=True, linewidth=2, gridcolor='#c7c7c7')
    fig.update_yaxes(showline=True, linewidth=2, gridcolor='#c7c7c7')


    return [{'label': x, 'value': x} for x in pd.unique(dataset.Type_sport)], fig



app.run_server()