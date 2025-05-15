from geopy.geocoders import Nominatim
from tqdm import tqdm
import time

def get_city_coordinates(city_list, country='Poland'):
    geolocator = Nominatim(user_agent="tsp_analysis")
    coordinates = {}

    for city in tqdm(city_list, desc="Pobieranie współrzędnych"):
        try:
            location = geolocator.geocode(f"{city}, {country}", timeout=10)
            if location:
                coordinates[city] = (location.latitude, location.longitude)
            else:
                coordinates[city] = (None, None)
        except Exception as e:
            print(f"Błąd dla {city}: {e}")
            coordinates[city] = (None, None)
            time.sleep(1)
    
    return {k: v for k, v in coordinates.items() if v[0] is not None}
