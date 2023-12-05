import base64

from django.db import models
from django.utils import timezone
from User.models import CustomUser


# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=225, unique=True)
    user = models.ManyToManyField(CustomUser, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    max_members = models.PositiveIntegerField(null=True, blank=True, default=10)

    def save(self, *args, **kwargs):
        # Update the "updated_on" field before saving
        self.updated_on = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='image')
    video = models.FileField(null=True, blank=True, upload_to='video')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update the "updated_on" field before saving
        self.updated_on = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + " " + str(self.chat_room.name)
