import streamlit as st
import folium
from streamlit_folium import folium_static

def display_weather(weather_data):
    """
    Display weather information
    """
    st.subheader("📅 Weather Forecast")
    
    # Group weather data by day
    daily_weather = {}
    for item in weather_data['list'][:5]:  # Show 5 days
        date = item['dt_txt'].split()[0]
        if date not in daily_weather:
            daily_weather[date] = item
    
    # Display weather for each day
    for date, weather in daily_weather.items():
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(date)
            with col2:
                st.write(f"{weather['weather'][0]['description'].capitalize()}")
            with col3:
                st.write(f"{round(weather['main']['temp'])}°C")

def display_itinerary(itinerary):
    """
    Display the AI-generated itinerary
    """
    st.subheader("🗓️ Your Personalized Itinerary")
    st.markdown(itinerary)

def display_places(places_data):
    """
    Display recommended places with an interactive map
    """
    st.subheader("📍 Recommended Places")
    
    # Create map
    if places_data['tourist_attraction']:
        first_place = places_data['tourist_attraction'][0]
        m = folium.Map(
            location=[
                first_place['geometry']['location']['lat'],
                first_place['geometry']['location']['lng']
            ],
            zoom_start=13
        )
        
        # Add markers for all places
        for category, places in places_data.items():
            for place in places:
                folium.Marker(
                    [
                        place['geometry']['location']['lat'],
                        place['geometry']['location']['lng']
                    ],
                    popup=place['name'],
                    tooltip=f"{category}: {place['name']}"
                ).add_to(m)
        
        folium_static(m)
    
    # Display places by category
    categories = {
        'tourist_attraction': '🏛️ Attractions',
        'restaurant': '🍽️ Restaurants',
        'hotel': '🏨 Hotels'
    }
    
    for category, title in categories.items():
        st.write(f"### {title}")
        for place in places_data[category]:
            with st.expander(place['name']):
                st.write(f"Rating: {'⭐' * round(place.get('rating', 0))}")
                st.write(f"Address: {place.get('vicinity', 'Not available')}")

def display_loading():
    """
    Display loading animation
    """
    with st.spinner('Creating your perfect itinerary...'):
        st.empty()
