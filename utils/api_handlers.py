import requests
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def get_weather_data(city, api_key=None):
    """
    Fetch weather data from Open-Meteo API (completely free, no authentication needed)
    """
    try:
        # First get coordinates for the city using Nominatim (OpenStreetMap)
        geocoding_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        headers = {'User-Agent': 'TravelPlanner/1.0'}
        geo_response = requests.get(geocoding_url, headers=headers)
        geo_response.raise_for_status()

        if not geo_response.json():
            raise Exception("City not found")

        location = geo_response.json()[0]
        lat, lon = float(location['lat']), float(location['lon'])

        # Get weather data from Open-Meteo
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,weathercode&timezone=auto"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Convert weather codes to descriptions
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Light snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm"
        }

        # Transform to match our expected format
        return {
            'list': [
                {
                    'dt_txt': date,
                    'main': {'temp': temp},
                    'weather': [{
                        'description': weather_codes.get(code, "Unknown")
                    }]
                }
                for date, temp, code in zip(
                    weather_data['daily']['time'],
                    weather_data['daily']['temperature_2m_max'],
                    weather_data['daily']['weathercode']
                )
            ]
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Weather API error: {str(e)}")

@st.cache_data(ttl=3600)
def get_places_data(city, budget, api_key=None):
    """
    Fetch places data from OpenTripMap API (free tier)
    """
    try:
        # Using OpenTripMap API free tier
        API_KEY = "5ae2e3f221c38a28845f05b6e387458371aa4704f3c1a817dd4c5954"  # Free API key

        # First, get city coordinates
        geourl = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={API_KEY}"
        response = requests.get(geourl)
        response.raise_for_status()
        location = response.json()

        if not location.get('lat'):
            raise Exception("City not found")

        # Get places around the location
        radius = 5000  # 5km radius
        categories = {
            'tourist_attraction': 'interesting_places',
            'restaurant': 'restaurants',
            'hotel': 'accomodations'
        }

        all_places = {}

        for category_key, category_value in categories.items():
            places_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={location['lon']}&lat={location['lat']}&kinds={category_value}&format=json&apikey={API_KEY}"
            response = requests.get(places_url)
            response.raise_for_status()
            places = response.json()[:5]  # Get top 5 places

            # Transform to match our format
            all_places[category_key] = [
                {
                    'name': place['name'] or "Unnamed Location",
                    'rating': float(place.get('rate', 0)) * 2,  # Convert to 5-star scale
                    'vicinity': f"{place.get('kinds', '').replace(',', ', ')}",
                    'geometry': {
                        'location': {
                            'lat': place['point']['lat'],
                            'lng': place['point']['lon']
                        }
                    }
                }
                for place in places if place.get('name')
            ]

        return all_places

    except requests.exceptions.RequestException as e:
        raise Exception(f"Places API error: {str(e)}")