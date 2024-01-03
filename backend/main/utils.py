import requests

import polyline


def get_google_maps_route(api_key, origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        # Extract and use the polyline points from the route
        polyline_points = data["routes"][0]["overview_polyline"]["points"]
        return polyline_points
    else:
        print("Error fetching route:", data["status"])
        return None


route_polyline = get_google_maps_route(
    "AIzaSyCdAOn8KI6yDXfUFN39qD1B1sglBKrqCO8",
    "17.4965, 78.3730",
    "17.4367, 78.4007",
)
decoded_route = polyline.decode(route_polyline)
print(len(decoded_route))
