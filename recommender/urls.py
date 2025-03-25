from django.urls import path
from .views import get_movie_recommendations

urlpatterns = [
    path('recommend/<str:movie_name>/', get_movie_recommendations, name='get_movie_recommendations'),
]