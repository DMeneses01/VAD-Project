import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os
import pandas as pd

import PIL

image_path = os.path.abspath('react_site/src/pages/components/olympic-rings.png')
pil_rings = PIL.Image.open(image_path)

image_path = os.path.abspath('react_site/src/pages/components/round-chevron-right.png')
pil_seta = PIL.Image.open(image_path)

Path = os.getcwd()
medals = pd.read_csv(os.path.join(Path, 'react_site', 'src', 'Dataframes','medals_country.csv'))

countries = medals['country'].drop_duplicates().sort_values()

colors = ['#D6AF36', '#A7A7AD', '#A77044']

dash.register_page(__name__, path='/by_country')

layout = html.Div(
    [
	    
        html.Div(children=[
                
        ], style = {'position': 'absolute', 'width': '72vw','height': '88vh', 'left': '26vw', 'top': '11vh', 'background': '#EEF1FA', 'borderRadius': '12px 0vh 0vh 12px'}),
		
        html.Div(children = [
            dcc.Dropdown(id="dropdown",
                options=[ {'label': x, 'value': x}
                        for x in countries
            ],
                value='Portugal',
                clearable=False,
                style={'width': '50%'}
            ),
            html.H4('Top 10 Medals by Country'),
            #dcc.Graph(id="graph")
        ],  style= {'fontFamily': 'Cabin'}),
	
        html.Div([
                html.H1("By country", style= {'position': 'absolute', 'width': '10vw', 'height': '5vh', 'left': '89vw', 'top': '2vh', 'fontFamily': 'Cabin', 'fontSize':'2.5vh'}),
                
                html.H1('Jogos Olímpicos à Lupa', style={'position': 'absolute', 'width': '30vw', 'height': '3.22vh', 'left': '4vw', 'top': '2vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                
                html.Div(
                    [
                        html.A(html.Img(src=pil_seta, style={'position': 'absolute', 'width': '2vw', 'height': '3.5vh', 'left': '1vw', 'top': '3.7vh', 'rotate': '180deg'}), href='/'),
                        dcc.Location(id='url', refresh=False),
                      
                    ] 
                      
                ),

                html.Img(src=pil_rings, style={'position': 'absolute', 'width': '3vw', 'height': '3.5vh', 'left': '19.5vw', 'top': '4vh'}),        
            
        ]),
                    
        html.Div(
            style={
                'backgroundColor': '#F6F7FB',
                'height': '98vh'}
		)
    ]
)