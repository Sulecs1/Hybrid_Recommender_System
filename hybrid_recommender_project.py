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

#############################################
# Adım 6: Weighted average recommendation score'un hesaplanması ve ilk beş filmin tutulması
#############################################
temp = top_users_ratings.groupby('movieId').sum()[['corr', 'weighted_rating']]
temp.columns = ['sum_corr', 'sum_weighted_rating']

temp.head()

recommendation_df = pd.DataFrame()
recommendation_df['weighted_average_recommendation_score'] = temp['sum_weighted_rating'] / temp['sum_corr']
recommendation_df['movieId'] = temp.index
recommendation_df = recommendation_df.sort_values(by='weighted_average_recommendation_score', ascending=False)
recommendation_df.head(10)


movie = pd.read_csv(r'C:\Users\Suleakcay\PycharmProjects\pythonProject3\Datasets\movie.csv')
movie_user = movie.loc[movie['movieId'].isin(recommendation_df.head(10)['movieId'].head())]['title']
movie_user.head()
movie_user[:5].values

"""array(['Strange Days (1995)',
            'Pulp Fiction (1994)',
            'Forrest Gump (1994)',
            'Rudy (1993)',
            "Schindler's List (1993)"],
      dtype=object)"""

#############################################
# Adım 7: İzlediği filmlerden en son en yüksek puan verdiği filmin adına göre item-based öneri yapınız.
# 5 öneri user-based 5 öneri item-based olacak şekilde 10 öneri yapınız.
#############################################

pd.set_option('display.max_columns', None)

movie = pd.read_csv(r'C:\Users\Suleakcay\PycharmProjects\pythonProject3\Datasets\movie.csv')
#title/genres/movieId <- movie
rating = pd.read_csv(r'C:\Users\Suleakcay\PycharmProjects\pythonProject3\Datasets\rating.csv')
#movieId,rating,timestamp
df = movie.merge(rating, how="left", on="movieId")
df.head()

#################
# title
#################
#yılı ayrıca ayıklama işlemi
df['year_movie'] = df.title.str.extract('(\(\d\d\d\d\))', expand=False) #4 değer olan ifadeyi çek
df['year_movie'] = df.year_movie.str.extract('(\d\d\d\d)', expand=False) #parantezlerin içine alıyoruz
df['title'] = df.title.str.replace('(\(\d\d\d\d\))', '')  #title içindeki yılı temizliyoruz
df['title'] = df['title'].apply(lambda x: x.strip()) #oluşan  boşulkları sil

df.shape  #(3400256, 7)
df.head()

#################
# genres
#################

df["genre"] = df["genres"].apply(lambda x: x.split("|")[0])
df.drop("genres", inplace=True, axis=1)
df.head()
#################
# timestamp  ->yaygın bir ihtiyaçtır
#################

df.info()  #timestamp time formatında olması lazım

df["timestamp"] = pd.to_datetime(df["timestamp"], format='%Y-%m-%d')
df.info() #datetime64[ns]

#Verileri ayrı ayrı çektik
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df.head()
######################################
# Adım 2: User Movie Df'inin Oluşturulması
######################################

df.shape
df["title"].nunique() #eşsiz film sayısı :26213
a = pd.DataFrame(df["title"].value_counts())
a.head() #titlelara gelen puanlar

rare_movies = a[a["title"] <= 1000].index  #1000 yorumun altındaki filmleri filtreledik
common_movies = df[~df["title"].isin(rare_movies)]
common_movies.shape #(2059083, 10)
common_movies["title"].nunique()  #859

item_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
item_movie_df.shape  #(23149, 859)
user_movie_df.head(10)
item_movie_df.columns

len(item_movie_df.columns)
common_movies["title"].nunique()




