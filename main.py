import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from movie_imdb_info import *
from recommend import *
from user import User


current_user = None
current_movie = None
cycled_movies = []
num_watched = 0
user_rec_thresh = 3
liked = []
disliked = []
glob_genres = []

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True


def genre_dropdown(hidden=False):
    opt = []
    for g in genres:
        opt.append({'label': g, 'value': g})

    if hidden:
        return dcc.Dropdown(
                        id='genre-dropdown',
                        options=opt,
                        placeholder="Select your favorite genres",
                        multi=True,
                        style={'display': 'none'}
                        )

    return dcc.Dropdown(
                    id='genre-dropdown',
                    options=opt,
                    placeholder="Select your favorite genres",
                    multi=True
                    )


def opinion_opts(hidden=False):
    if hidden:
        return dcc.RadioItems(
        id='opinion-radio',
        options=[
            {'label': 'Watched', 'value': 'Watched'},
            {'label': 'Interested', 'value': 'Interested'},
            {'label': 'Not Interested', 'value': 'Not Interested'},

        ],
        value='Interested',
        labelStyle={'display': 'inline-block'},
        style = {'display': 'none'}
    )
    else:
        return dcc.RadioItems(
            id='opinion-radio',
            options=[
                #{'label': 'Watched', 'value': 'Watched'},
                {'label': 'Interested', 'value': 'Interested'},
                {'label': 'Not Interested', 'value': 'Not Interested'},

            ],
            value='Interested',
            labelStyle={'display': 'inline-block'},
            style = {'padding-left': '2px'}
        )

def rating_opts(hidden=False):
    opts = []
    for r in range(1, 6):
        opts.append( {'label': r, 'value': r} )

    if hidden:
        return dcc.RadioItems(
            id='rating-radio',
            options=opts,
            value=opts[0]['value'],
            labelStyle={'display': 'inline-block'},
            style={'display': 'none'}
        )
    else:
        return dcc.RadioItems(
        id = 'rating-radio',
        options = opts,
        value = opts[0]['value'],
        labelStyle = {'display' : 'inline-block'},
        style = {'padding-left': '2px'}
    )

def user_dropdown(hidden=False):
    opt = []
    for u in userColumns:
        opt.append({'label': u, 'value': u})

    if hidden:
        return dcc.Dropdown(
                id='user-dropdown',
                options=opt,
                placeholder="Select your ID",
                style={'display': 'none'}
                )

    return dcc.Dropdown(
            id='user-dropdown',
            options=opt,
            placeholder="Select your ID",
            )

def like_dropdown():
    opt = []

    for index,m in movies_df.iterrows():
        opt.append({'label': m['title'], 'value': m['movieId']})

    return dcc.Dropdown(
        id='like_dropdown',
        options=opt,
        placeholder="Select movies you like",
        multi=True,
    )

def dislike_dropdown():
    opt = []

    for index,m in movies_df.iterrows():
        opt.append({'label': m['title'], 'value': m['movieId']})

    return dcc.Dropdown(
        id='dislike_dropdown',
        options=opt,
        placeholder="Select movies you dislike",
        multi=True,
    )

# =======================================================================================

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('New User', href='/new'),
    html.Br(),
    dcc.Link('Existing User', href='/existing'),
    html.Br(),
    dcc.Link('Movie Recommender', href='/recommender'),
    # html.Button('New User', id='button'),


    # content will be rendered in this element
    html.Div(id='page-content'),
    ])


# =======================================================================================

@app.callback(Output('page-content', 'children'),
  [Input('url', 'pathname')])

def display_page(pathname):
    global current_user

    cycled_movies = []
    liked = []
    disliked = []

    if pathname == '/new': # new user
        current_user = User(1) #User(users[-1]+1)  # create user and set u_id

        return html.Div([html.H5('Welcome, User #' + str(current_user.u_id)),
            html.Div([
                html.Div([ genre_dropdown(), html.Br(), opinion_opts(True), ], id='new-content1'),
                html.Div(id='new-content2'),
                html.Div([rating_opts(True)], id='new-content3'),
                html.Br(),
                html.Button(id='submit-button', n_clicks=0, children='Submit')]),
                ], style={'padding-left':'10%', 'padding-right':'10%'})

    elif pathname == '/existing': # existing user
        return html.Div([
                # user_dropdown(),
                # html.Div(id='existing-content1'),
                html.Div([html.H6('Select your ID: '),
                    user_dropdown(),
                    html.Br(),
                    html.Button(id='existing-submit', n_clicks=0, children='Submit'),
                    html.Br(),
                    html.Div([], id='existing-output')
                          ]),
                html.Br(),
            ], style={'padding-left':'10%', 'padding-right':'10%'})
    elif pathname == '/recommender': # existing user
        return html.Div([
                # user_dropdown(),
                # html.Div(id='existing-content1'),
                html.Div([html.H6('Select Movies you like and dislike: '),
                    like_dropdown(),
                      html.Br(),
                    dislike_dropdown(),
                      html.Br(),
                    html.Button(id='recommender_submit', n_clicks=0, children='Submit'),
                    html.Br(),
                          html.Div([],id='recommender_output'),
                    #opinion_opts(True),
                    ], id='recommender-1'),
                html.Br(),
            ], style={'padding-left':'10%', 'padding-right':'10%'})
    else:
        return

@app.callback(
    Output('new-content1', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('genre-dropdown', 'value'), State('opinion-radio', 'value'), State('rating-radio', 'value')])

def update_output(n_clicks, g, o, r):
    global current_movie
    global cycled_movies
    global liked
    global disliked
    global glob_genres

    rectext = ''

    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate()

    elif n_clicks == 1:
        rectext = 'Best-In-Genre Recommendation: '
        glob_genres = g
        m, title  = first_recomm(g,cycled_movies)

    elif len(cycled_movies) < user_rec_thresh:
        rectext = 'Best-In-Genre Recommendation: '
        if o == 'Interested':
            liked.append(current_movie)
        else:
            disliked.append(current_movie)

        m, title = first_recomm(glob_genres,cycled_movies)
    else:
        rectext = 'User-Item SVD Recommendation: '

        if o == 'Interested':
            liked.append(current_movie)
        else:
            disliked.append(current_movie)

        m, title = recomm_new_user(liked,disliked)


    current_movie = m
    cycled_movies.append(current_movie)

    imdbinfo = get_movie_info(current_movie)
    thumbnail = imdbinfo['cover url']

    return [genre_dropdown(True), html.H5(rectext), html.H6(title), html.Img(src=thumbnail),opinion_opts( )]


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
    else:
        return [rating_opts(True),]

@app.callback(
    Output('recommender_output', 'children'),
    [Input('recommender_submit', 'n_clicks')],
    [State('like_dropdown', 'value'), State('dislike_dropdown', 'value')])
def update_output(n_clicks, like, dislike):

    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate()

    if (like is None or like == []) and (dislike is None or dislike == []):
        raise dash.exceptions.PreventUpdate()

    if like is None:
        like = []
    if dislike is None:
        dislike = []

    current_movie, title = recomm_new_user(like,dislike)

    imdbinfo = get_movie_info(current_movie)
    thumbnail = imdbinfo['cover url']

    return [html.H5('Recommendation: '), html.H6(title), html.Img(src=thumbnail)]


# ======================================================================================= #
# =============================== EXISTING USERS ======================================== #
# ======================================================================================= #
n_not_interested = 0
n_similar_user = 0
reviewed_movies = []
#glob_v = ''
# Callback of existing user's selection
@app.callback(
    Output('existing-output', 'children'),
    [Input('existing-submit', 'n_clicks')],
    [State('user-dropdown', 'value'),
    ])
def update_output(n_clicks,u):
    global current_user, current_movie, n_similar_user, cycled_movies, glob_v

    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate()

    current_movie, title = recomm_exist_user(cycled_movies,u)

    cycled_movies.append(current_movie)

    imdbinfo = get_movie_info(current_movie)
    thumbnail = imdbinfo['cover url']

    return [html.H5('Recommendation based on your ratings: '), html.H6(title), html.Img(src=thumbnail)]

# Showing rating options
@app.callback(
    Output('existing-content2', 'children'),
    [Input('opinion-radio', 'value')])

def update_output(value):
    if value == 'Watched':
        return [rating_opts(),]
        # html.Button(id='opinion-button', n_clicks=0, children='Submit')]
    else:
        # return [html.Button(id='opinion-button', n_clicks=0, children='Next')]
        return [rating_opts(True),]

if __name__ == '__main__':
    # Loading screen CSS
    app.run_server(debug=True)



