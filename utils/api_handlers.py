import requests
import streamlit as st
from datetime import datetime, timedelta
import time
from typing import Dict, List

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

def fetch_with_retry(url: str, method: str = 'get', data: Dict = None, max_retries: int = 3, delay: int = 2) -> Dict:
    """Helper function to fetch data with retries"""
    headers = {'User-Agent': 'TravelPlanner/1.0 (educational project)'}

    for attempt in range(max_retries):
        try:
            if method.lower() == 'post':
                response = requests.post(url, headers=headers, data=data, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (attempt + 1))  # Exponential backoff

    raise Exception("Max retries reached")

@st.cache_data(ttl=3600)
def get_places_data(city: str, budget: float, api_key=None) -> Dict:
    """
    Fetch places data from OpenStreetMap/Nominatim API with improved reliability
    """
    try:
        # Get city information
        city_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        location_data = fetch_with_retry(city_url)

        if not location_data:
            return get_fallback_places(city)

        location = location_data[0]
        lat, lon = float(location['lat']), float(location['lon'])

        # Categories with fallback tags
        categories = {
            'tourist_attraction': ['tourism=attraction', 'tourism=museum', 'tourism=artwork'],
            'restaurant': ['amenity=restaurant', 'amenity=cafe'],
            'hotel': ['tourism=hotel', 'tourism=hostel']
        }

        all_places = {}

        for category_key, tags in categories.items():
            successful_places = []

            # Try each tag until we get enough places
            for tag in tags:
                if len(successful_places) >= 5:
                    break

                tag_type, tag_value = tag.split('=')
                query = f"""
                [out:json][timeout:5];
                (
                  node["{tag_type}"="{tag_value}"](around:5000,{lat},{lon});
                  way["{tag_type}"="{tag_value}"](around:5000,{lat},{lon});
                );
                out body center;
                """

                try:
                    overpass_url = "https://overpass-api.de/api/interpreter"
                    response_data = fetch_with_retry(
                        overpass_url,
                        method='post',
                        data={"data": query}
                    )

                    places = response_data.get('elements', [])

                    for place in places:
                        if len(successful_places) >= 5:
                            break

                        tags = place.get('tags', {})
                        if tags.get('name'):
                            successful_places.append({
                                'name': tags['name'],
                                'rating': 4.0,
                                'vicinity': f"{tags.get('addr:street', '')}, {tags.get('addr:city', city)}",
                                'geometry': {
                                    'location': {
                                        'lat': place.get('lat', place.get('center', {}).get('lat')),
                                        'lng': place.get('lon', place.get('center', {}).get('lon'))
                                    }
                                }
                            })

                    time.sleep(1)  # Respect rate limiting

                except Exception as e:
                    st.warning(f"Error fetching {tag}: {str(e)}")
                    continue

            # If we still don't have enough places, add some from our fallback
            if not successful_places:
                successful_places = get_fallback_places(city)[category_key]

            all_places[category_key] = successful_places

        return all_places

    except Exception as e:
        st.warning(f"Using fallback data due to API error: {str(e)}")
        return get_fallback_places(city)

def get_fallback_places(city: str) -> Dict:
    """Provide fallback place data when API fails"""
    lat, lon = 0, 0  # Default coordinates

    try:
        # Try to get basic coordinates for the city
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search?city={city}&format=json",
            headers={'User-Agent': 'TravelPlanner/1.0'},
            timeout=5
        )
        if response.ok and response.json():
            lat = float(response.json()[0]['lat'])
            lon = float(response.json()[0]['lon'])
    except:
        pass

    return {
        'tourist_attraction': [
            {
                'name': f'Popular Tourist Spot in {city}',
                'rating': 4.0,
                'vicinity': city,
                'geometry': {'location': {'lat': lat, 'lng': lon}}
            },
            {
                'name': f'Historic Site in {city}',
                'rating': 4.5,
                'vicinity': city,
                'geometry': {'location': {'lat': lat, 'lng': lon}}
            }
        ],
        'restaurant': [
            {
                'name': f'Local Restaurant in {city}',
                'rating': 4.0,
                'vicinity': city,
                'geometry': {'location': {'lat': lat, 'lng': lon}}
            },
            {
                'name': f'Popular Café in {city}',
                'rating': 4.2,
                'vicinity': city,
                'geometry': {'location': {'lat': lat, 'lng': lon}}
            }
        ],
        'hotel': [
            {
                'name': f'Central Hotel in {city}',
                'rating': 4.0,
                'vicinity': city,
                'geometry': {'location': {'lat': lat, 'lng': lon}}
            },
            {
                'name': f'Boutique Hotel in {city}',
                'rating': 4.3,
                'vicinity': city,
                'geometry': {'location': {'lat': lat, 'lng': lon}}
            }
        ]
    }