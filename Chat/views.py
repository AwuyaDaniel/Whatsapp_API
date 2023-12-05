from rest_framework.parsers import MultiPartParser
from drf_yasg import openapi
from rest_framework.decorators import api_view, parser_classes, action
from rest_framework.parsers import FileUploadParser, FormParser
from rest_framework.views import APIView
from .serializers import ChatRoomSerializer, AddChatRoomSerializer, AddMessageSerializer, MessageSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .service.service import ChatRoomService, MessageService
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
def get_user(token, authentication):
    # Get User Information through Token
    token_obj = token.objects.get(key=authentication[1])
    user_info = token_obj.user
    return user_info


def check_request_arguments(req, fields: list):
    # Check if all fields are added to the request
    try:
        unavailable_fields = [field for field in fields if not req.data.get(field)]
        if not unavailable_fields:
            return {"status": True, "unavailable_fields": unavailable_fields}
        else:
            return {"status": False, "unavailable_fields": unavailable_fields}
    except Exception as E:
        return {"status": False, "unavailable_fields": E}


class ChatRoomViewSet(ListAPIView):
    """
        View All Chat Rooms

        **View All Chat Room**
        This endpoint retrieves a list of all available chat rooms within the system. There are no requirement for this endpoint

        **Usage**
        GET /chat/chatrooms/

        **Response**
        200 OK: Successfully retrieved a list of chat rooms.
        401 Unauthorized: User authentication is required.
        500 Internal Server Error

        """

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = ChatRoomSerializer

    def get(self, request, *args, **kwargs):

        try:
            if not request.user:
                authentication_classes = [TokenAuthentication]
                permission_classes = [IsAuthenticated]
            response = ChatRoomService.get_all_chat_rooms(self, request, *args, **kwargs)
            return response
        except Token.DoesNotExist:
            return Response({"Error", "Invalid token"})


class AddChatRoom(generics.CreateAPIView):
    """
        Add a Chat Rooms

        **Add a Chat Rooms**
        This endpoint helps add a  chat room within the system, you can only add one chat room at a time and not mutiple. When a chat room is created the user creatng the chat room will be automatically added to the group

        **Requirements**
        **name**: This will be the name of the chat room to be created on the system
        **max_members**: this will be the number of users that can be allowed to be in the chat room. default value will result to max number of 10

        **Usage**
        POST /chat/addchatroom/

        **Response**
        200 OK: Successfully added a chat room.
        401 Unauthorized: User authentication is required.
        500 Internal Server Error

        """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AddChatRoomSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            if not request.user:
                authentication_classes = [TokenAuthentication]
                permission_classes = [IsAuthenticated]
            chat_room_response = ChatRoomService.create_chat_room(self, request, *args, **kwargs)
            return chat_room_response
        except Exception as E:
            response = {
                'status': 'Error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)


class LeaveChatroom(APIView):
    """
            Remove Logged in user from a chat room

            **Remove Logged in user from a chat room**
            This endpoint helps a user leave a chat room, the system tends to use the \
            logged in user information and removes that user from the chat room

            **Requirements**
            **name**: This will be the name of the chat room the user will be removed from

            **Usage**
            PUT /chat/leavechatroom/

            **Response**
            200 OK: Successfully removed the logged in user from the chat room.
            401 Unauthorized: User authentication is required.
            500 Internal Server Error
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='', required=True),
        ]
    )
    def put(self, request):
        try:
            if not request.user:
                authentication_classes = [TokenAuthentication]
                permission_classes = [IsAuthenticated]
            leave_chat_room = ChatRoomService.leave_chat_room(self, request)
            return leave_chat_room
        except Exception as E:
            response = {
                'status': 'Error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)


class EnterChatroom(APIView):
    """
        Enter Logged in user to a chat room

        **Enter Logged in user to a chat room**
        This endpoint helps a user Enter into a chat room, the system tends to use the \
        logged in user information and add that user to the chat room

        **Requirements**
        **name**: This will be the name of the chat room the user will be removed from

        **Usage**
        PUT /chat/enterchatroom/

        **Response**
        200 OK: Successfully removed the logged in user from the chat room.
        401 Unauthorized: User authentication is required.
        500 Internal Server Error
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    parser_classes = [MultiPartParser]


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='', required=True),
        ]
    )
    def put(self, request):
        try:
            if not request.user:
                authentication_classes = [TokenAuthentication]
                permission_classes = [IsAuthenticated]
            chat_room_response = ChatRoomService.enter_chat_room(self, request)
            return chat_room_response
        except Exception as E:
            response = {
                'status': 'Error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)


class AddMessage(generics.CreateAPIView):
    """
        Send a Message from the Logged in user to a specified Chart Room

        **Send a Message from the Logged in user to a specified Chart Room**
        This endpoint helps a user Sent a message to a chat room,  the system uses the \
        logged in user information and sends a message to a chat room chat room

        **Requirements**
        **name**: This will be the name of the chat room the user message will be sent to
        **message**: This will be message from the user
        **picture**: This will image file of the user
        **video**: This will be the video file of the user

        **Usage**
        POST /chat/sendmessage/

        **Response**
        200 OK: Successfully sent a message to the chat room.
        401 Unauthorized: User authentication is required.
        500 Internal Server Error
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AddMessageSerializer
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('chat_room', openapi.IN_FORM, type=openapi.TYPE_STRING, description='', required=True),
            openapi.Parameter('message', openapi.IN_FORM, type=openapi.TYPE_STRING, description='', required=True),
        ]
    )
    def post(self, request, *args, **kwargs):
        try:
            if not request.user:
                authentication_classes = [TokenAuthentication]
                permission_classes = [IsAuthenticated]
            message_response = MessageService.create_message(self, request,  *args, **kwargs)
            return message_response
        except Exception as E:
            response = {
                'status': 'Error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }
            print(E)
            return Response(response)


class MessageViewSet(ListAPIView):
    """
        get all Messages

        **View All Messages**
        This endpoint helps to get all messages on the system


        **Usage**
        GET /chat/messages/

        **Response**
        200 OK: Successful.
        401 Unauthorized: User authentication is required.
        500 Internal Server Error
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        try:
            if not request.user:
                authentication_classes = [TokenAuthentication]
                permission_classes = [IsAuthenticated]
            messages_response = MessageService.get_all_messages(self, request)
            return messages_response
        except Token.DoesNotExist:
            return Response({"error", "Invalid token"})
