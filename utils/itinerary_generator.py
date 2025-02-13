import openai
import streamlit as st

@st.cache_data(ttl=3600)
def generate_itinerary(travel_details, places_data, api_key=None):
    """
    Generate simple itinerary using OpenAI with optimized prompt
    """
    try:
        if api_key:
            openai.api_key = api_key
        else:
            # Return a sample itinerary if no API key is provided
            return generate_sample_itinerary(travel_details, places_data)

        # Create a concise prompt to minimize token usage
        attractions = ', '.join([place['name'] for place in places_data['tourist_attraction']])
        restaurants = ', '.join([place['name'] for place in places_data['restaurant']])
        hotels = ', '.join([place['name'] for place in places_data['hotel']])

        prompt = f"""Create a {travel_details['duration']}-day itinerary for {travel_details['group_size']} people in {travel_details['destination']}.
Budget: ${travel_details['budget']}/day
Attractions: {attractions}
Restaurants: {restaurants}
Hotels: {hotels}
Format: Daily schedule with timing and estimated costs."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a concise travel planner."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500  # Limit response size
        )

        return response.choices[0].message['content']

    except Exception as e:
        return generate_sample_itinerary(travel_details, places_data)

def generate_sample_itinerary(travel_details, places_data):
    """
    Generate a sample itinerary when OpenAI is not available
    """
    days = []
    attractions = places_data['tourist_attraction']
    restaurants = places_data['restaurant']
    hotels = places_data['hotel']

    for day in range(1, travel_details['duration'] + 1):
        daily_plan = f"""Day {day}:
9:00 AM - Start at {hotels[0]['name']} (Hotel)
10:00 AM - Visit {attractions[day % len(attractions)]['name']}
1:00 PM - Lunch at {restaurants[day % len(restaurants)]['name']}
3:00 PM - Explore {attractions[(day + 1) % len(attractions)]['name']}
7:00 PM - Dinner at {restaurants[(day + 1) % len(restaurants)]['name']}
9:00 PM - Return to hotel

Estimated daily cost: ${travel_details['budget']}
"""
        days.append(daily_plan)

    return "\n\n".join(days)