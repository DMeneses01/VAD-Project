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

athlete_results = athlete_results.drop(columns=['result_id','athlete','athlete_id','pos', 'index'])

athlete_results['edition'] = athlete_results['edition'].str.split().str[0].astype(int)
	

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

athlete_results['medal'] = athlete_results['medal'].replace([None], 0)
athlete_results['medal'] = athlete_results['medal'].replace(['Gold'], 1)
athlete_results['medal'] = athlete_results['medal'].replace(['Silver'], 1)
athlete_results['medal'] = athlete_results['medal'].replace(['Bronze'], 1)

athlete_results = athlete_results.drop(columns=['edition_id','sport','event','isTeamSport'])

athlete_results = athlete_results.merge(country_n, on='country_noc', how='left')

athlete_results.to_csv('../react_site/src/Dataframes/with_without_country.csv', index=False)

countries = athlete_results['country'].drop_duplicates().sort_values()

colors = ['#D6AF36', '#A7A7AD', '#A77044']


app = Dash(__name__)

app.layout = html.Div(style={'font-family': 'Cabin'}, children = [
    dcc.Dropdown(id="dropdown",
            options=[ {'label': x, 'value': x}
                    for x in countries
        ],
            value='Portugal',
            clearable=False,
        ),
    html.H4('Top 10 Medals by Country'),
    dcc.Graph(id="graph"),
])

@app.callback(
Output("graph", "figure"),
[Input("dropdown", "value")])
def medals_type(country):

    country_df = athlete_results[athlete_results["country"] == country]

    years = country_df["edition"].unique()

    year = []
    medal = []
    count = []

    for y in years:
        year.append(y)
        year.append(y)

        medal.append("Without")
        medal.append("With")

        withm = len(country_df[(country_df['edition'] == y) & (country_df['medal'] == 1)])
        withoutm = len(country_df[(country_df['edition'] == y) & (country_df['medal'] == 0)])

        count.append(withoutm)
        count.append(withm)

    df = pd.DataFrame()
    df["year"] = year
    df["medal"] = medal
    df["count"] = count

    df_with = df[df.medal == 'With']
    df_without = df[df.medal == 'Without']

    df_without['count'] = - df_without['count']

    colors = ['#EE334E', '#0081C8']

    fig = go.Figure()

    fig.add_trace(go.Bar(
            y = df_with["count"],
            x = df_with.year,
            name = 'With',
            
            marker_color=colors[0]
    ))

    fig.add_trace(go.Bar(
            y = df_without["count"],
            x = df_without.year,
            name = 'Without',
            
            marker_color=colors[1]
    ))

    fig.update_layout(xaxis=dict(tickformat='(.0f'), barmode = 'relative', font_family= 'Cabin',
                      yaxis_title="count", xaxis_title="year",
                      title={
                        'text': "<b>Medals vs Participations</b>",
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'x':0.5},
                      paper_bgcolor="white",
                      plot_bgcolor="white", width=1700, height=300, autosize = False,
                      legend=dict(yanchor="top", xanchor="left", font=dict(size=15)), 
                      margin=dict(l=1, r=2, b=20, t=31, pad=0))


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
