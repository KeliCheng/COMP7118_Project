import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from user import User


ratings_file = 'ml-latest-small/ratings.csv'
movies_file = 'ml-latest-small/movies.csv'
export = 'ml-latest-small/ratings_new.csv'
num_genre_col = 10 # number of columns after splitting the genre string of movies df


'''generate users matrix'''
def gen_user_matrix():
	global ratings_df

	users = ratings_df['userId'].unique().tolist()
	movies = ratings_df['movieId'].unique().tolist()

	matrix = np.zeros(shape=(len(users), len(movies)))

	for index, row in ratings_df.iterrows():
		u = users.index(row['userId'])
		m = movies.index(row['movieId'])
		matrix[u, m] = row['rating']
	return users, matrix


'''generate movies matrix'''
def gen_movie_matrix():
	global movies_df
	movies = movies_df['movieId'].unique().tolist()

	# split columns
	movies_df = pd.concat([movies_df['movieId'],
		movies_df['title'],
		movies_df['genres'].str.split('|', expand=True),
		], axis=1)

	genres = pd.unique(movies_df[list(range(num_genre_col))].values.ravel('K')).tolist()

	matrix = np.zeros(shape=(len(movies), len(genres)))

	for index, row in movies_df.iterrows():
		for i in range(num_genre_col):
			m = movies.index(row['movieId'])
			g = genres.index(row[i])
			matrix[m][g] = 1
	return movies, genres, matrix

# ----------------------------------------------------------------------------------------------
'''find most similar item based on cosine similarity'''
def most_similar_item(cos_sim, l, item, n):
	i = l.index(item)
	j = cos_sim[i].argsort()[-(n+1)]

	return j # the index


'''find least similar item based on cosine similarity'''
def least_similar_item(cos_sim, l, item, n):
	i = l.index(item)
	j = cos_sim[i].argsort()[n-1]

	return j # the index



''' find a most similar user based on current users profile '''
''' and recommend an unseen movie '''
def get_recommendation(u_id):
	global user_matrix, user_cos_sim, users, ratings_df

	j = most_similar_item(user_cos_sim, users, u_id, 1) # find most similar user

	# get all movies rated by similar user
	for index, v in ratings_df.loc[ratings_df['userId'] == users[j]].iterrows():
		if user_matrix[users.index(u_id)][int(v['movieId'])] == 0.0:
			m = movies_df.loc[movies_df['movieId'] == v['movieId']]
			return int(v['userId']), m['title'].to_string()


def first_recomm(selected_genres):
	# find movies with highest ratings & in genres selected by the user
	sorted_ratings = ratings_df.groupby('movieId').rating.mean().sort_values(ascending=False)
	for m, r in sorted_ratings.items():
		m = movies_df.iloc[movies.index(m)]
		for i in range(num_genre_col):
			if m[i] in selected_genres:
				return m['movieId'], m['title']






# ------------------------------------------------------------------------------------------------

movies_df = pd.read_csv(movies_file)
ratings_df = pd.read_csv(ratings_file)

movies, genres, movie_matrix = gen_movie_matrix()
movies_cos_sim = 1-pairwise_distances(movie_matrix, metric="cosine")
#

users, user_matrix = gen_user_matrix()
user_cos_sim = 1-pairwise_distances(user_matrix, metric="cosine")

# first_recomm(['Comedy'])


