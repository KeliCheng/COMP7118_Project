import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import pickle
#import dask.dataframe as dd

def read_ratings():

    ratings_df = pd.read_csv('ratings.csv')

    return ratings_df

def read_movies():

    movies_df = pd.read_csv('movies.csv')

    return movies_df

def read_links():

    links_df = pd.read_csv('movies.csv')

    return links_df

def reduce_mem_usage(props):
    start_mem_usg = props.memory_usage().sum() / 1024 ** 2
    print("Memory usage of properties dataframe is :", start_mem_usg, " MB")
    NAlist = []  # Keeps track of columns that have missing values filled in.
    for col in props.columns:
        if props[col].dtype != object:  # Exclude strings

            # Print current column type
            print("******************************")
            print("Column: ", col)
            print("dtype before: ", props[col].dtype)

            # make variables for Int, max and min
            IsInt = False
            mx = props[col].max()
            mn = props[col].min()

            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(props[col]).all():
                NAlist.append(col)
                props[col].fillna(mn - 1, inplace=True)

                # test if column can be converted to an integer
            asint = props[col].fillna(0).astype(np.int64)
            result = (props[col] - asint)
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True

            # Make Integer/unsigned Integer datatypes
            if IsInt:
                if mn >= 0:
                    if mx < 255:
                        props[col] = props[col].astype(np.uint8)
                    elif mx < 65535:
                        props[col] = props[col].astype(np.uint16)
                    elif mx < 4294967295:
                        props[col] = props[col].astype(np.uint32)
                    else:
                        props[col] = props[col].astype(np.uint64)
                else:
                    if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                        props[col] = props[col].astype(np.int8)
                    elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                        props[col] = props[col].astype(np.int16)
                    elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                        props[col] = props[col].astype(np.int32)
                    elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                        props[col] = props[col].astype(np.int64)

                        # Make float datatypes 32 bit
            else:
                props[col] = props[col].astype(np.float32)

            # Print new column type
            print("dtype after: ", props[col].dtype)
            print("******************************")

    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = props.memory_usage().sum() / 1024 ** 2
    print("Memory usage is: ", mem_usg, " MB")
    print("This is ", 100 * mem_usg / start_mem_usg, "% of the initial size")
    return props, NAlist

def get_movies_with_rating():
    lowest_rating = 3.3

    ratings_df = pd.read_csv('ratings.csv')

    ratings_df = ratings_df[ratings_df['userId'].isin(ratings_df['userId'].drop_duplicates().sample(frac=0.25).values)]

    avg_rating = ratings_df.groupby('movieId').rating.mean().mean()

    avg_num_votes = ratings_df.groupby('movieId').rating.count().mean()

    groupedMovies = ratings_df.groupby('movieId').rating.agg(['mean', 'count'])

    groupedMovies['bayesianRating'] = ( ( (avg_num_votes * avg_rating) + (groupedMovies['count'] * groupedMovies['mean'])) / (avg_num_votes + groupedMovies['count']  )  )
    print(groupedMovies)

    #groupedMovies = groupedMovies.sort_values('bayesianRating', ascending=False)
    finalMovieList = np.asarray(((groupedMovies.loc[groupedMovies.bayesianRating >= lowest_rating]).index).values) #.tolist()
    groupedMovies.reset_index(level=0, inplace=True)
    aggregatedMovies = groupedMovies[['movieId','bayesianRating']][groupedMovies.movieId.isin(finalMovieList)]
    print(aggregatedMovies)

    culledDf = ratings_df[ratings_df.movieId.isin(finalMovieList)]
    return culledDf, finalMovieList, aggregatedMovies
    #culledDf = culledDf.categorize(columns=['movieId'])
    #culledDf = culledDf.to_sparse(fill_value=0)
    #print(culledDf.density)
    #print(pivotedDf.density)
    #pivotedDf = pivotedDf.repartition(npartitions=500)
    #print(pivotedDf.npartitions)
    #finalDf = pivotedDf.compute()

finalDf, movieList, aggregatedDf = get_movies_with_rating()

print(finalDf.dtypes)
reduce_mem_usage(finalDf)

#finalDf["rating"] = pd.to_numeric(finalDf["rating"],downcast='float')
#finalDf[["userid", "movieId", "timestamp"]] = finalDf[["userId", "movieId", "timestamp"]].apply(pd.to_numeric,downcast='unsigned')
print(finalDf)
finalDf = finalDf.pivot_table(index='userId', columns='movieId', values='rating', fill_value=0)

sparseFinalDf = finalDf.to_sparse(fill_value = 0)

moviesDf = read_movies()
linksDf = read_links()

finalMoviesDf = moviesDf[moviesDf['movieId'].isin(movieList)]
finalLinksDf = linksDf[linksDf['movieId'].isin(movieList)]

print('Number of rows in Ratings file:',finalDf.shape[0])

#finalDf.to_csv('finalRatings.csv',index = False,encoding="utf-8")
finalMoviesDf.to_csv('finalMovies.csv',index = False,encoding="utf-8")
finalLinksDf.to_csv('finalLinks.csv',index = False,encoding="utf-8")

userRatingMatrix = finalDf.as_matrix()

print(finalDf)
print(finalDf.index)

userColumns = finalDf.index.values

U, sigma, Vt = svds(userRatingMatrix, k = 100)

filehandler = open('sparseFinalDf.pickle', 'wb')
pickle.dump(sparseFinalDf, filehandler)

filehandler = open('U.pickle', 'wb')
pickle.dump(U, filehandler)

filehandler = open('sigma.pickle', 'wb')
pickle.dump(sigma, filehandler)

filehandler = open('Vt.pickle', 'wb')
pickle.dump(Vt, filehandler)

userRatingColumns = list(finalDf.columns.values)
print(userRatingColumns)

filehandler = open('userRatingColumns.pickle', 'wb')
pickle.dump(userRatingColumns, filehandler)

filehandler = open('aggregatedRatings.pickle', 'wb')
pickle.dump(aggregatedDf, filehandler)

filehandler = open('userColumns.pickle', 'wb')
pickle.dump(userColumns, filehandler)

'''
users = ratingsdf['userId'].unique().tolist()
movies = ratingsdf['movieId'].unique().tolist()


print(len(users),len(movieTuple))

matrix = np.zeros(shape=(len(users), len(movieTuple)))

for index, row in ratingsdf.iterrows():
    u = users.index(row['userId'])
    m = movies.index(row['movieId'])

    if m not in movieTuple:
        continue

    matrix[u, movieTuple.index(m)] = row['rating']

print(matrix)
'''