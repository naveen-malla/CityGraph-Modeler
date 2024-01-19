import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city_center(city_name):
    try:
        geolocator = Nominatim(user_agent="unique_user_agent")
        location = geolocator.geocode(city_name + ", Germany", timeout=10)
        return (location.latitude, location.longitude) if location else (None, None)
    except (GeocoderTimedOut, GeocoderUnavailable):
        return (None, None)

# List of German cities - replace with a complete list
german_cities = ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig", "Bremen", "Dresden", "Hanover", "Nuremberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster"]

city_centers = {}

for city in german_cities:
    lat, lon = get_city_center(city)
    if lat and lon:
        city_centers[city] = (lat, lon)
    time.sleep(1)  # To prevent rate limiting

for city, coords in city_centers.items():
    print(f"{city}: {coords}")
