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

#############################################
# Adım 4: Öneri yapılacak kullanıcı ile en benzer kullanıcıların belirlenmesi
#############################################
#Kişi ile aynı filmi izleyen kullanıcıların id aynı df getirdik
final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies.index)],
                      random_user_df[movies_watched]])

final_df.head()
final_df.T.corr()
final_df.shape  #(405, 19)

corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()
corr_df.head()

#   user_id_1  user_id_2      corr
#0    10759.0    13820.0 -1.000000
#1    10759.0     8438.0 -1.000000
#2    12641.0     4674.0 -1.000000
#3     2230.0    12312.0 -0.994850
#4    18955.0     1242.0 -0.993399

#korelasyonu yüzdeatmış beşten büyük olan korelasyonu getir
#korelasyonu yüksek olan birbirine en yakın kullanıcıdır
top_users = corr_df[(corr_df["user_id_1"] == user_number) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)

top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

top_users
#   userId      corr
#1    908.0  0.958927
#0  12309.0  0.952563

rating = pd.read_csv(r'C:\Users\Suleakcay\PycharmProjects\pythonProject3\Datasets\rating.csv')
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
top_users_ratings
top_users_ratings.shape #(143, 4)

#############################################
# Adım 5: Weighted rating'lerin  hesaplanması
#############################################
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings.head()



