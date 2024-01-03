from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    TripSerializer,
    SharingTripSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from main.models import Cab, SharingCab, Driver, Trip, SharingTrip
from main.algorithm import assign_cab
from main.sharing_cab_algorithm import assign_sharing_cab
import datetime


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/login/",
        "/api/register/",
        "/api/login/refresh/" "/api/candidates/",
        "/api/candidates/register",
        "/api/candidates/id",
        "/api/candidates/id/delete",
    ]
    return Response(routes)


@api_view(["POST"])
def assign_cab_view(request):
    pickup_latitude = request.POST.get("pickup_latitude")
    pickup_longitude = request.POST.get("pickup_longitude")
    drop_latitude = request.POST.get("drop_latitude")
    drop_longitude = request.POST.get("drop_longitude")

    api_key = "AIzaSyCdAOn8KI6yDXfUFN39qD1B1sglBKrqCO8"

    cab = assign_cab(pickup_latitude, pickup_longitude, api_key)

    if cab:
        trip = Trip.objects.create(
            cab=Cab.objects.get(pk=cab.id),
            user=request.user,
            start_location_latitude=pickup_latitude,
            start_location_longitude=pickup_longitude,
            end_location_latitude=drop_latitude,
            end_location_longitude=drop_longitude,
            start_time=datetime.datetime.now(),
        )

        serializer = TripSerializer(trip)
        return Response(serializer.data)
    else:
        return Response({"error": "No cabs available at the moment."})


@api_view(["POST"])
def assign_sharing_cab_view(request):
    pickup_latitude = request.POST.get("pickup_latitude")
    pickup_longitude = request.POST.get("pickup_longitude")
    drop_latitude = request.POST.get("drop_latitude")
    drop_longitude = request.POST.get("drop_longitude")

    api_key = "AIzaSyCdAOn8KI6yDXfUFN39qD1B1sglBKrqCO8"

    cab = assign_sharing_cab(
        pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, api_key
    )

    if cab:
        trip = SharingTrip.objects.create(
            cab=SharingCab.objects.get(pk=cab.id),
            user=request.user,
            start_location_latitude=pickup_latitude,
            start_location_longitude=pickup_longitude,
            end_location_latitude=drop_latitude,
            end_location_longitude=drop_longitude,
            start_time=datetime.datetime.now(),
        )

        serializer = SharingTripSerializer(trip)
        return Response(serializer.data)
    else:
        return Response({"error": "No cabs available at the moment."})
