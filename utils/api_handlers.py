import requests
import streamlit as st
from datetime import datetime, timedelta
import time

@st.cache_data(ttl=3600)
def get_weather_data(city, api_key=None):
    """
    Fetch weather data from OpenWeather API with caching
    """
    try:
        if not api_key:
            raise Exception("OpenWeather API key is required")

        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Weather API error: {str(e)}")

@st.cache_data(ttl=3600)
def get_places_data(city, budget, api_key=None):
    """
    Fetch places data from OpenStreetMap/Nominatim API (free, no authentication needed)
    """
    try:
        headers = {'User-Agent': 'TravelPlanner/1.0 (educational project)'}

        # Get city information
        city_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        response = requests.get(city_url, headers=headers)
        response.raise_for_status()

        if not response.json():
            raise Exception("City not found")

        location = response.json()[0]
        lat, lon = float(location['lat']), float(location['lon'])

        # Categories to search for
        categories = {
            'tourist_attraction': 'tourism',
            'restaurant': 'restaurant',
            'hotel': 'hotel'
        }

        all_places = {}

        for category_key, osm_tag in categories.items():
            # Respect rate limiting
            time.sleep(1)

            # Search for places in each category
            query = f"""
            [out:json][timeout:10];
            (
              node["amenity"="{osm_tag}"](around:5000,{lat},{lon});
              way["amenity"="{osm_tag}"](around:5000,{lat},{lon});
              relation["amenity"="{osm_tag}"](around:5000,{lat},{lon});
            );
            out body center;
            """

            overpass_url = "https://overpass-api.de/api/interpreter"
            response = requests.post(overpass_url, data={"data": query}, headers=headers)
            response.raise_for_status()

            places = response.json().get('elements', [])[:5]  # Get top 5 places

            # Transform to match our format
            all_places[category_key] = [
                {
                    'name': place.get('tags', {}).get('name', 'Unnamed Location'),
                    'rating': 4.0,  # Default rating since OSM doesn't provide ratings
                    'vicinity': f"{place.get('tags', {}).get('addr:street', '')}, {place.get('tags', {}).get('addr:city', city)}",
                    'geometry': {
                        'location': {
                            'lat': place.get('lat', place.get('center', {}).get('lat')),
                            'lng': place.get('lon', place.get('center', {}).get('lon'))
                        }
                    }
                }
                for place in places
                if place.get('tags', {}).get('name')
            ]

            # If no places found, add some generic ones
            if not all_places[category_key]:
                all_places[category_key] = [{
                    'name': f'Popular {category_key.replace("_", " ").title()} in {city}',
                    'rating': 4.0,
                    'vicinity': city,
                    'geometry': {
                        'location': {
                            'lat': lat,
                            'lng': lon
                        }
                    }
                }]

        return all_places

    except requests.exceptions.RequestException as e:
        raise Exception(f"Places API error: {str(e)}")