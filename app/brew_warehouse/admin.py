from django.contrib import admin
from .models import WarehouseItem

@admin.register(WarehouseItem)
class WarehouseItemAdmin(admin.ModelAdmin):

    list_display = (
        'pk', 'title', 'content', 'quantity'
    )