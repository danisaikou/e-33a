from django.contrib import admin

# Register your models here.
from .models import User, Posts

admin.site.register(User)
