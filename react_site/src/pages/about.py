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

dash.register_page(__name__, path='/about')

layout = html.Div(
    [ 
        html.Div([
                html.H1("About", style= {'position': 'relative', 'width': '10vw', 'height': '5vh', 'left': '89vw', 'top': '1vh', 'fontFamily': 'Cabin', 'fontSize':'2.5vh'}),
                
                html.H1('The Olympics under a magnifying glass', style={'position': 'relative', 'width': '30vw', 'height': '3.22vh', 'left': '4vw', 'top': '-6vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                html.Div([
                        html.A(html.Img(src=pil_rings, style={'position': 'relative', 'width': '3vw', 'height': '3.5vh', 'left': '0.5vw', 'top': '-11.5vh'}), href='/'),
                        dcc.Location(id='url', refresh=False),  
                ]),      
        ]),

        html.Div([
            html.H2('We intend to provide the countries competing in the Olympic Games with the means of analyzing their results over the years, through the visualization of information. In this way, any state can identify which sports it does not present such positive results or with less evolution and, thus, direct its attention to improving its performance in those events.'),
            html.H2('On the other hand, by identifying the sports in which a nation is not so good, we are also able to know those in which it is better. In this way, our work also becomes useful to the bettors: by knowing which countries do better in each event, they can have more confidence in their bets.'),
            html.H2('We had at our disposal a vast dataset with information from the Olympics since 1896. Over time, some nations have ceased to exist, others have joined and others have split. With this, we chose to do the following (entity - decision - reason):'),
            html.H2('➜ Mixed Team - Ignore data - Impossible to attribute the medals to a specific country'),
            html.H2('➜ Unified Team - Ignore data - Unable to give medals to a specific country'),
            html.H2('➜ Individual Olympic Athletes - Ignore data - Unable to allocate medals to a specific country'),
            html.H2('➜ Bohemia - Ignore data - Split into several countries'),
            html.H2('➜ Australasia - Ignore data - Divided into several countries'),
            html.H2('➜ Czechoslovakia - Data Ignore - Split into several countries'),
            html.H2('➜ Yugoslavia - Data Ignore - Split into several countries'),
            html.H2('➜ Soviet Union - Data Ignore - Divided into several countries'),
            html.H2('➜ United Arab Republic - Data Ignore - Divided into several countries'),
            html.H2('➜ Federation of West Indies - Data Ignore - Divided into several countries'),
            html.H2('➜ Federal Republic of Germany - Add data from Germany - Union of nations'),
            html.H2('➜ Germany - Join data with Germany - Union of Nations'),
            html.H2('➜ Hong Kong - Join data with China - Hong Kong and a region of China'),
            html.H2('➜ Russian Olympic Comite - Add data from Russia - The athletes are Russian'),
        
        ], style={'position': 'relative', 'width': '93vw', 'height': '50vh','fontFamily': 'Cabin', 'left':'2vw', 'top':'-5vh'}),

        
    ]
)