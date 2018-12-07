import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from user import User
from scipy import spatial
import pickle
from recommend_movies_svd import *

'''
ratings_file = 'ml-latest-small/ratings.csv'
movies_file = 'ml-latest-small/movies.csv'
export = 'ml-latest-small/ratings_new.csv'
'''

# New subset of the full-size MovieLens set
#ratings_file = 'ml-svd/finalRatings.csv'
movies_file = 'ml-svd/finalMovies.csv'
export = 'ml-svd/finalRatings_new.csv'

num_genre_col = 6 # number of columns after splitting the genre string of movies df

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


def first_recomm(selected_genres,cycled_movies):
	# find movies with highest ratings & in genres selected by the user
	sorted_ratings = ratings_df.sort_values('bayesianRating', ascending=False)
	for index, row in sorted_ratings.iterrows():
		m = row['movieId']
		if m in cycled_movies:
			continue
		#print(m,r)
		m = movies_df.iloc[movies.index(m)]
		for i in range(num_genre_col):
			if m[i] in selected_genres:
				return m['movieId'], m['title']

def store_recomm(m_id,rating):
	#print(movies)
	movie_index = movies.index(m_id)
	new_user_movie_ratings[movie_index] = rating

def recomm_new_user(liked,disliked):
	global movies_df

	# Spit list of movies into alg, get movies back
	results = user_predict(liked, disliked, liked+disliked, userRatingColumns, Vt)

	cycledTuple = tuple(liked+disliked)
	for i in results:
		if i not in cycledTuple:
			m = movies_df.loc[movies_df['movieId'] == i]
			return m['movieId'].values[0], m['title'].values[0]

	return None

def recomm_exist_user(watched,userId):
	global movies_df

	watched = sparseFinalDf.loc[userId]
	watchedCols = []
	for index,item in watched.iteritems():
		if item == 0:
			continue
		watchedCols.append(index)

	# Spit list of movies into alg, get movies back
	results = exist_user_predict(userId, watchedCols, userColumns, userRatingColumns, Vt, U)

	cycledTuple = tuple(watchedCols)
	for i in results:
		if i not in cycledTuple:
			m = movies_df.loc[movies_df['movieId'] == i]
			return m['movieId'].values[0], m['title'].values[0]

	return None


# ------------------------------------------------------------------------------------------------

U, Vt, userRatingColumns, userColumns, ratings_df, sparseFinalDf = load_svd_data()

movies_df = pd.read_csv(movies_file)

movies, genres, movie_matrix = gen_movie_matrix()
