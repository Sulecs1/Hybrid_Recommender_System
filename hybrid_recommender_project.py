#############################################################################################
#               HYBRID RECOMMENDER SYSTEM PROJECT                                           #
#############################################################################################
#<<<Şule AKÇAY>>>

#############################################
# Adım 1: Verinin Hazırlanması
#############################################

import pandas as pd

from helpers.helpers import create_user_movie_df
################################################

user_movie_df = create_user_movie_df()
user_number = 12312

#############################################
# Adım 2: Öneri yapılacak kullanıcının izlediği filmlerin belirlenmesi
#############################################

random_user_df = user_movie_df[user_movie_df.index == user_number]
random_user_df


movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

len(movies_watched)  #19


#############################################
# Adım 3: Aynı filmleri izleyen diğer kullanıcıların verisine ve id'lerine erişmek
#############################################
movies_watched_df = user_movie_df[movies_watched]
movies_watched_df
movies_watched_df.shape  #(23149, 19)

user_movie_count = movies_watched_df.T.notnull().sum() #herbir kullanıcı için kaç film izlediği geldi
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]

perc = len(movies_watched) * 60 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]


