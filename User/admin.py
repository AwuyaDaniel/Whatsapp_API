from django.contrib import admin
from .models import *
from rest_framework.authtoken.models import Token


# Register your models here.
admin.site.register(CustomUser)
# admin.site.register(Token)
