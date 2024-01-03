import requests

from main.models import SharingCab
from main.algorithm import get_distance_from_maps_api


def assign_sharing_cab(
    pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, api_key
):
    assigned_cab = None
    empty_available_cabs = SharingCab.objects.filter(
        is_available=True, is_on_trip=False, is_empty=True
    )
    if empty_available_cabs:
        print("Providing empty cab")
        # Initialize variables for the shortest distance and the cab to be assigned
        shortest_distance = float("inf")

        # Iterate through available cabs and calculate distances using Google Maps API
        for cab in empty_available_cabs:
            distance = get_distance_from_maps_api(
                api_key,
                pickup_latitude,
                pickup_longitude,
                cab.location_latitude,
                cab.location_longitude,
            )

            # Update the assigned cab if the distance is shorter
            if distance is not None and distance < shortest_distance:
                shortest_distance = distance
                assigned_cab = cab

        # If a cab is found, update its status to 'booked' and return it
        if assigned_cab:
            assigned_cab.is_assigned = True
            assigned_cab.is_empty = False
            assigned_cab.is_on_trip = True
            assigned_cab.passenger1_pickup_location_latitude = pickup_latitude
            assigned_cab.passenger1_pickup_location_longitude = pickup_longitude
            assigned_cab.passenger1_drop_location_latitude = drop_latitude
            assigned_cab.passenger1_drop_location_longitude = drop_longitude
            assigned_cab.save()
            return assigned_cab
    else:
        print("Providing filled cab")
        # Fetch all available cabs from the database
        available_cabs = SharingCab.objects.filter(
            is_available=True, is_on_trip=True, is_filled=False, is_empty=False
        )

        # Initialize variables for the shortest distance and the cab to be assigned
        least_deviation = float("inf")

        # Iterate through available cabs and calculate distances using Google Maps API
        for cab in available_cabs:
            print("cab", cab)
            x = get_distance_from_maps_api(
                api_key,
                pickup_latitude,
                pickup_longitude,
                cab.location_latitude,
                cab.location_longitude,
            )

            print("x", x)

            c = get_distance_from_maps_api(
                api_key,
                cab.location_latitude,
                cab.location_longitude,
                cab.passenger1_drop_location_latitude,
                cab.passenger1_drop_location_longitude,
            )

            print("c", c)

            a = get_distance_from_maps_api(
                api_key,
                pickup_latitude,
                pickup_longitude,
                cab.passenger1_drop_location_latitude,
                cab.passenger1_drop_location_longitude,
            )

            print("a", a)

            b = get_distance_from_maps_api(
                api_key,
                pickup_latitude,
                pickup_longitude,
                drop_latitude,
                drop_longitude,
            )

            print("b", b)

            k = get_distance_from_maps_api(
                api_key,
                cab.passenger1_drop_location_latitude,
                cab.passenger1_drop_location_longitude,
                drop_latitude,
                drop_longitude,
            )
            print("k", k)

            if x is None or c is None or a is None or b is None or k is None:
                continue

            extra_distance_for_p1_p2_after_dropof_p1 = abs(x + a - c) + abs(a + k - b)
            extra_distance_for_p1_after_dropof_p2 = abs(x + b + k - c)
            extra_distance_for_picking_p2_after_dropof_p1 = abs(c + a - x)

            min_extra_distance = min(
                extra_distance_for_p1_p2_after_dropof_p1,
                extra_distance_for_p1_after_dropof_p2,
                extra_distance_for_picking_p2_after_dropof_p1,
            )

            if min_extra_distance < least_deviation:
                least_deviation = min_extra_distance
                assigned_cab = cab

    # If a cab is found, update its status
    if assigned_cab:
        assigned_cab.is_assigned = True
        assigned_cab.is_filled = True
        assigned_cab.save()
        return assigned_cab
    else:
        print("No available sharing cabs at the moment.")
        return None
