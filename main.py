import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from recommend import *
from user import User


current_user = None
current_movie = None

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True


def genre_dropdown():
    opt = []
    for g in genres:
        opt.append({'label': g, 'value': g})

    return dcc.Dropdown(
                    id='genre-dropdown',
                    options=opt,
                    placeholder="Select your favorite genres",
                    multi=True
                    )

def user_dropdown():
    opt = []
    for u in users:
        opt.append({'label': u, 'value': u})

    return dcc.Dropdown(
                    id='user-dropdown',
                    options=opt,
                    placeholder="Select your ID",
                    )

def opinion_opts():
    return dcc.RadioItems(
        id='opinion-radio',
        options=[
            {'label': 'Watched', 'value': 'Watched'},
            {'label': 'Interested', 'value': 'Interested'},
            {'label': 'Not Interested', 'value': 'Not Interested'},

        ],
        value='Interested',
        labelStyle={'display': 'inline-block'},
        style = {'padding-left': '2px'}
    )

def rating_opts():
    opts = []
    for r in range(1, 6):
        opts.append( {'label': r, 'value': r} )

    return dcc.RadioItems(
        id = 'rating-radio',
        options = opts,
        value = opts[0]['value'],
        labelStyle = {'display' : 'inline-block'},
        style = {'padding-left': '2px'}
    )

# =======================================================================================

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('New User', href='/new'),
    html.Br(),
    dcc.Link('Existing User', href='/existing'),
    # html.Button('New User', id='button'),


    # content will be rendered in this element
    html.Div(id='page-content'),
    ])


# =======================================================================================

@app.callback(Output('page-content', 'children'),
  [Input('url', 'pathname')])

def display_page(pathname):
    global current_user

    if pathname == '/new': # new user
        current_user = User(len(users)+1)
        return html.Div([html.H5('Welcome, User #' + str(current_user.u_id)),
            html.Div([
                html.Div([ genre_dropdown(), html.Br()], id='new-content1'),
                html.Div(id='new-content2'),
                html.Div(id='new-content3'),

                html.Button(id='submit-button', n_clicks=0, children='Submit')]),
                ], style={'padding-left':'10%', 'padding-right':'10%'})

    elif pathname == '/existing': # existing user
        return html.Div([
            # html.H3('You are on page {}'.format(pathname))
            # html.H3('existing')
            html.H6('Select your ID: '),
            html.Div([
                user_dropdown(),
                html.Div(id='output-container2')
                ])

            ], style={'padding-left':'10%', 'padding-right':'10%'})
    else:
        return

# =======================================================================================
# Callback of new user's selection
'''
@app.callback(
    Output('new-content1', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('genre-dropdown', 'value'), State('opinion-radio', 'value'), State('rating-radio', 'value')])
def update_output(n_clicks, g, o, r):
    global current_movie

    print(g, o, r)

    if n_clicks == 1:

        m, title  = first_recomm(value)
        current_movie = m

         return [html.H5('Recommendation: '), html.H6(title), genre_dropdown(),
         opinion_opts(), rating_opts()]

     else:
         if o == "Interested":
             return [html.H5('Interested'), genre_dropdown(),
             opinion_opts(), rating_opts()]
         elif o == "Not Interested":
             return [html.H5('Not Interested'), genre_dropdown(),
             opinion_opts(), rating_opts()]
         else:
             return [html.H5('Give a rate'), genre_dropdown(),
             opinion_opts(), rating_opts()]
'''


@app.callback(
    Output('new-content1', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('genre-dropdown', 'value')])

def update_output(n_clicks, value):
    global current_movie
    m, title  = first_recomm(value)
    current_movie = m

    return [html.H5('Recommendation: '), html.H6(title),
    opinion_opts()]

    # return html.Div(, style={'display': 'none'})


# =======================================================================================
# Callback of opinion radios
@app.callback(
    Output('new-content2', 'children'),
    [Input('opinion-button', 'n_clicks')],
    [State('opinion-radio', 'value')])


def update_output(n_clicks, value):
    global current_user

    if n_clicks > 0:
        if value == 'Interested':
            current_user.whitelist.append(current_movie)
            print(current_user.whitelist)


            return 'Interested'
        elif value == 'Not Interested':
            current_user.blacklist.append(current_movie)

            return 'Not'
        else:
            return

# =======================================================================================
# Showing rating options
@app.callback(
    Output('new-content3', 'children'),
    [Input('opinion-radio', 'value')])

def update_output(value):
    if value == 'Watched':
        return [rating_opts(),]
        # html.Button(id='opinion-button', n_clicks=0, children='Submit')]
    else:
        # return [html.Button(id='opinion-button', n_clicks=0, children='Next')]
        return

# =======================================================================================
# Callback of existing user's selection
@app.callback(
    Output('output-container2', 'children'),
    [Input('user-dropdown', 'value')])
def update_output(value):
    v, m = get_recommendation(value)
    return [html.H5('Your most similar user: '), html.H6(v),
    html.H5('Recommendation based on your ratings: '), html.H6(m),
    opinion_opts(),
    html.Button(id='existing-submit', n_clicks=0, children='Submit')]
    # return 'You have selected "{}"'.format(value)





if __name__ == '__main__':
    app.run_server(debug=True)


