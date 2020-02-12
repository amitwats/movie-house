import pandas as pd
import numpy as np


'''
Structure of movies.dat
movie_id::movie_title (movie_year)::genre|genre|genre

Structure of users.dat
userid::twitter_id

Structure of ratings.dat
user_id::movie_id::rating::rating_timestamp

the most popular movie genres, year by year, for the past decade by using user rating from tweets.


'''
def getGenreData(str):
    #return 
    return [(x) for x in str.split("|")]

# MOVIES_FILE="./data/movies.dat"
# RATINGS_FILE="./data/ratings.dat"
# USERS_FILE="./data/users.dat"

MOVIES_FILE="./data/movies_s.dat"
RATINGS_FILE="./data/ratings_s.dat"
USERS_FILE="./data/users_s.dat"

def test():
    df = pd.DataFrame({'num_legs': [2, 4, 8, 0],
                    'num_wings': [2, 0, 0, 0],
                    'num_specimen_seen': ["aa|bb|cc", "aa", "nn|kk", "LL|hh"]},
                    index=['falcon', 'dog', 'spider', 'fish'])
    
    newDF=df[['num_legs','num_specimen_seen']]
    df["sp"]=df['num_specimen_seen'].apply(getGenreData)
    df=df.explode('sp')
    print(df)
    # otherDf=newDF.set_index(['num_legs']).apply(lambda x:x.str.split("|").explode())
    # #otherDf=newDF.set_index(['num_legs']).apply(lambda x:x[0].split("|").explode())


    # print(otherDf)
    
    # xdf=newDF.explode('num_specimen_seen')
    # print(newDF)
    # print(xdf)


def main():
    print("Have started")
    # movies_df=pd.read_csv(MOVIES_FILE, header=None, delimiter="::",engine="python")
    # ratings_df=pd.read_csv(RATINGS_FILE, header=None, delimiter="::",engine="python")
    # users_df=pd.read_csv(USERS_FILE, header=None, delimiter="::",engine="python")
    
    
    # print(movies_df.head())
    # print(ratings_df.head())
    # print(users_df.head())
    test()
