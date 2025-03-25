from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    movie_name = serializers.CharField()