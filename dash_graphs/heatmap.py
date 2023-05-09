import geopandas as gpd
import pandas as pd
import os

from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash
import os

app = Dash(__name__)
countries = gpd.read_file(os.path.join(os.getcwd(), 'Dataset', 'countries.geojson'))


games_Medal = pd.read_csv(os.path.join(os.getcwd(), 'Dataset', 'Olympic_Games_Medal_Tally.csv'), sep=',', encoding_errors='replace')
games_Medal = games_Medal.replace(["na"], None)

games_Medal = games_Medal[games_Medal["edition"].str.contains("Winter") == False]

df = pd.DataFrame(games_Medal["country"].unique(), columns=["country"])

total = games_Medal.groupby('country')['total'].sum()

df = pd.merge(df, total, on='country', how='left')

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

df.loc[df['country'] == "Germany", ['total']] += df.loc[df['country'] == "West Germany", ['total']].values[0][0]
df.loc[df['country'] == "Germany", ['total']] += df.loc[df['country'] == "East Germany", ['total']].values[0][0]
df = df[df["country"].str.contains("West Germany")==False]
df = df[df["country"].str.contains("East Germany")==False]

df.loc[df['country'] == "People's Republic of China", ['total']] += df.loc[df['country'] == "Hong Kong, China", ['total']].values[0][0]
df = df[df["country"].str.contains("Hong Kong, China")==False]

df.loc[df['country'] == "Russian Federation", ['total']] += df.loc[df['country'] == "ROC", ['total']].values[0][0]
df = df[df["country"].str.contains("ROC")==False]


Path = os.getcwd()
df.to_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','heatmap.csv'), index=False)


colors = ['#D6AF36', '#A7A7AD', '#A77044']
colors = {
    'background': '#EEF1FA'
}
text = {
    'font_family': 'Cabin'
}

fig = px.choropleth(df, geojson=countries, locations='country', locationmode='country names', color='total',
                           color_continuous_scale='viridis',
                           range_color=(0, max(df["total"])),
                           labels={'total':'medals'}
                          )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(style={'font-family': text['font_family']}, children = [
    html.H4('Top 10 Medals by Country'),
    dcc.Graph(id="graph", figure=fig),
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
