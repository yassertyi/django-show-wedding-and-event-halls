from django.contrib import admin
from .models import Halls, Client, Shar


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name']
   

@admin.register(Halls)
class HallAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'capacity', 'price', 'address', 'active']
    list_filter = ['capacity', 'price', 'address', 'active']
    search_fields = ['name', 'body']


@admin.register(Shar)
class SharAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'halls', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
