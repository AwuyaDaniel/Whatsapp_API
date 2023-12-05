# services.py
from django.http import JsonResponse
from copy import deepcopy
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import QueryDict
from ..models import ChatRoom, Message
from ..serializers import ChatRoomSerializer, AddChatRoomSerializer, MessageSerializer, AddMessageSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
import base64


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


class ChatRoomService:
    def get_all_chat_rooms(self, request, *args, **kwargs):
        # Logic to fetch all chat rooms
        if not request.user:
            authentication = request.headers.get('Authorization', '').split()
            user = get_user(Token, authentication)
        else:
            user = request.user
        if user:
            chat_rooms = ChatRoom.objects.all().order_by('created_on')
            paginator = self.pagination_class()
            paginated_schools = paginator.paginate_queryset(chat_rooms, request)
            serializer = ChatRoomSerializer(paginated_schools, many=True)

            return Response(serializer.data)
        else:
            return Response(
                {'error': f'User: {user.username} do not have the required permission to access this Information'},
                status.HTTP_400_BAD_REQUEST)

    def create_chat_room(self, request, *args, **kwargs):
        # Logic to create a chat room
        data = check_request_arguments(request, ['name'])

        try:
            instance = ChatRoom.objects.get(name=request.data.get('name'))
            if instance:
                return Response({'detail': f'Record {request.data.get("name")} Already Exist'}, status=404)
        except ChatRoom.DoesNotExist:
            pass

        if not data['status']:
            return Response({'error': f'The following field(s) are required', 'field(s)': data["unavailable_fields"]},
                            status.HTTP_400_BAD_REQUEST)
        else:
            if not request.user:
                authentication = request.headers.get('Authorization', '').split()
                token_obj = Token.objects.get(key=authentication[1])
                user = token_obj.user
            else:
                user = request.user

            if user.is_superuser or user.is_active:
                chatroom = self.create(request, *args, **kwargs)
                chatroom_instance = ChatRoom.objects.get(pk=chatroom.data['id'])
                chatroom_instance.user.add(user)
                serializer = AddChatRoomSerializer(chatroom_instance)
                serialized_data = serializer.data
                return JsonResponse(serialized_data)
            else:
                return Response({'error': f'You Do Not have permission to make this request'},
                                status.HTTP_400_BAD_REQUEST)

    def leave_chat_room(self, request):
        try:
            instance = ChatRoom.objects.get(name=request.data.get('name'))
        except ChatRoom.DoesNotExist:
            return Response({'detail': 'Record not found'}, status=404)

        if not request.user:
            authentication = request.headers.get('Authorization', '').split()
            token_obj = Token.objects.get(key=authentication[1])
            user = token_obj.user
        else:
            user = request.user
        instance.user.remove(user)
        serializer = ChatRoomSerializer(instance, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def enter_chat_room(self, request):
        try:
            instance = ChatRoom.objects.get(name=request.data.get('name'))
            if instance.max_members <= instance.user.count():
                return Response({'detail': f'Maximum Users in Chat Room {request.data.get("name")} Has Been Reached'}, status=404)

        except ChatRoom.DoesNotExist:
            return Response({'detail': 'Record not found'}, status=404)

        if not request.user:
            authentication = request.headers.get('Authorization', '').split()
            token_obj = Token.objects.get(key=authentication[1])
            user = token_obj.user
        else:
            user = request.user
        instance.user.add(user)
        serializer = ChatRoomSerializer(instance, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class MessageService:
    def get_all_messages(self, request):
        # Logic to fetch all message
        if not request.user:
            authentication = request.headers.get('Authorization', '').split()
            token_obj = Token.objects.get(key=authentication[1])
            user = token_obj.user
        else:
            user = request.user
        if user:
            message = Message.objects.all().order_by('created_on')
            paginator = self.pagination_class()
            paginated_schools = paginator.paginate_queryset(message, request)
            serializer = MessageSerializer(paginated_schools, many=True)

            return Response(serializer.data)
        else:
            return Response(
                {'error': f'User: {user.username} do not have the required permission to access this Information'},
                status.HTTP_400_BAD_REQUEST)

    def create_message(self, request, *args, **kwargs):
        # Logic to create a message
        data = check_request_arguments(request, ['message', 'chat_room'])
        if not data['status']:
            return Response({'error': f'The following field(s) are required', 'field(s)': data["unavailable_fields"]},
                            status.HTTP_400_BAD_REQUEST)
        else:
            if not request.user:
                authentication = request.headers.get('Authorization', '').split()
                token_obj = Token.objects.get(key=authentication[1])
                user = token_obj.user
            else:
                user = request.user
            if user.is_superuser or user.is_active:
                try:
                    chat_room_instance = ChatRoom.objects.get(name=request.data.get('chat_room'))
                except ChatRoom.DoesNotExist:
                    return Response({'detail': 'Record not found'}, status=404)

                if request.data.get('image'):
                    message = Message.objects.create(user_id=user.id, chat_room=chat_room_instance, image=request.data.get('image'))
                elif request.data.get('video'):
                    message = Message.objects.create(user_id=user.id, chat_room=chat_room_instance,video=request.data.get('video'))
                elif request.data.get('video') and request.data.get('image'):
                    message = Message.objects.create(user_id=user.id, chat_room=chat_room_instance,
                                                     video=request.data.get('video'), image=request.data.get('image'))
                else:
                    message = Message.objects.create(user_id=user.id, chat_room=chat_room_instance)
                    message.save()
                message_instance = Message.objects.get(pk=message.id)
                serializer = MessageSerializer(message_instance)
                serialized_data = serializer.data
                return JsonResponse(serialized_data)
            else:
                return Response({'error': f'You Do Not have permission to make this request'},
                                status.HTTP_400_BAD_REQUEST)

    # Add other methods as needed for message operations
