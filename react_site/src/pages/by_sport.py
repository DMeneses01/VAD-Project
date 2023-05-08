import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os


dash.register_page(__name__, path='/by_sport')

layout = html.Div()