import pandas as pd
import numpy as np
import time

'''
Structure of movies.dat
movie_id::movie_title (movie_year)::genre|genre|genre

Structure of users.dat
userid::twitter_id

Structure of ratings.dat
user_id::movie_id::rating::rating_timestamp

the most popular movie genres, year by year, for the past decade by using user rating from tweets.


'''


def splitGenreData(val):
    if isinstance(val,str):
        return [(x) for x in val.split("|")] if val!=None else []
    else:
        return []

def getMovieYear(val):
    if isinstance(val,str):
        beg=val.find("(")
        en=val.find(")")
        return val[beg+1:en]
    else:
        return None


MOVIES_FILE="./data/movies.dat"
RATINGS_FILE="./data/ratings.dat"
USERS_FILE="./data/users.dat"

# MOVIES_FILE="./data/movies_s.dat"
# RATINGS_FILE="./data/ratings_s.dat"
# USERS_FILE="./data/users_s.dat"

MOVIE_GENRE_OP_FILE="./op/movie_genre_op.dat"
MOVIE_OP_FILE="./op/movie_op.dat"
RATING_OP_FILE="./op/rating_op.dat"
# def test():
#     df = pd.DataFrame({'num_legs': [2, 4, 8, 0],
#                     'num_wings': [2, 0, 0, 0],
#                     'num_specimen_seen': ["aa|bb|cc", "aa", "nn|kk", "LL|hh"]},
#                     index=['falcon', 'dog', 'spider', 'fish'])
    
#     df["sp"]=df['num_specimen_seen'].apply(splitGenreData)
#     df=df.explode('sp')
#     print(df)
#     # otherDf=newDF.set_index(['num_legs']).apply(lambda x:x.str.split("|").explode())
#     # #otherDf=newDF.set_index(['num_legs']).apply(lambda x:x[0].split("|").explode())


#     # print(otherDf)
    
#     # xdf=newDF.explode('num_specimen_seen')
#     # print(newDF)
#     # print(xdf)


def getTimeElement(t_str,format):
    return time.strftime(format, time.localtime(int(t_str)))

def main():
    print("Have started")
    movies_df=pd.read_csv(MOVIES_FILE, header=None, delimiter="::",engine="python",names=["movie_id","movie_title_year","genre"])
    ratings_df=pd.read_csv(RATINGS_FILE, header=None, delimiter="::",engine="python",names=["user_id","movie_id","rating","rating_timestamp"])
    users_df=pd.read_csv(USERS_FILE, header=None, delimiter="::",engine="python",names=("user_id","twitter_id"))
    
    #extracting genre into different data frame
    movie_genre_df=movies_df[["movie_id","genre"]].copy()
    movie_genre_df["genre"]=movie_genre_df["genre"].apply(splitGenreData)
    movie_genre_df=movie_genre_df.explode('genre')
    
    #adding year column to movie data in seperate column
    movies_df["year"]=movies_df["movie_title_year"].apply(getMovieYear)
    movies_df=movies_df.drop(['genre'],axis=1)
    
    #splitting time elements to day, month, year, hour and minute
    ratings_df["rating_date"]=ratings_df["rating_timestamp"].apply(lambda t:[getTimeElement(t,"%d"),getTimeElement(t,"%m"),getTimeElement(t,"%Y"),getTimeElement(t,"%H"),getTimeElement(t,"%M")])
    ratings_df[["rating_date_day","rating_date_month","rating_date_year","rating_date_hour","rating_date_minute"]]=pd.DataFrame(ratings_df["rating_date"].tolist())
    ratings_df=ratings_df.drop(['rating_date'],axis=1)



    
    print(movies_df.head())
    #print(ratings_df.head())
    #print(users_df.head())
    print(movie_genre_df.head())
    movie_genre_df.to_csv(MOVIE_GENRE_OP_FILE,index=False)
    movies_df.to_csv(MOVIE_OP_FILE,index=False)
    ratings_df.to_csv(RATING_OP_FILE,index=False)
    #test()
