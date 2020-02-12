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

MOVIES_FILE="./input_data/movies.dat"
RATINGS_FILE="./input_data/ratings.dat"
USERS_FILE="./input_data/users.dat"

MOVIE_GENRE_NORM_FILE="./norm_data/movie_genre_norm.dat"
MOVIE_NORM_FILE="./norm_data/movie_norm.dat"
RATING_NORM_FILE="./norm_data/rating_norm.dat"

GENRE_MAX_COMMENTS_FILE="./norm_data/genre_max_comments.csv"
GENRE_MAX_RATINGS_FILE="./norm_data/genre_max_ratings.csv"


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


# highest average rating gener by Year of release
def higherRatings():
    movie_genre_df=pd.read_csv(MOVIE_GENRE_NORM_FILE)
    ratings_df=pd.read_csv(RATING_NORM_FILE)
    movies_df=pd.read_csv(MOVIE_NORM_FILE)
    
    # dropping unused columns
    ratings_df.drop(["rating_timestamp","rating_date_day","rating_date_month","rating_date_year","rating_date_hour","rating_date_minute"],axis=1,inplace=True)
    movies_df.drop(["movie_title_year"],axis=1,inplace=True)

    movie_genre_mean_df=pd.merge(pd.merge(movies_df,ratings_df,on='movie_id',how='left'),movie_genre_df,on='movie_id',how='left')
    movie_genre_mean_df.drop(['movie_id','user_id'],axis=1,inplace=True)
    movie_genre_mean_df=movie_genre_mean_df.groupby(['year','genre']).mean()
    movie_genre_mean_df.reset_index( inplace=True)
    movie_mean_df=movie_genre_mean_df.drop(['genre'],axis=1)
    
    movie_mean_df=movie_mean_df.groupby(['year']).max()
    movie_mean_df.reset_index( inplace=True)   
    result_df=pd.merge(movie_mean_df,movie_genre_mean_df,on=['year','rating'],how='left')
    result_df.to_csv(GENRE_MAX_RATINGS_FILE,index=False)


# most twetted genre by Year of release
def makeRatingYearGenre():
    movie_genre_df=pd.read_csv(MOVIE_GENRE_NORM_FILE)
    ratings_df=pd.read_csv(RATING_NORM_FILE)
    movies_df=pd.read_csv(MOVIE_NORM_FILE)
    
    # dropping unused columns
    ratings_df.drop(["rating_timestamp","rating_date_day","rating_date_month","rating_date_year","rating_date_hour","rating_date_minute"],axis=1,inplace=True)
    movies_df.drop(["movie_title_year"],axis=1,inplace=True)

    merged_df=pd.merge(pd.merge(movies_df,ratings_df,on='movie_id',how='left'),movie_genre_df,on='movie_id',how='left')

    count_ratings_by_year_df=merged_df.groupby(['year','genre']).count().drop(['user_id','rating'],axis=1)
    count_ratings_by_year_df.reset_index(level=0, inplace=True)
    count_ratings_by_year_df["genre_c"]=count_ratings_by_year_df.index
    
    year_max_of_movie_df=count_ratings_by_year_df.groupby(['year'], sort=True).max()
    year_max_of_movie_df.reset_index(level=0,inplace=True)
    year_max_of_movie_df=year_max_of_movie_df.groupby("year").max()

    result_df=pd.merge(year_max_of_movie_df,count_ratings_by_year_df,on=['year','movie_id'],how="inner").drop(['genre_c_x'],axis=1)
    result_df.rename(columns={"movie_id":"remarks_count","genre_c_y":"genre"},inplace=True)
    result_df.to_csv(GENRE_MAX_COMMENTS_FILE,index=False)


def main():
    print("Starting.....")
    createNormalisedDataFiles()
    makeRatingYearGenre()
    higherRatings()
    print("Done")
