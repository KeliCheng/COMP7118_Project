import imdb
import pandas as pd

def get_movie_info(mov_id):
    imdb_id = links_df.loc[mov_id]['imdbId']
    movie = access.get_movie(imdb_id,info='main')

    return movie

# Get Links DF
links_file = 'ml-svd/finalLinks.csv'
links_df = pd.read_csv(links_file, index_col=0)

access = imdb.IMDb()

#print("title: %s year: %s" % (movie['title'], movie['year']))
#print ("Cover url: %s" % movie['cover url'])