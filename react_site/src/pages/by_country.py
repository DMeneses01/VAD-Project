import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os
import pandas as pd
import plotly.graph_objects as go

import PIL

image_path = os.path.abspath('pages/components/olympic-rings.png')
pil_rings = PIL.Image.open(image_path)

image_path = os.path.abspath('pages/components/round-chevron-right.png')
pil_seta = PIL.Image.open(image_path)

image_path = os.path.abspath('pages/components/button.png')
pil_button = PIL.Image.open(image_path)

Path = os.getcwd()
medals = pd.read_csv(os.path.join(Path,'Dataframes','medals_country.csv'))

top_sports = pd.read_csv(os.path.join(Path, 'Dataframes','top5_sports_country.csv'))

with_without = pd.read_csv(os.path.join(Path, 'Dataframes','with_without_country.csv'))

countries = medals['country'].drop_duplicates().sort_values()

colors = ['#D6AF36', '#A7A7AD', '#A77044']
color = ['#0081C8', '#FCB131', '#000000', '#00A651', '#EE334E']
colorsw = ['#EE334E', '#0081C8']

dash.register_page(__name__, path='/by_country')

layout = html.Div(
    [
	    
        html.Div(children = [
            dcc.Dropdown(id="dropdown",
                options=[ {'label': x, 'value': x}
                        for x in countries
            ],
                value='Portugal',
                clearable=False,
                style={'width': '18vw', 'height':'3vh', 'fontSize':'2.5vh'}
            ),
        ],  style= {'position':'absolute', 'fontFamily': 'Cabin', 'top':'11vh', 'left':'3.5vw'}),

        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id="graph"),
                dcc.Checklist(
                    id='checklist',
                    options=[],
                    value=['Athletics'],
                    inline=True
                ) ], 
            style={'backgroundColor': '#EEF1FA', 'fontFamily': 'Cabin', 'left':'0.5vw'})   
        ], style = {'position': 'absolute', 'width': '68.5vw','height': '75vh', 'left': '26vw', 'top': '11vh', 'background': '#EEF1FA', 'borderRadius': '12px 12px 12px 12px', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)'}),
		

        html.Div([
            dcc.Graph(id="graph1", style={'position': 'absolute','top':' 1vh', 'left':'0.1vw', 'width':'17.5vw', 'height':'23vh'})
        
        ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 
            'position': 'absolute', 'width': '18vw', 'height': '24.5vh', 'left': '3.5vw', 'top':' 19.5vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
        
        html.Div([
            dcc.Graph(id="graph2", style={'position': 'absolute','top':' 3vh', 'left':'0.1vw',  'width':'17.5vw', 'height':'34vh'})
        
        ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 
            'position': 'absolute', 'width': '18vw', 'height': '38vh', 'left': '3.5vw', 'top':' 48vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
        
        html.Div([
           dcc.Graph(id="graph3", style={'position': 'absolute','top':' 1vh', 'left':'0.5vw', 'width':'90vw', 'height':'35vh'})
        ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 
            'position': 'absolute', 'width': '91.1vw', 'height': '38vh', 'left': '3.5vw', 'top':' 90vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
        
	
        html.Div([
                html.H1("By country", style= {'position': 'absolute', 'width': '10vw', 'height': '5vh', 'left': '89vw', 'top': '2vh', 'fontFamily': 'Cabin', 'fontSize':'2.5vh'}),
                
                html.H1('Jogos Olímpicos à Lupa', style={'position': 'absolute', 'width': '30vw', 'height': '3.22vh', 'left': '4vw', 'top': '2vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                
                html.Div(
                    [
                        html.A(html.Img(src=pil_button, style={'position': 'absolute', 'width': '2vw', 'height': '3.5vh', 'left': '1vw', 'top': '4vh', 'rotate': '180deg', 'background': '#000000', 'borderRadius': '7px', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)'}), href='/dashboard'),
                        dcc.Location(id='url', refresh=False),
                      
                    ]
                
                ),


                html.Img(src=pil_rings, style={'position': 'absolute', 'width': '3vw', 'height': '3.5vh', 'left': '19.5vw', 'top': '4vh'}),        
            
        ]),
                    
        html.Div(
            style={
                'backgroundColor': '#F6F7FB',
                'height': '127.5vh'}
		)
    ]
)

@callback(
Output("graph1", "figure"),
Output("graph2", "figure"),
Output("graph3", "figure"),
Output("checklist", "options"),
Output("graph", "figure"),
Input("dropdown", "value"),
Input("checklist", "value"))
def medals_type(country, sports):

    ## Medals

    goldv = medals.loc[(medals['country'] == country), 'gold'].values[0]
    silverv = medals.loc[(medals['country'] == country), 'silver'].values[0]
    bronzev = medals.loc[(medals['country'] == country), 'bronze'].values[0]

    fig1 = go.Figure(data=[go.Pie(labels=['Gold','Silver','Bronze'],
                                values=[goldv,silverv,bronzev])])                       
    fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    fig1.update_layout(font_family= 'Cabin',autosize = False, 
                      legend=dict(yanchor="top", xanchor="left", font=dict(size=15)),
                      margin=dict(l=2, r=2, b=20, t=31, pad=0),
                      title={
                        'text': "<b>Medals</b>",
                        'y':0.9,
                        'x':0.15,
                        'xanchor': 'center',
                        'yanchor': 'top'})
    
    ## Top 5 sports

    dataset = top_sports[top_sports['country'] == country].reset_index()

    new_medal = []
    for i in range(len(dataset)):
        edition = dataset.loc[i, 'edition']
        sport = dataset.loc[i, 'sport']
        event = dataset.loc[i, 'event']

        new_medal.append(dataset[(dataset['edition'] <= edition) & (dataset['sport'] == sport) & (dataset['event'] == event)]['medal'].sum())

    dataset['medal'] = new_medal

    dataset2 = dataset.copy()

    dataset2 = pd.DataFrame(dataset2.groupby(['sport']).sum()).reset_index()

    dataset2 = dataset2.sort_values(by=['medal'], ascending=False).head(5)

    dataset2['color'] = color

    fig2 = px.bar(dataset2, x="sport", y="medal", color= 'color', title="Top 5 sports for the country",
                color_discrete_sequence=['#0081C8', '#FCB131', '#000000', '#00A651', '#EE334E'] )
    fig2.update_layout(font_family= 'Cabin',autosize = False, 
                        legend=dict(yanchor="top", xanchor="left", font=dict(size=15)),
                        margin=dict(l=1, r=6, b=20, t=31, pad=0), showlegend=False)
    
    ## With Without

    country_df = with_without[with_without["country"] == country]

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

    fig3 = go.Figure()

    fig3.add_trace(go.Bar(
            y = df_with["count"],
            x = df_with.year,
            name = 'With',
            
            marker_color=colorsw[0]
    ))

    fig3.add_trace(go.Bar(
            y = df_without["count"],
            x = df_without.year,
            name = 'Without',
            
            marker_color=colorsw[1]
    ))

    fig3.update_layout(xaxis=dict(tickformat='(.0f'), barmode = 'relative', font_family= 'Cabin',
                      yaxis_title="count", xaxis_title="year",
                      title={
                        'text': "<b>Medals vs Participations</b>",
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'x':0.5},
                      paper_bgcolor="white",
                      plot_bgcolor="white", autosize = False,
                      legend=dict(yanchor="top", xanchor="left", font=dict(size=15)), 
                      margin=dict(l=1, r=2, b=20, t=31, pad=0))
    
    ## Line Chart
    fig = go.Figure()

    df = dataset#px.data.gapminder()
    mask = df.sport.isin(sports)
    fig = px.line(df[mask], 
        x="edition", y="medal", color='event').update_layout({
                                                    'plot_bgcolor': '#FFFFFF',
                                                    'paper_bgcolor': '#EEF1FA'
                                                    }, font_family= 'Cabin'
                                                    )
    fig.update_xaxes(showline=True, linewidth=2, gridcolor='#c7c7c7')
    fig.update_yaxes(showline=True, linewidth=2, gridcolor='#c7c7c7')
    fig.update_layout( title={
                        'text': "Sports evolution of " + country,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'x':0.5,
                        'font': dict(size=20)
                       })

    

    return fig1, fig2, fig3,[{'label': x, 'value': x} for x in pd.unique(dataset.sport)], fig