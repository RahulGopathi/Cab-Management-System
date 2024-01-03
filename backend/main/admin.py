from main.models import Cab, SharingCab, Driver, Trip, SharingTrip
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class CabAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "is_available", "is_on_trip")
    list_filter = ("type", "is_available", "is_on_trip")
    search_fields = ("name", "type")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "location_latitude",
                    "location_longitude",
                    "is_available",
                    "is_on_trip",
                )
            },
        ),
        (
            _("Trip Details"),
            {
                "classes": ("collapse",),
                "fields": (
                    "start_location",
                    "end_location",
                    "trip_start_time",
                    "trip_end_time",
                ),
            },
        ),
    )


class SharingCabAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "is_available", "is_on_trip")
    list_filter = ("type", "is_available", "is_on_trip")
    search_fields = ("name", "type")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "location_latitude",
                    "location_longitude",
                    "is_available",
                    "is_on_trip",
                    "is_empty",
                    "is_filled",
                )
            },
        ),
        (
            _("Passenger 1 Details"),
            {
                "classes": ("collapse",),
                "fields": (
                    "passenger1_pickup_location_latitude",
                    "passenger1_pickup_location_longitude",
                    "passenger1_drop_location_latitude",
                    "passenger1_drop_location_longitude",
                ),
            },
        ),
        (
            _("Trip Details"),
            {
                "classes": ("collapse",),
                "fields": (
                    "start_location",
                    "end_location",
                    "trip_start_time",
                    "trip_end_time",
                ),
            },
        ),
    )


class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "cab", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name",)


class TripAdmin(admin.ModelAdmin):
    list_display = ("cab", "driver", "start_time", "end_time", "is_completed")
    list_filter = ("is_completed",)
    search_fields = ("cab", "driver", "start_location", "end_location")


class SharingTripAdmin(admin.ModelAdmin):
    list_display = ("cab", "driver", "start_time", "end_time", "is_completed")
    list_filter = ("is_completed",)
    search_fields = ("cab", "driver", "start_location", "end_location")


admin.site.register(Cab, CabAdmin)
admin.site.register(SharingCab, SharingCabAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(SharingTrip, SharingTripAdmin)
