import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
from utils.place_images import get_place_image

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
    st.subheader("🗓️ Your Daily Schedule")

    # Split itinerary into days
    days = itinerary.split('Day')

    # Create tabs for each day
    if len(days) > 1:  # Skip the first empty split
        tabs = st.tabs([f"Day {i}" for i in range(1, len(days))])
        for i, tab in enumerate(tabs):
            with tab:
                st.markdown(f"### Day {i+1}")
                # Format the day's schedule
                schedule = days[i+1].strip()
                st.markdown(schedule)

def display_place_card(place, city, category_emoji=""):
    """
    Display a place card with image and details
    """
    image_url = get_place_image(place['name'], city)

    card_html = f"""
    <div style="
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h3 style="color: #1E88E5; margin-bottom: 0.5rem;">{category_emoji} {place['name']}</h3>
    """

    if image_url:
        card_html += f'<img src="{image_url}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 0.5rem; margin: 0.5rem 0;">'

    card_html += f"""
        <p>{'⭐' * round(place.get('rating', 0))}</p>
        <p style="color: #666;"><small>{place.get('vicinity', 'Address not available')}</small></p>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)

def display_places(places_data):
    """
    Display recommended places with an interactive map
    """
    city = places_data['tourist_attraction'][0]['vicinity'].split(',')[-1].strip()

    # Display map
    if places_data['tourist_attraction']:
        st.subheader("📍 Interactive Map")
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

    # Must Visit Places
    st.markdown("### 🏛️ Must-Visit Places")
    st.markdown("<hr>", unsafe_allow_html=True)
    for place in places_data['tourist_attraction']:
        display_place_card(place, city, "🏛️")

    # Hotels
    st.markdown("### 🏨 Recommended Hotels")
    st.markdown("<hr>", unsafe_allow_html=True)
    hotel_cols = st.columns(2)
    for idx, hotel in enumerate(places_data['hotel']):
        with hotel_cols[idx % 2]:
            display_place_card(hotel, city, "🏨")

    # Restaurants
    st.markdown("### 🍽️ Popular Restaurants")
    st.markdown("<hr>", unsafe_allow_html=True)
    restaurant_cols = st.columns(2)
    for idx, restaurant in enumerate(places_data['restaurant']):
        with restaurant_cols[idx % 2]:
            display_place_card(restaurant, city, "🍽️")

def display_loading():
    """
    Display loading animation
    """
    with st.spinner('Creating your perfect itinerary...'):
        st.empty()