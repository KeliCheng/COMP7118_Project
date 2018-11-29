import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State




current_user = None
current_movie = None

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True