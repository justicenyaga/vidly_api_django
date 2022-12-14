from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Genre, Movie
from .serializer import GenreSerializer, MovieSerializer, UserSerializer, UserSerializerWithToken

# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)

        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getGenres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMovies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMovie(request, pk):
    movie = Movie.objects.get(_id=pk)
    serializer = MovieSerializer(movie, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateMovie(request, pk):
    data = request.data

    movie = Movie.objects.get(_id=pk)

    movie.title = data['title']
    movie.numberInStock = data['numberInStock']
    movie.dailyRentalRate = data['dailyRentalRate']
    movie.genre = Genre.objects.get(_id=data['genre'])

    movie.save()

    serializer = MovieSerializer(movie, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createMovie(request):
    data = request.data

    movie = Movie.objects.create(
        title=data['title'],
        numberInStock=data['numberInStock'],
        dailyRentalRate=data['dailyRentalRate'],
        genre=Genre.objects.get(_id=data['genre'])
    )

    serializer = MovieSerializer(movie, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteMovie(request, pk):
    movie = Movie.objects.get(_id=pk)
    movie.delete()

    return Response('Movie Deleted')
