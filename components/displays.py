import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

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

        # Display map
        folium_static(m)

    # Display hotels first with prominent styling
    st.markdown("### 🏨 Available Hotels")
    st.markdown("<hr>", unsafe_allow_html=True)
    for hotel in places_data['hotel']:
        st.markdown(f"""
        <div style="
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 2px solid #1E88E5;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
        ">
            <h3 style="color: #1E88E5; margin-bottom: 0.5rem;">{hotel['name']}</h3>
            <p>{'⭐' * round(hotel.get('rating', 0))}</p>
            <p style="color: #666;"><small>{hotel.get('vicinity', 'Address not available')}</small></p>
        </div>
        """, unsafe_allow_html=True)

    # Display other places by category
    other_categories = {
        'tourist_attraction': '🏛️ Places to Visit',
        'restaurant': '🍽️ Where to Eat'
    }

    for category, title in other_categories.items():
        st.markdown(f"### {title}")
        st.markdown("<hr>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, place in enumerate(places_data[category]):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="
                    padding: 1rem;
                    border-radius: 0.5rem;
                    border: 1px solid #ddd;
                    margin-bottom: 1rem;
                    background-color: white;
                ">
                    <h4 style="margin-bottom: 0.5rem;">{place['name']}</h4>
                    <p>{'⭐' * round(place.get('rating', 0))}</p>
                    <p style="color: #666;"><small>{place.get('vicinity', 'Address not available')}</small></p>
                </div>
                """, unsafe_allow_html=True)

def display_loading():
    """
    Display loading animation
    """
    with st.spinner('Creating your perfect itinerary...'):
        st.empty()