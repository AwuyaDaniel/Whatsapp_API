from rest_framework import serializers
from .models import *


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class AddChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        exclude = ['user']

    def create(self, validated_data):
        return ChatRoom.objects.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class AddMessageSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    class Meta:
        model = Message
        exclude = ['user']

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
