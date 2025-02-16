import streamlit as st
import os
from dotenv import load_dotenv
from components.forms import render_input_form
from components.displays import (
    display_weather,
    display_itinerary,
    display_places,
    display_loading
)
from utils.api_handlers import get_weather_data, get_places_data
from utils.itinerary_generator import generate_itinerary

# Load environment variables
load_dotenv()

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Travel Planner",
        page_icon="✈️",
        layout="wide"
    )

    # Custom CSS
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Header
    st.title("✈️ AI Travel Planner")
    st.markdown("### Your Personal Travel Assistant")

    # Initialize session state
    if 'generated_plan' not in st.session_state:
        st.session_state.generated_plan = None

    # Sidebar with input form
    with st.sidebar:
        travel_details = render_input_form()

    # Main content
    if travel_details:
        try:
            with st.spinner("Planning your perfect trip..."):
                # Get weather data
                weather_data = get_weather_data(
                    travel_details['destination'],
                    os.getenv('OPENWEATHER_API_KEY')
                )
                
                # Get places data
                places_data = get_places_data(
                    travel_details['destination'],
                    travel_details['budget'],
                    os.getenv('GOOGLE_PLACES_API_KEY')
                )
                
                # Generate AI itinerary
                itinerary = generate_itinerary(
                    travel_details,
                    places_data,
                    os.getenv('OPENAI_API_KEY')
                )

                # Display results
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    display_itinerary(itinerary)
                    display_places(places_data)
                
                with col2:
                    display_weather(weather_data)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    main()
