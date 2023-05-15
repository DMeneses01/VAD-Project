import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os
import pandas as pd
import plotly.graph_objects as go
from raceplotly.plots import barplot

import PIL

image_path = os.path.abspath('pages/components/olympic-rings.png')
pil_rings = PIL.Image.open(image_path)

image_path = os.path.abspath('pages/components/round-chevron-right.png')
pil_seta = PIL.Image.open(image_path)

image_path = os.path.abspath('pages/components/button.png')
pil_button = PIL.Image.open(image_path)

Path = os.getcwd()
mVSw = pd.read_csv(os.path.join(Path, 'Dataframes','menVSwomen.csv'))

topMedals = pd.read_csv(os.path.join(Path, 'Dataframes','topMedals_sport.csv'))

raceplot = pd.read_csv(os.path.join(Path, 'Dataframes','raceplot.csv'))

sport = mVSw['sport'].drop_duplicates().sort_values()


dash.register_page(__name__, path='/by_sport')

layout = html.Div(
    [
	    
        html.Div(children = [
            dcc.Dropdown(id="dropdown",
            options=[ {'label': x, 'value': x}
                    for x in sport
            ],
                value='Athletics',
                clearable=False,
                style={'width': '18vw', 'height':'3vh', 'fontSize':'2.5vh','top':'1vh'}
            ),

        ],  style= {'position':'absolute', 'fontFamily': 'Cabin', 'top':'11vh', 'left':'3.5vw'}),

        
        html.Div(children=[
             html.Div(children = [
                    dcc.Graph(id="g3", style={'position': 'absolute', 'left': '3vw', 'top': '5vh', 'width': '65vw','height': '65vh'}),
                    html.H4('Country Race', style={'position': 'absolute', 'left': '3.5vw', 'position': 'absolute', 'fontSize': '25px', 'fontFamily': 'Cabin', 'width': '30vw','height': '5vh', 'left':'27vw', 'background': '#FFFFFF'}),
            ])
           
        ], style = {'position': 'absolute', 'width': '68.5vw','height': '75vh', 'left': '26vw', 'top': '11vh', 'background': '#FFFFFF', 'borderRadius': '12px 12px 12px 12px', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)'}),


        html.Div([
            dcc.Graph(id="g2", style={'position': 'absolute','top':' 1.5vh', 'left':'0.5vw',  'width':'17vw', 'height':'64vh'})

        ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'position': 'absolute',
                        'width': '18vw', 'height': '66.5vh', 'left': '3.5vw', 'top': '19.5vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
        

        html.Div([
           dcc.Graph(id="g1", style={'position':'absolute', 'top':' 1.5vh', 'left':'0.5vw',  'width':'90vw', 'height':'35vh'})
        ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 
            'position': 'absolute', 'width': '91.1vw', 'height': '38vh', 'left': '3.5vw', 'top':' 90vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'}),
        
        html.Div([
                html.H1("By sport", style= {'position': 'absolute', 'width': '10vw', 'height': '5vh', 'left': '89vw', 'top': '2vh', 'fontFamily': 'Cabin', 'fontSize':'2.5vh'}),
                
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
    Output("g1", "figure"),
    Output("g2", "figure"),
    Output("g3", "figure"),
    Input("dropdown", "value"))
def sports_callback(sports):

    ## Men vs Women

    years = mVSw["edition"].unique()

    year = []
    gender = []
    count = []

    for y in years:
        year.append(y)
        year.append(y)

        gender.append("Female")
        gender.append("Male")
        

        female = len(mVSw[(mVSw['edition'] == y) & (mVSw['sex'] == 'Female') & (mVSw["sport"] == sports)])
        male = len(mVSw[(mVSw['edition'] == y) & (mVSw['sex'] == 'Male') & (mVSw["sport"] == sports)])

        count.append(female)
        count.append(male)

    df = pd.DataFrame()
    df["year"] = year
    df["gender"] = gender
    df["count"] = count

    df_male = df[df.gender == 'Male']
    df_female = df[df.gender == 'Female']

    df_female['count'] = - df_female['count']

    fig1 = go.Figure()

    fig1.add_trace(go.Bar(
        x = df_female.year,
        y = df_female["count"],
        name = 'Female',

        marker_color='#FCB131'
    ))

    fig1.add_trace(go.Bar(
            x = df_male.year,
            y = df_male["count"],
            name = 'Male',

            marker_color='#00A651'
    ))

    fig1.update_layout(xaxis=dict(tickformat='(.0f'), barmode = 'relative',
                       font_family= 'Cabin',autosize = False, 
                    title={
                        'text': "<b>Men vs Women evolution</b>",
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'x':0.5,
                        'y':1}, 
                      legend=dict(yanchor="top", xanchor="left", font=dict(size=15)),
                      margin=dict(l=1, r=2, b=20, t=31, pad=0))
    
    ## Top Medals by Country in the sport
    athleter = topMedals[topMedals['sport'] == sports].reset_index()

    athlete_aux = athleter.copy()

    athleter['medal'] = athleter['medal'].replace([None], 0)
    athleter['medal'] = athleter['medal'].replace(['Gold'], 1)
    athleter['medal'] = athleter['medal'].replace(['Silver'], 1)
    athleter['medal'] = athleter['medal'].replace(['Bronze'], 1)

    athleter = athleter.drop(columns=['edition_id','sport','event','isTeamSport'])

    medals = pd.DataFrame(athleter.groupby(['country_noc']).sum()).reset_index().sort_values(by=['medal'], ascending=False).head(10)

    athlete_aux = athlete_aux[athlete_aux['country_noc'].isin(medals['country_noc'])]

    medals = pd.DataFrame(athlete_aux.groupby(['country_noc' , 'medal']).count()).reset_index()
    medals.drop(columns=['edition_id','sport','event','isTeamSport'], inplace=True)
    medals.rename(columns={'edition': 'count', 'country_noc': 'country'}, inplace=True)

    fig2 = go.Figure()

    fig2 = px.bar(medals, x="country", y="count", color='medal', 
            color_discrete_map={
                'Gold': '#D6AF36',
                'Silver': '#A7A7AD',
                'Bronze': '#A77044'}, 
            title="Top Medals by Country in the sport")
    fig2.update_xaxes(categoryorder="total descending")
    fig2.update_layout(font_family= 'Cabin', margin=dict(l=1, r=2, b=20, t=31, pad=0))

    ## Raceplot

    athlete_r = raceplot[raceplot['sport'] == sports]

    df = pd.DataFrame(athlete_r.groupby(['edition','country_noc']).sum()).reset_index()

    # Create a MultiIndex with all possible combinations of edition and country_noc
    index = pd.MultiIndex.from_product([df['edition'].unique(), df['country_noc'].unique()], names=['edition', 'country_noc'])

    # Reindex the DataFrame with the new MultiIndex and fill missing values with 0
    df = df.set_index(['edition', 'country_noc']).reindex(index, fill_value=0).reset_index()

    df['edition'] = df['edition'].astype(int)
    df['medal'] = df['medal'].astype(int)

    # Sort the DataFrame by edition and country_noc
    df = df.sort_values(['edition', 'country_noc'])

    # Group the DataFrame by country_noc and calculate the cumulative sum of the medal column
    df['new_medal'] = df.groupby('country_noc')['medal'].cumsum()
    
    my_raceplot = barplot(df, item_column='country_noc', value_column='new_medal', time_column='edition')

    my_raceplot.plot(item_label = 'Top 10 countries', value_label = 'Amount of Medals', time_label='Year ', frame_duration = 800)
    
    return fig1, fig2, my_raceplot.fig