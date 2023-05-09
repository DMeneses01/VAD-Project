import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os
import pandas as pd
import geopandas as gpd

app = Dash(__name__)

Path = os.getcwd()
medals = pd.read_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','top10_medals.csv'))

colors = ['#D6AF36', '#A7A7AD', '#A77044']
colors = {
    'background': '#EEF1FA'
}
text = {
    'font_family': 'Cabin'
}

fig1 = px.bar(medals, x="country", y="count", color='medal', 
             color_discrete_map={
                'Gold': '#D6AF36',
                'Silver': '#A7A7AD',
                'Bronze': '#A77044'}, width=300, height=600)

fig1.update_xaxes(categoryorder="total descending")
fig1.update_layout(font_family= 'Cabin', margin={'t':5, 'b':5, 'r': 3, 'l': 3})

countries = gpd.read_file(os.path.join(os.getcwd(), 'Dataset', 'countries.geojson'))
heatmap = pd.read_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','heatmap.csv'))

fig2 = px.choropleth(heatmap, geojson=countries, locations='country', locationmode='country names', color='total',
                           color_continuous_scale='viridis',
                           range_color=(0, max(heatmap["total"])),
                           labels={'total':'medals'},  width=1150, height=550
                          )
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#EEF1FA", font_family= 'Cabin')


dash.register_page(__name__, path='/dashboard')

layout = html.Div(
    [
	    
        html.Div(children=[
                html.Div(children = [
                    html.H4('Top 10 Medals by Country', style={'position': 'absolute', 'left': '3.5vw', 'position': 'absolute', 'fontFamily': text['font_family'], 'width': '30vw','height': '5vh', 'background': '#EEF1FA'}),
                    dcc.Graph(id="graph", figure=fig2, style={'position': 'absolute', 'left': '3vw', 'top': '10vh','position': 'absolute', 'background': '#EEF1FA'}),
                    
                ])
        ], style = {'position': 'absolute', 'width': '72vw','height': '88vh', 'left': '26vw', 'top': '11vh', 'background': '#EEF1FA', 'borderRadius': '14vh 0vh 0vh 14vh'}),
		
        html.Div([
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(
                                    f"{'By country'}", href=page["relative_path"]
                                ), style={'position': 'absolute', 'width': '10vw', 'height':'6.5vh', 'left': '2vw', 'top':'-0.9vh',
                                        'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '500', 'fontSize': '2.6vh',
                                        'lineHeight': '1.89vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em'}
                            )
                            for page in dash.page_registry.values()
                            if page["path"] == "/by_country"
                        ], style= {'position': 'absolute', 'width': '10vw', 'height': '5vh', 'left': '70vw', 'top': '3vh',
                                    'background': '#FFFFFF', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'borderRadius': '7px'}
				    ), 
				    #html.Img(src='/assets/round-chevron-right.svg')         
                ]
        ),
	
        html.Div([
                html.H1('Jogos Olímpicos à Lupa', style={'position': 'absolute', 'width': '30vw', 'height': '3.22vh', 'left': '4vw', 'top': '1vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                html.Div(children = [
                    html.H4('Top 10 Medals by Country', style={'position': 'absolute', 'left': '3.5vw'}),
                    dcc.Graph(id="graph", figure=fig1, style={'position': 'absolute', 'left': '0.2vw', 'top': '7vh'}),    
                ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 'position': 'absolute',
                        'width': '18vw', 'height': '87vh', 'left': '3.5vw', 'top': '11vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'})
            ]),
                    
        html.Div(
            style={
                'backgroundColor': '#F6F7FB',
                'height': '98vh'}
		)
    ]
)