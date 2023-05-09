import pandas as pd
import plotly.express as px

from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash
import os

app = Dash(__name__)

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

athlete_aux = athlete_results.copy()

athlete_results['medal'] = athlete_results['medal'].replace([None], 0)
athlete_results['medal'] = athlete_results['medal'].replace(['Gold'], 1)
athlete_results['medal'] = athlete_results['medal'].replace(['Silver'], 1)
athlete_results['medal'] = athlete_results['medal'].replace(['Bronze'], 1)

athlete_results = athlete_results.drop(columns=['edition_id','sport','event','isTeamSport'])

medals = pd.DataFrame(athlete_results.groupby(['country_noc']).sum()).reset_index().sort_values(by=['medal'], ascending=False).head(10)

athlete_aux = athlete_aux[athlete_aux['country_noc'].isin(medals['country_noc'])]

medals = pd.DataFrame(athlete_aux.groupby(['country_noc' , 'medal']).count()).reset_index()
medals.drop(columns=['edition_id','sport','event','isTeamSport'], inplace=True)
medals.rename(columns={'edition': 'count', 'country_noc': 'country'}, inplace=True)

medals.to_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','top10_medals.csv'), index=False)


colors = ['#D6AF36', '#A7A7AD', '#A77044']
colors = {
    'background': '#EEF1FA'
}
text = {
    'font_family': 'Cabin'
}

fig = px.bar(medals, x="country", y="count", color='medal', 
             color_discrete_map={
                'Gold': '#D6AF36',
                'Silver': '#A7A7AD',
                'Bronze': '#A77044'}, width=1200, height=900).update_xaxes(categoryorder="total descending").update_layout(font_family= 'Cabin', margin={'t':5, 'b':5, 'r': 3, 'l': 3})

app.layout = html.Div(style={'font-family': text['font_family']}, children = [
    html.H4('Top 10 Medals by Country'),
    dcc.Graph(id="graph", figure=fig),
    
])

if __name__ == '__main__':
    app.run_server(debug=True)


