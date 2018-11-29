import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input
import numpy as np
import random
import pandas as pd 
import sys
app = dash.Dash()
def reading_file():
        f1=pd.read_csv("ratings.csv")
        f2=pd.read_csv("movies.csv")#,encoding="utf8")
        user_id_moviemap={}
        movieid_ratmap={}
        user=[]
        movieid=[]
        mid=[]
        ttl=[]
        str2=[]
        mname={}
        rating=[]
        uniq_user=[]
        duser={}
        dmv={}
        tzone=[]
        mrt={}
        mnn=[]
        d={}
        for tt in f2.movieId:
            mid.append(tt)
        for tt in f2.title:
            ttl.append(tt)
        for kk in range(0,len(ttl)):
            mname[mid[kk]]=ttl[kk]
            mnn.append(ttl[kk])
        for tt in f1.movieId:
            movieid.append(tt)
        for tt in f1.userId:
            user.append(tt)
        for tt in f1.rating:
            rating.append(tt)
        app.layout=html.Div([
        html.H1("Enter the rating of the movie"),
         dcc.Dropdown(id='dropdown1',options=[{'label': i, 'value': i} for i in mnn],placeholder="Select a Movie",),
         dcc.Dropdown( value=['0'], options=[{'label': i, 'value': i} for i in ['5', '4', '3', '2','1','1.5','2.5','3.5','4.5']],
                    multi=False,id='dropdown'),
             html.H3(id='output')])
        @app.callback(Output('output', 'children'), [Input('dropdown1', 'value'),Input('dropdown', 'value')])
        def display_output(value1,value2):
            d[str(value1)]=str(value2)
            return "The Raing of the movie: "+str(value1)+" given by the new user is"+"::"+str(value2)
        
        return d

dd=reading_file()

print(dd)
if __name__ == '__main__':
             app.run_server(debug=True)



        