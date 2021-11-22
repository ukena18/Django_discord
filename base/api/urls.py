from django.urls import path
from . import views



urlpatterns = [
    path("",views.getRoute,name="all-api"),
    path("rooms",views.getRooms,name="all-rooms-api"),
    path("room/<str:pk>",views.getRoom,name="room-api"),


]