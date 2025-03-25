import numpy as np
import pandas as pd

movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')

movies.head(1)

credits.head(1)

credits.head(1)['cast']

movies.merge(credits, on='title')

movies=movies.merge(credits, on='title')

movies.head(1)

# genres
# id
# keywords
# title
# overview
# cast
# crew
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.head(1)

movies.isnull().sum()

movies.dropna(inplace=True)

movies.duplicated().sum()

movies.isnull().sum()

import ast
def convert(obj):
    tags=[]
    for i in ast.literal_eval(obj):
        tags.append(i['name'])
    return tags

movies.head(1)

movies['keywords']=movies['keywords'].apply(convert)

movies.head()

import ast
def convertCast(obj):
    tags=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter != 3:
            tags.append(i['name'])
            counter+=1
        else:
            break
    return tags

movies['cast']=movies['cast'].apply(convertCast)

movies.head()

movies['crew'][0]

import ast
def findDirector(obj):
    tags=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            tags.append(i['name'])
            break
    return tags

movies['crew']=movies['crew'].apply(findDirector)

movies.head()

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

# 'Sam Worthington'->'SamWorthington'
movies['genres']=movies['genres'].apply(convert)


movies['genres']

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags']=movies['overview']+movies['genres']+movies['cast']+movies['keywords']+movies['crew']

movies.head()

newMoviesData=movies[['movie_id','title','tags']]

newMoviesData.head()

newMoviesData['tags']=newMoviesData['tags'].apply(lambda x:" ".join(x))

newMoviesData['tags'][0]

newMoviesData['tags']=newMoviesData['tags'].apply(lambda x:x.lower()) 
# recommended

newMoviesData.head()

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
    textArray=[]
    for i in text.split():
        textArray.append(ps.stem(i))
    return " ".join(textArray)

newMoviesData['tags']=newMoviesData['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000, stop_words='english')

vectors=cv.fit_transform(newMoviesData['tags']).toarray()
#vectorization

vectors

vectors[0]

cv.get_feature_names_out()

from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vectors)
#calculating the similar data through cosine angle greater the cosine angle=>lesser the similarity

similarity[1]

def recommend(movie):
    movies_index=newMoviesData[newMoviesData['title'].apply(lambda x:x.lower())==movie.lower()].index[0]
    distances=similarity[movies_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:31]
    movies_name=[]
    for i in movies_list:
        movies_name.append(newMoviesData.iloc[i[0]].movie_id)
        print(newMoviesData.iloc[i[0]].movie_id)
    # print(movies_name)
    return movies_name

# newMoviesData['title'].apply(lambda x:x.lower())=='spider'

# recommend('avenge')



