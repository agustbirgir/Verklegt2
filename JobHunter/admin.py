from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'password', 'date_joined')#remeber to take out password
    search_fields = ('first_name', 'email')
    list_filter = ('date_joined',)

admin.site.register(User, UserAdmin)

