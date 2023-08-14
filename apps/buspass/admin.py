from django.contrib import admin
from .models import BusStop, Bus, UserBusPass, Notification

# Register your models here.

class BusStopAdmin(admin.ModelAdmin):
    """Admin interface to manage coupon types."""

    list_display = ('id', 'name', 'distance_from_college')
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(BusStop, BusStopAdmin)


class BusAdmin(admin.ModelAdmin):
    """Admin interface to manage coupon types."""

    list_display = ('id', 'bus_number', 'destination')
    list_filter = ('bus_number',)
    search_fields = ('bus_number',)

admin.site.register(Bus, BusAdmin)

class UserBusPassAdmin(admin.ModelAdmin):
    """Admin interface to manage coupon types."""

    list_display = ('id', 'user', 'bus', 'boarding_point', 'created_at', 'expire_at', 'fare', 'active')
    list_filter = ('user',)
    search_fields = ('user',)

admin.site.register(UserBusPass, UserBusPassAdmin)

admin.site.register(Notification)