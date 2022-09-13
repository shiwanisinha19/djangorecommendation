from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import os
import pickle
import random
import pandas as pd

def models(request):
    filename=os.path.dirname(os.path.abspath(__file__))+'/buses_pickle'
    with open(filename,'rb') as f:
        model=pickle.load(f)
    return model

def home(request):
    model=models(request)
    buses=[]
    s=model.index.size
    for i in range(21):
        r=random.randint(1,s)
        buses.append(model.index[r])
    return render(request,'home.html',{'buses':buses})

def detail(request):
    model=models(request)
    buses=request.GET['buses']
    if buses in model.index:
        return render(request,'detail.html',{'buses':buses})
    else:
        return render(request,'detail.html',{'buses':buses,'message':'bus Not found'})


def get_similar(request,bus_name,rating):
    model=models(request)
    similar_ratings = model[bus_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

def recommend_movie(request,buses_collection):
    similar_movies = pd.DataFrame()
    for buses,rating in buses_collection:
        similar_movies = similar_movies.append(get_similar(request,buses,rating),ignore_index = True)
    movies=similar_movies.sum().sort_values(ascending=False).head(10).index
    return movies
    
def recommendation(request):
    bus_name=request.GET['busname']
    rating=request.GET['ratings']
    bus_collection=[]
    bus_collection.append((bus_name,int(rating)))
    buses=recommend_movie(request,bus_collection)
    return render(request,'recommendation.html',{'moviess':buses,'m':bus_name})
