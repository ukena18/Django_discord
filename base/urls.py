from django.urls import path
from . import views


urlpatterns = [
    path("login/",views.loginPage,name="login-page"),
    path("logout/",views.logoutPage,name="logout-page"),
    path("register/",views.register,name="register-page"),


    path('', views.home,name="base-home"),

    path('room/<str:pk>/', views.room,name="room"),
    path('update/<str:pk>/', views.updateRoom,name="update-room"),
    path('delete/<str:pk>/', views.deleteRoom,name="delete-room"),
    path('create-room', views.createRoom,name="create"),


    path('profile/<str:pk>', views.userProfile,name="user-profile"),
path('update-user/', views.updateUser,name="update-user"),


path('delete-message/<str:pk>/', views.deleteMessage,name="delete-message"),

path('topics/', views.topicPage,name="topic-page"),
path('activity/', views.activityPAge,name="activity-page"),


]
