import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os


dash.register_page(__name__, path='/') 

layout = html.Div(
    [
        html.H1('Advanced Data Visualization', 
	            style = {'position': 'absolute', 'width':' 16.04vw', 'height': '8.33vh', 'left': '4vw', 'top': '2vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '700', 'fontSize': '3.5vh', 'lineHeight': '4.5vh',
                            'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em',
                            'color': '#000000', 'backgroundColor': '#F6F7FB'}),
			    
        html.Div([
                    #html.Img(src=pil__rings,  
                            #style={'position': 'absolute', 'left': '26.39vw', 'top': '25vh', 'width': '30%', 'height': '30%'}),
                    html.H1('Jogos Olímpicos à lupa', 
			                style={'position': 'absolute', 'width': '60vw', 'height': '9.33vh', 'left': '13vw', 'top': '55vh',
                                    'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '700', 'fontSize': '10vh', 'lineHeight': '10vh', 
				                    'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em', 'color': '#000000'} )
                    ], 
                    style = {'position': 'absolute', 'width': '72vw','height': '88vh', 'left': '26vw', 'top': '11vh', 'background': '#EEF1FA', 'borderRadius': '14vh 0vh 0vh 14vh'}),
		html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(
                                    f"{'Next'}", href=page["relative_path"]
                                ), style={'position': 'absolute', 'width': '3vw', 'height':'6.5vh', 'left': '3vw', 'top':'-0.9vh',
                                        'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '500', 'fontSize': '2.6vh',
                                        'lineHeight': '1.89vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em'}
                            )
                            for page in dash.page_registry.values()
                            if page["path"] == "/dashboard"
                        ], style= {'position': 'absolute', 'width': '10vw', 'height': '5vh', 'left': '7.5vw', 'top': '90vh',
                                    'background': '#FFFFFF', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'borderRadius': '7px'}
				    ), 
				    #html.Img(src='/assets/round-chevron-right.svg')     
                ]
        ),
	
        html.Div([
                html.H1('Authors', style={'position': 'absolute', 'width': '4.86vw', 'height': '3.22vh', 'left': '9.5vw', 'top': '15vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                html.Div([
                    html.H1('Made by', style={'position': 'absolute', 'height': '2vh', 'left': '1vw','top': '2vh', 'fontSize': '2.6vh', 'lineHeight': '1.89vh'}),
                    html.H2('Duarte Meneses', style={'width': '20vw', 'top': '6vh', 'fontSize': '2.5vh', 'position': 'absolute', 'height': '2vh', 'left':' 1vw', 'lineHeight': '1.67vh'}),
                    html.H2('Patricia Costa', style={'width': '20vw', 'top': '10vh', 'fontSize': '2.5vh', 'position': 'absolute', 'height': '2vh', 'left':' 1vw', 'lineHeight': '1.67vh'}),
			        
                    html.H2('2019216949', style={'width': '20vw', 'top': '6vh', 'fontSize': '2.5vh', 'position': 'absolute', 'height': '2vh', 'left': '10vw', 'lineHeight': '1.67vh'}),
                    html.H2('2019213995', style={'width': '20vw', 'top': '10vh', 'fontSize': '2.5vh', 'position': 'absolute', 'height': '2vh', 'left': '10vw', 'lineHeight': '1.67vh'}),
			        html.H2('2022/2023', style={'left':'6vw', 'width': '20vw', 'top': '15vh', 'fontSize': '2.5vh', 'position': 'absolute', 'height': '5vh', 'left': '6vw', 'lineHeight': '1.67vh'})
                
                ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 
			        'position': 'absolute', 'width': '18vw', 'height': '20vh', 'left': '3.5vw', 'top':' 23vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
                html.Div([
                    html.Img(src='../components/git.png', style={'position': 'absolute', 'width': '3vw', 'height': '6.5vh', 'left': '4vw', 'top': '10vh'}),
                    html.H2('GitHub', style={'position':'absolute', 'width': '20vw', 'height': '2vh', 'left': '8vw', 'top': '12.5vh', 'fontSize': '2.6vh'}),
                    html.A('@DMeneses01', href='https://github.com/DMeneses01', style={'position':'absolute','width': '20vw', 'height': '2vh', 'left': '5vw', 'top': '21vh'}),
                    html.A('@patii01', href='https://github.com/patii01', style={'position':'absolute','width': '20vw', 'height': '2vh', 'left': '7vw', 'top': '27vh'})
                ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 'position': 'absolute',
                        'width': '18vw', 'height': '35vh', 'left': '3.5vw', 'top': '50vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
            ]),
                    
        html.Div(
            style={
                'backgroundColor': '#F6F7FB',
                'height': '98vh'}
		)
    ]
)