from django.shortcuts import render
import requests
from django.http import JsonResponse
from .movie_model import recommend

API_KEY = "YOUR_API_KEY"
STREAMING_AVAILABILITY_URL = "https://streaming-availability.p.rapidapi.com"

# Create your views here.
def get_movie_recommendations(request, movie_name):
    headers = {
        "x-rapidapi-key": "9027759883msh8d05df6ce9abb0dp14009ajsn4a448f4eb244",
        "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
    }

    # Get recommended movie IDs from model
    recommended_movie_names = recommend(movie_name)
    print(recommended_movie_names)

    if not recommended_movie_names:
        return JsonResponse({"error": "No recommendations found"}, status=404)

    movie_details = []

    for movies_name in recommended_movie_names:
        try:
            # querystring = {"country":"IN","title":movies_name,"show_type":"movie","output_language":"en"}
            movie_details_url = f"{STREAMING_AVAILABILITY_URL}/shows/movie/{movies_name}"
            response = requests.get(movie_details_url, headers=headers)
            # print(response.json())
            data = response.json()

            if data:
                movie_info = {
                    "movie_id": data.get("id", ""),
                    "movie_name": data.get("title", ""),
                    "poster": data.get("imageSet", {}),
                    # "streaming_services": data.get("streamingInfo", {})
                    "genres":data.get("genres",[]),
                    "ratings":data.get("rating",""),
                    "runtime":data.get("runtime",""),

                }
                movie_details.append(movie_info)
        except Exception as e:
            pass  # Skip movie if error occurs

    return JsonResponse({"recommended_movies": movie_details})