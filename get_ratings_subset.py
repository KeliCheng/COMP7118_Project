import pandas as pd
from scipy.sparse.linalg import svds
import numpy as np

def read_ratings():

    ratings_df = pd.read_csv('ratings.csv')

    return ratings_df

def read_movies():

    movies_df = pd.read_csv('movies.csv')

    return movies_df

def read_links():

    links_df = pd.read_csv('links.csv')

    return links_df

def get_movies_with_rating(lowest_rating):
    df = read_ratings()

    # Limit unique user percentage first.
    #print(df['userId'].drop_duplicates().sample(frac=0.5))
    df = df[df['userId'].isin(df['userId'].drop_duplicates().sample(frac=0.005).values)]

    print(df)

    # Total Average Rating
    avg_rating = df.groupby('movieId').rating.mean().mean()

    # Total Average Number of Votes
    avg_num_votes = df.groupby('movieId').rating.count().mean()

    groupedMovies = df.groupby('movieId').rating.agg(['mean', 'count'])

    groupedMovies['bayesianRating'] = ((avg_num_votes * avg_rating) + (groupedMovies['count'] * groupedMovies['mean'])) / (avg_num_votes + groupedMovies['count'])

    sortedMoviesDf = groupedMovies.sort_values('bayesianRating', ascending=False)
    finalMovieList = ((sortedMoviesDf.loc[sortedMoviesDf.bayesianRating >= lowest_rating]).index).values.tolist()

    print('Number of unique movies in final Ratings table:',len(finalMovieList))

    finalRatingsDf = df[df.movieId.isin(finalMovieList)]
    #pivotedDf = culledDf.pivot_table(index='userId', columns='movieId', values='rating', fill_value=0)

    return finalRatingsDf, finalMovieList



ratingDf,movieList = get_movies_with_rating(3.10)

moviesDf = read_movies()
linksDf = read_links()

finalMoviesDf = moviesDf[moviesDf['movieId'].isin(movieList)]
finalLinksDf = linksDf[linksDf['movieId'].isin(movieList)]

print('Number of rows in Ratings file:',ratingDf.shape[0])

ratingDf.to_csv('finalRatings.csv',index = False,encoding="utf-8")
finalMoviesDf.to_csv('finalMovies.csv',index = False,encoding="utf-8")
finalMoviesDf.to_csv('finalLinks.csv',index = False,encoding="utf-8")
