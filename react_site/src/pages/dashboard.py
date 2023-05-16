import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os
import pandas as pd
import geopandas as gpd

import PIL

image_path = os.path.abspath('pages/components/olympic-rings.png')
pil_rings = PIL.Image.open(image_path)

image_path = os.path.abspath('pages/components/round-chevron-right.png')
pil_seta = PIL.Image.open(image_path)

app = Dash(__name__)

Path = os.getcwd()
medals = pd.read_csv(os.path.join(Path, 'Dataframes','top10_medals.csv'))

colors = ['#D6AF36', '#A7A7AD', '#A77044']

fig1 = px.bar(medals, x="country", y="count", color='medal', 
             color_discrete_map={
                'Gold': colors[0],
                'Silver': colors[1],
                'Bronze': colors[2]})

fig1.update_xaxes(categoryorder="total descending")
fig1.update_layout(font_family= 'Cabin', margin={'t':5, 'b':5, 'r': 3, 'l': 3},  yaxis_title="Medals", xaxis_title="Countries",)

countries = gpd.read_file('../../Dataset/countries.geojson')
heatmap = pd.read_csv(os.path.join(Path, 'Dataframes','heatmap.csv'))

fig2 = px.choropleth(heatmap, geojson=countries, locations='country', locationmode='country names', color='total',
                           color_continuous_scale='sunsetdark',
                           range_color=(0, max(heatmap["total"])),
                           labels={'total':'medals'}
                          )
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#EEF1FA", font_family= 'Cabin')


dash.register_page(__name__, path='/dashboard')

layout = html.Div(
    [
	    
        html.Div([
                html.H1('The Olympics under a magnifying glass', style={'position': 'relative', 'width': '30vw', 'height': '3.22vh', 'left': '4vw', 'top': '2vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                html.Div(
                    [
                        html.A(html.Img(src=pil_rings, style={'position': 'relative', 'width': '3vw', 'height': '3.5vh', 'left': '0.5vw', 'top': '-3.5vh'}), href='/'),
                        dcc.Location(id='url', refresh=False),
                      
                    ]
                
                ),      
            ]),

        html.Div(children = [
            html.H4('Top Countries', style={'position': 'relative', 'left': '5.5vw', 'top':'3vh'}),
            dcc.Graph(id="graph", figure=fig1, style={'position': 'relative', 'left': '0.2vw', 'top': '3vh', 'width':'17vw', 'height':'78vh'}),    
        ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 'position': 'relative',
                'width': '18vw', 'height': '87vh', 'left': '3.5vw', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px', 'top': '-1.4vh'}),

        html.Div(children=[
            html.Div(children = [
                html.H4('Medals by Country', style={'left': '3.5vw', 'position': 'relative', 'fontSize': '25px', 'fontFamily': 'Cabin', 'width': '30vw','height': '5vh', 'left':'30vw', 'background': '#EEF1FA', 'top': '5.5vh'}),
                dcc.Graph(id="graph", figure=fig2, style={'position': 'relative', 'left': '4vw', 'top': '1vh','background': '#EEF1FA', 'width': '65vw','height': '75vh'}),
                
            ])
        ], style = {'position': 'relative', 'width': '72vw','height': '87vh', 'left': '26vw', 'top': '-92vh', 'background': '#EEF1FA', 'borderRadius': '12px 0px 0px 12px'}),
		

        html.Div([
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(
                                    f"{'By country'}", href=page["relative_path"]
                                ), style={'position': 'relative', 'width': '10vw', 'height':'6.5vh', 'left': '1.5vw', 'top':'-0.9vh',
                                        'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '500', 'fontSize': '2.6vh',
                                        'lineHeight': '1.89vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em'}
                            )
                            for page in dash.page_registry.values()
                            if page["path"] == "/by_country"
                        ], style= {'position': 'relative', 'width': '10vw', 'height': '5vh', 'left': '74vw', 'top': '-188vh',
                                    'background': '#FFFFFF', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'borderRadius': '12px'}
				    ), 
				    html.Img(src=pil_seta, style={'position': 'relative', 'width': '1.5vw', 'height': '3vh', 'left': '82vw', 'top': '-192vh'}), 
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(
                                    f"{'By sport'}", href=page["relative_path"]
                                ), style={'position': 'relative', 'width': '10vw', 'height':'6.5vh', 'left': '2vw', 'top':'-0.9vh',
                                        'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '500', 'fontSize': '2.6vh',
                                        'lineHeight': '1.89vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em'}
                            )
                            for page in dash.page_registry.values()
                            if page["path"] == "/by_sport"
                        ], style= {'position': 'relative', 'width': '10vw', 'height': '5vh', 'left': '85vw', 'top': '-196.5vh',
                                    'background': '#FFFFFF', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'borderRadius': '12px'}
				    ),
                    html.Img(src=pil_seta, style={'position': 'relative', 'width': '1.5vw', 'height': '3vh', 'left': '93vw', 'top': '-200.5vh'}),        
                ]
        ),

    ], style={'width': '80%', 'height': '0'}
)