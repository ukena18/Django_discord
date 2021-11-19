# render a html file and redirect a html file
from django.shortcuts import render, redirect
# send a html context to frontend
from django.http import HttpResponse
# form models.py file import our models
from .models import Room, Topic, Message
# from forms.py import our custom form for RoomModel
# you can use model and form together
from .forms import RoomForm
# login_required is for function views authentication check
from django.contrib.auth.decorators import login_required
# Q is for search input  so we can interact with database faster
# you can create own functions but this is faster and django recommended it
from django.db.models import Q
# import User model  from so we can use it
# it is built-in inside django
from django.contrib.auth.models import User
# to show flash messages
from django.contrib import messages
# basic authentication check functions
# so useful and easy
from django.contrib.auth import authenticate, login, logout
# basic userCreationForm form from django
from django.contrib.auth.forms import UserCreationForm


# log out func using built-in logout func
# it delete cookies and all tokens
def logoutPage(request):
    logout(request)

    return redirect("base-home")


# register func for create new user
def register(request):
    # get the userCreationForm
    form = UserCreationForm()

    # if the method is post or not
    if request.method == "POST":
        # that is means for filled up already
        # take all infos and send to usercreationform
        form = UserCreationForm(request.POST)
        # this is form's built-in func it is checking for us
        if form.is_valid():
            # if commit=False ,we are holding save
            user = form.save(commit=False)
            # lowercase username
            user.username = user.username.lower()
            # then save it so all the usernames is gonna be lowercase
            user.save()
            # using login func we import it from built-in django
            login(request, user)
            return redirect("base-home")
        else:
            # flash messages
            messages.error(request, "error happen during registration")
    # if the request is not post  render login page and send form probs
    return render(request, "base/login_register.html", {"form": form})


# login page
def loginPage(request):
    # register and login is same html file
    # inside html file there is condition seperated which form is shown
    # page = login is making sure we are getting right form
    page = "login"
    # if user logged in successfully
    if request.user.is_authenticated:
        return redirect("base-home")
    # if it is post method
    if request.method == "POST":
        # lowercase username and get from the form
        username = request.POST.get("username").lower()
        # get the password from the form
        password = request.POST.get("password")

        # check if there is username or not
        try:
            # if there is username in databse save this value to user instance
            user = User.objects.get(username=username)
        except():
            # if not that means user doesn't exist
            messages.error(request, "User doesn't exist")
        # authenticate func from django library
        # check if password and username is matching from database
        # return true or false
        user = authenticate(request, password=password, username=username)

        # if there is user try to login
        if user is not None:
            # use login func from django library
            login(request, user)
            return redirect("base-home")
        else:
            # flash message
            messages.error(request, "Username or password doesnt exits")
    # send props if the page is login or register
    context = {"page": page}
    return render(request, "base/login_register.html", context)


# home page
def home(request):
    # this is inside navbar.html for search thing in the website
    # if there is nothing on search input it gves you empty string

    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    # since q is empty string it is returning all , means filter is not gonna effect it
    # special method for database if want to find any topic name including whatever inside q variable

    # or any name or description an search input
    rooms = Room.objects.filter(

        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    # get all the topocs
    topic = Topic.objects.all()
    # count how many room are available
    room_count = rooms.count()
    # check the room messages that including q input
    # again if q is empty string that means no filter apply
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # send all data to html file so we can use it
    context = {"rooms": rooms, "topics": topic, "room_count": room_count, "room_messages": room_messages}
    return render(request, "base/home.html", context)


# room page get room id with it
def room(request, pk):
    # find the right room which match with id that we are looking
    room = Room.objects.get(id=int(pk))
    # if we want to reach any subtable we can use <table>.<lowercaseSubTable>_set.<function>
    room_messages = room.message_set.all()
    # how many people on the room
    # it is on the database
    participants = room.participants.all()
    # if it is post request
    if request.method == 'POST':
        # another way to create a message
        message = Message.objects.create(
            # get the current username
            # in the html file it is just User
            user=request.user,
            # the room that math with the id
            room=room,
            # the bbody of message which is from the form
            body=request.POST.get("body")
        )
        # and add this user to participant  so we can keep tracking who is in the room
        room.participants.add(request.user)
        # redirect it to room with right id
        return redirect("room", pk=room.id)
    # if it is not send request  send all data to room.html file
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)


# single user profile  with user.id
def userProfile(request, pk):
    # find the right user , it is not current user profile
    # it is like facebook when you wanna see someone else profile
    user = User.objects.get(id=int(pk))
    # if we want to reach any subtable we can use <table>.<lowercaseSubTable>_set.<function>
    rooms = user.room_set.all()
    # if we want to reach any subtable we can use <table>.<lowercaseSubTable>_set.<function>
    rooms_messages = user.message_set.all()
    # find all topics
    topics = Topic.objects.all()
    # send all data to html file
    context = {"user": user, "rooms": rooms, "rooms_messages": rooms_messages, "topics": topics}
    return render(request, "base/profile.html", context)

#  in order to create you gotta login first  from django.contrib.auth.decorators import login_required
@login_required
# for creating room while you are logged in
def createRoom(request):
    # if it is post request
    if request.method == "POST":
        # use customForm and fill it up with request.POST infos
        form = RoomForm(request.POST)
        # built in func if it is valid
        if form.is_valid():
            room = form.save(commit=False)
            room.host=request.user
            # save it and redirect it
            form.save()
            return redirect("base-home")
    # if it not request.POST send blank form to html file
    form = RoomForm()
    context = {"form": form}
    return render(request, "base/room_form.html", context)

#  in order to create you gotta login first  from django.contrib.auth.decorators import login_required
# login url means if the user is not logged in send him to the "login-page" url so they can log in to see page
@login_required(login_url="login-page")
# update room with id
def updateRoom(request, pk):
    # find the right room
    room = Room.objects.get(id=int(pk))
    # to fillet it up our custom room form with current room info we can instance = room
    form = RoomForm(instance=room)

    # only room.host can update room
    if request.user != room.host:
        return HttpResponse("You Are not authentication")

    # if it is post request for updating page
    if request.method == "POST":
        # ??????????????????????????????????
        form = RoomForm(request.POST, instance=room)
        # ??????????????????????????????????????
        form.save()
        return redirect("base-home")

    context = {"form": form}
    return render(request, 'base/room_form.html', context)

#  in order to create you gotta login first  from django.contrib.auth.decorators import login_required
# login url means if the user is not logged in send him to the "login-page" url so they can log in to see page
@login_required(login_url="login-page")
def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))

    if request.user != room.host:
        return HttpResponse("You Are not authentication")

    if request.method == "POST":
        room.delete()
        return redirect("base-home")
    return render(request, 'base/delete.html', {"obj": room})

#  in order to create you gotta login first  from django.contrib.auth.decorators import login_required
# login url means if the user is not logged in send him to the "login-page" url so they can log in to see page
@login_required(login_url="login-page")
def deleteMessage(request, pk):
    user_message = Message.objects.get(id=int(pk))

    if request.user != user_message.user:
        return HttpResponse("You Are not authentication")

    if request.method == "POST":
        user_message.delete()
        return redirect("base-home")
    return render(request, 'base/delete.html', {"obj": user_message})
