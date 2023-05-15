import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash

Path = os.getcwd()
athlete_Bio = pd.read_csv('../Dataset/Olympic_Athlete_Bio.csv', sep=',')

athlete_Bio = athlete_Bio.replace(["na"], None)
athlete_Bio["height"] = athlete_Bio["height"].astype(float)

athlete_Event_Results = pd.read_csv('../Dataset/Olympic_Athlete_Event_Results.csv', sep=',')
athlete_Event_Results = athlete_Event_Results.replace(["na"], None)

athlete_Event_Results = athlete_Event_Results[athlete_Event_Results["edition"].str.contains("Winter") == False]

athlete_Event_Results['country_noc'] = athlete_Event_Results['country_noc'].replace(['FRG'], 'GER')
athlete_Event_Results['country_noc'] = athlete_Event_Results['country_noc'].replace(['GDR'], 'GER')

athlete_Event_Results['country_noc'] = athlete_Event_Results['country_noc'].replace(['HKG'], 'CHN')

athlete_Event_Results['country_noc'] = athlete_Event_Results['country_noc'].replace(['ROC'], 'RUS')

athlete_Bio.drop(columns=['name', 'born', 'height', 'weight', 'country', 'country_noc', 'description', 'special_notes'], inplace=True)
athlete_Event_Results.drop(columns=['edition_id', 'country_noc', 'result_id', 'pos', 'medal', 'isTeamSport'], inplace=True)

df_aux = pd.merge(athlete_Bio, athlete_Event_Results, on='athlete_id')

df_aux['edition'] = df_aux['edition'].str.split().str[0].astype(int)

df_aux.to_csv('../react_site/src/Dataframes/menVSwomen.csv', index=False)


sport = df_aux["sport"].drop_duplicates().sort_values()


app = Dash(__name__)

app.layout = html.Div(style={'font-family': 'Cabin'}, children = [
    dcc.Dropdown(id="dropdown",
            options=[ {'label': x, 'value': x}
                    for x in sport
        ],
            value='Atheletics',
            clearable=False,
        ),
    dcc.Graph(id="graph"),
])

@app.callback(
Output("graph", "figure"),
[Input("dropdown", "value")])
def medals_type(sport):

    
    years = df_aux["edition"].unique()

    year = []
    gender = []
    count = []

    for y in years:
        year.append(y)
        year.append(y)

        gender.append("Female")
        gender.append("Male")
        

        female = len(df_aux[(df_aux['edition'] == y) & (df_aux['sex'] == 'Female') & (df_aux["sport"] == sport)])
        male = len(df_aux[(df_aux['edition'] == y) & (df_aux['sex'] == 'Male') & (df_aux["sport"] == sport)])

        count.append(female)
        count.append(male)

    df = pd.DataFrame()
    df["year"] = year
    df["gender"] = gender
    df["count"] = count

    df_male = df[df.gender == 'Male']
    df_female = df[df.gender == 'Female']

    df_female['count'] = - df_female['count']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = df_female.year,
        y = df_female["count"],
        name = 'Female',

        marker_color='#EE334E'
    ))

    fig.add_trace(go.Bar(
            x = df_male.year,
            y = df_male["count"],
            name = 'Male',

            marker_color='#0081C8'
    ))


    fig.update_layout(xaxis=dict(tickformat='(.0f'), barmode = 'relative', font_family= 'Cabin',autosize = False, 
                      yaxis_title="count", xaxis_title="year",
                      title={
                        'text': "<b>Females vs Males</b>",
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'x':0.5},
                      paper_bgcolor="white",
                      plot_bgcolor="white",
                      legend=dict(yanchor="top", xanchor="left", font=dict(size=15)),
                      margin=dict(l=1, r=2, b=20, t=31, pad=0))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
