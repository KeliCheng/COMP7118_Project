import pickle
import numpy as np
import pandas as pd
import copy

def top_cosine_similarity(data, movie_id):
    index = movie_id #- 1 # Movie id starts from 1
    movie_row = data[movie_id, :]
    magnitude = np.sqrt(np.einsum('ij, ij -> i', data, data))
    similarity = np.dot(movie_row, data.T) / (magnitude[index] * magnitude)
    sort_indexes = np.argsort(-similarity)
    return sort_indexes

def load_svd_data():


    file = open('ml-svd/U.pickle', 'rb')
    U = pickle.load(file)
    file.close()
    '''
    file = open('sigma.pickle', 'rb')
    Sigma = pickle.load(file)
    file.close()
    '''

    file = open('ml-svd/Vt.pickle', 'rb')
    Vt = pickle.load(file)
    file.close()

    file = open('ml-svd/userRatingColumns.pickle', 'rb')
    userRatingColumns = pickle.load(file)
    file.close()

    file = open('ml-svd/aggregatedRatings.pickle', 'rb')
    ratings_df = pickle.load(file)
    file.close()

    file = open('ml-svd/userColumns.pickle', 'rb')
    userColumns = pickle.load(file)
    file.close()

    file = open('ml-svd/sparseFinalDf.pickle', 'rb')
    sparseFinalDf = pickle.load(file)
    file.close()

    return U,Vt,userRatingColumns,userColumns,ratings_df,sparseFinalDf

def user_predict(like,dislike,watched,userRatingColumns,Vt):

    if len(like) == 0 and len(dislike) == 0:
        return

    # Get transpose of Vt
    V = np.array(Vt).transpose()

    # get row index translation of ids
    likeIndexes = []

    for i in like:
        likeIndexes.append(userRatingColumns.index(i))

    likeIndexesArray = np.array(likeIndexes)

    dislikeIndexes = []
    for i in dislike:
        dislikeIndexes.append(userRatingColumns.index(i))

    dislikeIndexesArray = np.array(dislikeIndexes)

    watchedIndexes = []
    for i in watched:
        watchedIndexes.append(userRatingColumns.index(i))

    watchedIndexesArray = np.array(watchedIndexes)

    # Keep rows that are liked
    # Keep negative of rows that are disliked
    # Get average of all those
    if len(dislikeIndexesArray) != 0 and len(likeIndexesArray) != 0:
        averageRow = np.append(V[likeIndexesArray[:, None], :], np.negative(V[dislikeIndexesArray[:, None], :]),axis=0).mean(axis=0)
    elif len(likeIndexesArray) != 0:
        averageRow = V[likeIndexesArray[:, None], :].mean(axis=0)
    else:
        averageRow = np.negative(V[dislikeIndexesArray[:, None], :]).mean(axis=0)

    # Remove rows already watched
    V = np.delete(V,watchedIndexesArray,axis=0)

    # Append the subject row into V
    V = np.append(averageRow, V, axis=0)

    newUserRatingColumns = copy.deepcopy(userRatingColumns)
    for i in sorted(watchedIndexes, reverse=True):
        del newUserRatingColumns[i]

    resultsList = top_cosine_similarity(V, 0)

    for index,i in enumerate(resultsList):
        if i == 0:
            continue
        resultsList[index] = newUserRatingColumns[i - 1]

    return resultsList[1:]


def exist_user_predict(userId,watched,userColumns,userRatingColumns,Vt,U):

    # Get transpose of Vt
    V = np.array(Vt).transpose()
    #V = Vt

    # get row index translation of ids
    userIndex = userColumns.tolist().index(userId)

    watchedIndexes = []
    for i in watched:
        watchedIndexes.append(userRatingColumns.index(i))

    watchedIndexesArray = np.array(watchedIndexes)

    # Remove rows already watched
    V = np.delete(V,watchedIndexesArray,axis=0)

    # Append the subject row into V
    V = np.append(np.array([U[userIndex]]), V, axis=0)

    newUserRatingColumns = copy.deepcopy(userRatingColumns)

    for i in sorted(watchedIndexes, reverse=True):
        del newUserRatingColumns[i]

    resultsList = top_cosine_similarity(V, 0)

    for index,i in enumerate(resultsList):
        if i == 0:
            continue
        resultsList[index] = newUserRatingColumns[i - 1]

    return resultsList[1:]