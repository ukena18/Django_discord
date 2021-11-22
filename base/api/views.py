from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(["GET"])
def getRoute(request):
    routes = [
        "GET /api/",
        "GET /api/rooms",
        "GET /api/rooms/:id",

    ]
    return Response(routes,)

@api_view(["GET"])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    print(serializer)
    return Response(serializer.data)

@api_view(["GET"])
def getRoom(request,pk):
    room = Room.objects.get(id=int(pk))
    serializer = RoomSerializer(room)
    print(serializer)
    return Response(serializer.data)