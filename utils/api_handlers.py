import requests
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def get_weather_data(city, api_key):
    """
    Fetch weather data from OpenWeather API with caching
    """
    try:
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
def get_places_data(city, budget, api_key):
    """
    Fetch places data from Google Places API with caching
    """
    try:
        # First, get place ID for the city
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": city,
            "key": api_key
        }
        response = requests.get(geocode_url, params=params)
        response.raise_for_status()
        location_data = response.json()
        
        if not location_data['results']:
            raise Exception("City not found")
            
        location = location_data['results'][0]['geometry']['location']
        
        # Then, search for places
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        # Define price level based on budget
        if budget < 100:
            max_price = 1
        elif budget < 200:
            max_price = 2
        else:
            max_price = 3
            
        categories = ['tourist_attraction', 'restaurant', 'hotel']
        all_places = {}
        
        for category in categories:
            params = {
                "location": f"{location['lat']},{location['lng']}",
                "radius": 5000,
                "type": category,
                "maxprice": max_price,
                "key": api_key
            }
            
            response = requests.get(places_url, params=params)
            response.raise_for_status()
            all_places[category] = response.json()['results'][:5]
            
        return all_places
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Places API error: {str(e)}")
