import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from user import User
import pickle

'''
ratings_file = 'ml-latest-small/ratings.csv'
movies_file = 'ml-latest-small/movies.csv'
export = 'ml-latest-small/ratings_new.csv'
'''

# New subset of the full-size MovieLens set
ratings_file = 'ml-subset/finalRatings.csv'
movies_file = 'ml-subset/finalMovies.csv'
export = 'ml-subset/finalRatings_new.csv'

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
	j = cos_sim[i].argsort().tolist()[-(n+1)]

	return j # the index

'''find most similar item based on cosine similarity except from those in list'''
def most_similar_item_except(cos_sim, l, item, n, exceptions):

	exceptions = [l.index(x) for x in exceptions]

	i = l.index(item)
	simList = cos_sim[i].argsort().tolist()

	simList = [x for x in simList if x not in exceptions]

	j = simList[-(n+1)]

	return j # the index


'''find least similar item based on cosine similarity except from those in list'''
def least_similar_item_except(cos_sim, l, item, n, exceptions):

	exceptions = [l.index(x) for x in exceptions]

	i = l.index(item)
	simList = cos_sim[i].argsort().tolist()

	simList = [x for x in simList if x not in exceptions]

	j = simList[n-1]

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


''' find a most similar movie based on genre and recommend '''
def get_movie_recommendation(m_id,cycled_movies):
	global movie_matrix, movies_cos_sim, movies, ratings_df
	j = most_similar_item_except(movies_cos_sim, movies, m_id, 1, cycled_movies) # find most similar movie

	return j


''' find a least similar movie based on genre and recommend '''
def get_movie_recommendation_inverse(m_id,cycled_movies):
	global movie_matrix, movies_cos_sim, movies, ratings_df
	j = least_similar_item_except(movies_cos_sim, movies, m_id, 1, cycled_movies) # find most similar movie

	return j


def first_recomm(selected_genres):
	# find movies with highest ratings & in genres selected by the user
	sorted_ratings = ratings_df.groupby('movieId').rating.mean().sort_values(ascending=False)
	for m, r in sorted_ratings.items():
		m = movies_df.iloc[movies.index(m)]
		for i in range(num_genre_col):
			if m[i] in selected_genres:
				return m['movieId'], m['title']


def subseq_recomm(current_movie,cycled_movies,opinion):

	if opinion == 'Interested':
		m = get_movie_recommendation(current_movie,cycled_movies)
	else:
		m = get_movie_recommendation_inverse(current_movie,cycled_movies)
	m = movies_df.iloc[m]

	return m['movieId'], m['title']



# ------------------------------------------------------------------------------------------------

# Speed up the process by storing the matrix objects.
# This way, we don't need to recalculate the distances when starting the app.
# If the data to use changes, flip this switch for the first run.
recalcMatrix = True

if recalcMatrix:
	movies_df = pd.read_csv(movies_file)
	ratings_df = pd.read_csv(ratings_file)

	movies, genres, movie_matrix = gen_movie_matrix()
	movies_cos_sim = 1-pairwise_distances(movie_matrix, metric="cosine")

	users, user_matrix = gen_user_matrix()
	user_cos_sim = 1-pairwise_distances(user_matrix, metric="cosine")

	file = open('movies.pickle', 'wb')
	pickle.dump(movies, file)
	file.close()

	file = open('genres.pickle', 'wb')
	pickle.dump(genres, file)
	file.close()

	file = open('movie_matrix.pickle', 'wb')
	pickle.dump(movie_matrix, file)
	file.close()

	file = open('movies_cos_sim.pickle', 'wb')
	pickle.dump(movies_cos_sim, file)
	file.close()

	file = open('users.pickle', 'wb')
	pickle.dump(users, file)
	file.close()

	file = open('user_matrix.pickle', 'wb')
	pickle.dump(user_matrix, file)
	file.close()

	file = open('user_cos_sim.pickle', 'wb')
	pickle.dump(user_cos_sim, file)
	file.close()

	file = open('movies_df.pickle', 'wb')
	pickle.dump(movies_df, file)
	file.close()

	file = open('ratings_df.pickle', 'wb')
	pickle.dump(ratings_df, file)
	file.close()

else:
	file = open('movies.pickle', 'rb')
	movies = pickle.load(file)
	file.close()

	file = open('genres.pickle', 'rb')
	genres = pickle.load(file)
	file.close()

	file = open('movie_matrix.pickle', 'rb')
	movie_matrix = pickle.load(file)
	file.close()

	file = open('movies_cos_sim.pickle', 'rb')
	movies_cos_sim = pickle.load(file)
	file.close()

	file = open('users.pickle', 'rb')
	users = pickle.load(file)
	file.close()

	file = open('user_matrix.pickle', 'rb')
	user_matrix = pickle.load(file)
	file.close()

	file = open('user_cos_sim.pickle', 'rb')
	user_cos_sim = pickle.load(file)
	file.close()

	file = open('movies_df.pickle', 'rb')
	movies_df = pickle.load(file)
	file.close()

	file = open('ratings_df.pickle', 'rb')
	ratings_df = pickle.load(file)
	file.close()




# first_recomm(['Comedy'])


