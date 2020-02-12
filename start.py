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


most twetted genre by Year of release
highest average rating gener by Year of release




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


MOVIES_FILE="./input_data/movies_s.dat"
RATINGS_FILE="./input_data/ratings_s.dat"
USERS_FILE="./input_data/users.dat"

MOVIE_GENRE_NORM_FILE="./norm_data/movie_genre_norm.dat"
MOVIE_NORM_FILE="./norm_data/movie_norm.dat"
RATING_NORM_FILE="./norm_data/rating_norm.dat"

MASTER_FILE="./norm_data/master.dat"

def getTimeElement(t_str,format):
    return time.strftime(format, time.localtime(int(t_str)))

def createNormalisedDataFiles():
    movies_df=pd.read_csv(MOVIES_FILE,   converters={'movie_id': lambda x: str(x)}, header=None, delimiter="::",engine="python",names=["movie_id","movie_title_year","genre"])
    ratings_df=pd.read_csv(RATINGS_FILE, header=None, delimiter="::",engine="python",names=["user_id","movie_id","rating","rating_timestamp"])
    users_df=pd.read_csv(USERS_FILE, header=None, delimiter="::",engine="python",names=("user_id","twitter_id"))
    
    # extracting genre into different data frame
    movie_genre_df=movies_df[["movie_id","genre"]].copy()
    movie_genre_df["genre"]=movie_genre_df["genre"].apply(splitGenreData)
    movie_genre_df=movie_genre_df.explode('genre')
    # removing blanks
    movie_genre_df['genre'].replace('', np.nan, inplace=True)
    movie_genre_df.dropna(subset=['genre'], inplace=True)
    
    # adding year column to movie data in seperate column
    movies_df["year"]=movies_df["movie_title_year"].apply(getMovieYear)
    movies_df=movies_df.drop(['genre'],axis=1)
    
    # splitting time elements to day, month, year, hour and minute
    ratings_df["rating_date"]=ratings_df["rating_timestamp"].apply(lambda t:[getTimeElement(t,"%d"),getTimeElement(t,"%m"),getTimeElement(t,"%Y"),getTimeElement(t,"%H"),getTimeElement(t,"%M")])
    ratings_df[["rating_date_day","rating_date_month","rating_date_year","rating_date_hour","rating_date_minute"]]=pd.DataFrame(ratings_df["rating_date"].tolist())
    ratings_df=ratings_df.drop(['rating_date'],axis=1)
   
    # creating files out of normalised DF
    movie_genre_df.to_csv(MOVIE_GENRE_NORM_FILE,index=False)
    movies_df.to_csv(MOVIE_NORM_FILE,index=False)
    ratings_df.to_csv(RATING_NORM_FILE,index=False)

def testJoin():
    fst = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K1', 'K4', 'K5'],
                   'A': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']})

    # sec = pd.DataFrame({'key': ['K0', 'K1', 'K2','K2'],
    #                     'B': ['B0', 'B1', 'B2','B3']})

    sec = pd.DataFrame({'key': ['K0', 'K0', 'K1','K2', 'K1', 'K1', 'K1', 'K1', 'K1'],
                        'B': ['B0', 'B1', 'B2','B3','B_1','B_2','B_3','B_4','B_5']})


    print(pd.merge(fst,sec,left_on='key',right_on='key',how='left'))

    # print(fst)
    # print(sec)

def makeRatingYearGenre():
    # movie_genre_df=pd.read_csv(MOVIE_GENRE_NORM_FILE, delimiter=",",engine="python",names=["movie_id","genre"])
    # ratings_df=pd.read_csv(RATING_NORM_FILE, delimiter=",",engine="python",names=["user_id","movie_id","rating","rating_timestamp","rating_date_day","rating_date_month","rating_date_year","rating_date_hour","rating_date_minute"])
    # movies_df=pd.read_csv(MOVIE_NORM_FILE, delimiter=",",engine="python",names=["movie_id","movie_title_year","year"])
    movie_genre_df=pd.read_csv(MOVIE_GENRE_NORM_FILE)
    ratings_df=pd.read_csv(RATING_NORM_FILE)
    movies_df=pd.read_csv(MOVIE_NORM_FILE)
    
    # dropping unused columns
    ratings_df.drop(["rating_timestamp","rating_date_day","rating_date_month","rating_date_year","rating_date_hour","rating_date_minute"],axis=1,inplace=True)
    movies_df.drop(["movie_title_year"],axis=1,inplace=True)


    # most twetted genre by Year of release
    # highest average rating gener by Year of release

    merged_df=pd.merge(pd.merge(movies_df,ratings_df,on='movie_id',how='left'),movie_genre_df,on='movie_id',how='left')

    #count_ratings_by_year_df=merged_df.groupby(['year','genre']).count().sort_values(by='movie_id',ascending=False)
    count_ratings_by_year_df=merged_df.groupby(['year','genre']).count().drop(['user_id','rating'],axis=1)
    #count_ratings_by_year_df['genre']=count_ratings_by_year_df.index
    count_ratings_by_year_df.reset_index(level=0, inplace=True)
    print("##"*40)
    #print(count_ratings_by_year_df.groupby(['year','genre'],sort=False)['movie_id'].max())
    x=count_ratings_by_year_df.loc[count_ratings_by_year_df.groupby(['year','genre'], sort=True)['movie_id'].idxmax()]
    print(x.head(10))
    print("$"*40)

    movie_count_year_df=count_ratings_by_year_df.groupby(['year']).max()
    movie_count_year_df.reset_index(level=0, inplace=True)
    #print(movie_count_year_df.head(8))

    final=pd.merge(movie_count_year_df,count_ratings_by_year_df,how='left',on=['movie_id','year'])
    print("(("*40)
    #print(final.head(10))
    print("))"*40)
    #.sort('movie_id').index[-1]#
    # count_ratings_by_year_df.groupby(['year','genre']).
    # print(count_ratings_by_year_df)

    # print(movie_genre_df.head())
    # print(ratings_df.head()).max().reset_index(level=0).sort_values(by='year')
    # print(movies_df.head())
    # print(merged_df.head())
    print(count_ratings_by_year_df.head())
    merged_df.to_csv(MASTER_FILE,index=False)
    count_ratings_by_year_df.to_csv("./norm_data/op.dt")


def main():
    print("Have started")
    createNormalisedDataFiles()
    #testJoin()
    makeRatingYearGenre()
    #test()
