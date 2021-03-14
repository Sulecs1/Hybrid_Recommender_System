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


