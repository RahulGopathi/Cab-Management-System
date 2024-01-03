import requests

from main.models import Cab


def get_distance_from_maps_api(
    api_key, origin_lat, origin_lon, destination_lat, destination_lon
):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{origin_lat},{origin_lon}",
        "destinations": f"{destination_lat},{destination_lon}",
        "key": api_key,
    }

    if origin_lat == destination_lat and origin_lon == destination_lon:
        return 0
    else:
        print("params", params)
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)

        if data["rows"][0]["elements"][0]["status"] == "OK":
            # Extract distance in meters from the response
            distance = data["rows"][0]["elements"][0]["distance"]["value"]
            print("Distance:", distance)
            return distance
        else:
            print("Error fetching distance:", data["status"])
            print(params)
            return None


def assign_cab(pickup_latitude, pickup_longitude, api_key):
    # Fetch all available cabs from the database
    available_cabs = Cab.objects.filter(is_available=True, is_on_trip=False)

    # Initialize variables for the shortest distance and the cab to be assigned
    shortest_distance = float("inf")
    assigned_cab = None

    # Iterate through available cabs and calculate distances using Google Maps API
    for cab in available_cabs:
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

    # If a cab is found, update its status
    if assigned_cab:
        assigned_cab.is_assigned = True
        assigned_cab.is_on_trip = True
        assigned_cab.save()
        return assigned_cab
    else:
        print("No available cabs at the moment.")
        return None
