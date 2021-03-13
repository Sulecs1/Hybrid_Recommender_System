#############################################################################################
#               HYBRID RECOMMENDER SYSTEM PROJECT                                           #
#############################################################################################
#<<<Şule AKÇAY>>>

#############################################
# Adım 1: Verinin Hazırlanması
#############################################

import pandas as pd
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

df.shape
df.head()



#############################################
# Adım 2: Öneri yapılacak kullanıcının izlediği filmlerin belirlenmesi
#############################################

#############################################
# Adım 3: Aynı filmleri izleyen diğer kullanıcıların verisine ve id'lerine erişmek
#############################################

#############################################
# Adım 4: Öneri yapılacak kullanıcı ile en benzer kullanıcıların belirlenmesi
#############################################

#############################################
# Adım 5: Weighted rating'lerin  hesaplanması
#############################################

#############################################
# Adım 6: Weighted average recommendation score'un hesaplanması ve ilk beş filmin tutulması
#############################################

#############################################
# Adım 7: İzlediği filmlerden en son en yüksek puan verdiği filmin adına göre item-based öneri yapınız.
# 5 öneri user-based 5 öneri item-based olacak şekilde 10 öneri yapınız.
#############################################

