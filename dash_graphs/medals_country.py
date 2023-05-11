import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash
Path = os.getcwd()

games_Medal = pd.read_csv(os.path.join(Path,'Dataset', 'Olympic_Games_Medal_Tally.csv'), sep=',')
games_Medal = games_Medal.replace(["na"], None)

games_Medal = games_Medal[games_Medal["edition"].str.contains("Winter") == False]   # apenas jogos de verao

df = pd.DataFrame(games_Medal["country"].unique(), columns=["country"])

gold = games_Medal.groupby('country')['gold'].sum()
silver = games_Medal.groupby('country')['silver'].sum()
bronze = games_Medal.groupby('country')['bronze'].sum()

df = pd.merge(df, gold, on='country', how='left')
df = pd.merge(df, silver, on='country', how='left')
df = pd.merge(df, bronze, on='country', how='left')


# CLEANING DATA

df = df[df["country"].str.contains("Mixed team")==False] # Impossivel dividir
df = df[df["country"].str.contains("Unified Team")==False] # Impossivel dividir
df = df[df["country"].str.contains("Individual Olympic Athletes")==False] # Impossivel dividir
df = df[df["country"].str.contains("Bohemia")==False]    # Eslováquia + Republica Checa
df = df[df["country"].str.contains("Australasia")==False]    # Australia + Nova Zelandia + Nova Guine + partes da Indonesia
df = df[df["country"].str.contains("Czechoslovakia")==False]    # Eslováquia + Republica Checa
df = df[df["country"].str.contains("Yugoslavia")==False] # Bosnia + Croacia + Macedonia + Montenegro + Eslovenia + Servia
df = df[df["country"].str.contains("Soviet Union")==False] # Russia + Letonia + Lituania + Estonia + Georgia + Armenia + Azerbaijao + Bielorrussia + Cazaquistao + Moldavia + Quirguistao + Tajiquistao + Turquemenistao + Ucrania + Usbequistao
df = df[df["country"].str.contains("United Arab Republic")==False]  # Egypt + Syria + Faixa de Gaza
df = df[df["country"].str.contains("West Indies Federation")==False] # Antigua + Barbados + Cayman Islands + Dominica + Grenada + Jamaica + Montserrat + St Christopher-Nevis-Anguilla + Saint Lucia	+ St Vincent and the Grenadines	+ Trinidad and Tobago + Turks and Caicos Islands	

df["country"] = df["country"].replace('Türkiye', 'Turkey')

df.loc[df['country'] == "Germany", ['gold']] += df.loc[df['country'] == "West Germany", ['gold']].values[0][0]
df.loc[df['country'] == "Germany", ['gold']] += df.loc[df['country'] == "East Germany", ['gold']].values[0][0]
df.loc[df['country'] == "Germany", ['silver']] += df.loc[df['country'] == "West Germany", ['silver']].values[0][0]
df.loc[df['country'] == "Germany", ['silver']] += df.loc[df['country'] == "East Germany", ['silver']].values[0][0]
df.loc[df['country'] == "Germany", ['bronze']] += df.loc[df['country'] == "West Germany", ['bronze']].values[0][0]
df.loc[df['country'] == "Germany", ['bronze']] += df.loc[df['country'] == "East Germany", ['bronze']].values[0][0]
df = df[df["country"].str.contains("West Germany")==False]
df = df[df["country"].str.contains("East Germany")==False]

df.loc[df['country'] == "People's Republic of China", ['gold']] += df.loc[df['country'] == "Hong Kong, China", ['gold']].values[0][0]
df.loc[df['country'] == "People's Republic of China", ['silver']] += df.loc[df['country'] == "Hong Kong, China", ['silver']].values[0][0]
df.loc[df['country'] == "People's Republic of China", ['bronze']] += df.loc[df['country'] == "Hong Kong, China", ['bronze']].values[0][0]
df = df[df["country"].str.contains("Hong Kong, China")==False]

df.loc[df['country'] == "Russian Federation", ['gold']] += df.loc[df['country'] == "ROC", ['gold']].values[0][0]
df.loc[df['country'] == "Russian Federation", ['silver']] += df.loc[df['country'] == "ROC", ['silver']].values[0][0]
df.loc[df['country'] == "Russian Federation", ['bronze']] += df.loc[df['country'] == "ROC", ['bronze']].values[0][0]
df = df[df["country"].str.contains("ROC")==False]

df.to_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','medals_country.csv'), index=False)

countries = df['country'].drop_duplicates().sort_values()

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

    goldv = df.loc[(df['country'] == country), 'gold'].values[0]
    silverv = df.loc[(df['country'] == country), 'silver'].values[0]
    bronzev = df.loc[(df['country'] == country), 'bronze'].values[0]

    fig = go.Figure(data=[go.Pie(labels=['Gold','Silver','Bronze'],
                                values=[goldv,silverv,bronzev])])                       
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    fig.update_layout(font_family= 'Cabin',autosize = False, width = 300, height = 172, 
                      legend=dict(yanchor="top", xanchor="left", font=dict(size=15)),
                      margin=dict(l=1, r=2, b=20, t=31, pad=0),
                      title={
                        'text': "<b>Medals</b>",
                        'y':0.9,
                        'x':0.15,
                        'xanchor': 'center',
                        'yanchor': 'top'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
