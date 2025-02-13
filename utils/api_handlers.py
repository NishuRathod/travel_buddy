import requests
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def get_weather_data(city, api_key=None):
    """
    Fetch weather data from WeatherAPI.com (free tier)
    """
    try:
        # Using WeatherAPI.com free tier
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        params = {
            "q": city,
            "days": 5,
            "key": "7f6b9a1a8c024f7485374055232502"  # Free API key with limited requests
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # Transform response to match our format
        data = response.json()
        return {
            'list': [
                {
                    'dt_txt': day['date'],
                    'main': {'temp': day['day']['avgtemp_c']},
                    'weather': [{'description': day['day']['condition']['text']}]
                }
                for day in data['forecast']['forecastday']
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
                    'name': place['name'],
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