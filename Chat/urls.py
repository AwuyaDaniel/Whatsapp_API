from django.urls import path
from .views import ChatRoomViewSet, AddChatRoom, LeaveChatroom, EnterChatroom, AddMessage, MessageViewSet


urlpatterns = [
    path('chatrooms/', ChatRoomViewSet.as_view(), name='chatrooms'),
    path('addchatroom/', AddChatRoom.as_view(), name='addchatroom'),
    path('leavechatroom/', LeaveChatroom.as_view(), name='leavechatroom'),
    path('enterchatroom/', EnterChatroom.as_view(), name='enterchatroom'),
    path('sendmessage/', AddMessage.as_view(), name='sendmessage'),
    path('messages/', MessageViewSet.as_view(), name='messages'),
]
