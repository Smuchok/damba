from django.contrib import admin

# Register your models here.
# from django.contrib.admin.models import LogEntry
# LogEntry.objects.all().delete()

from .models import *

class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Price, PriceAdmin)
admin.site.register(Category, CategoryAdmin)


class HousesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'capacity', 'rooms', 'pets_allow')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = (
        'price', 'capacity', 'wifi', 'kitchen','bathroom',
        'central_heat', 'pets_allow'
        )
    list_editable = ('pets_allow',)

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'house_id', 'date_future_settlment', 'date_future_checkout')
    list_display_links = ('id', 'client_id', 'house_id')
    search_fields = ('client_id', 'house_id')
    list_filter = ('date_future_settlment', 'date_future_checkout')

class SettlmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'house_id', 'date_of_settlment', 'date_of_checkout')
    list_display_links = ('id', 'client_id', 'house_id')
    search_fields = ('client_id', 'house_id')
    list_filter = ('date_of_settlment', 'date_of_checkout')



admin.site.register(Houses, HousesAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Settlment, SettlmentAdmin)
