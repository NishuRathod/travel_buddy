import openai
import streamlit as st

@st.cache_data(ttl=3600)
def generate_itinerary(travel_details, places_data, api_key):
    """
    Generate AI-powered itinerary using OpenAI
    """
    try:
        openai.api_key = api_key
        
        # Create prompt from travel details and places
        prompt = f"""Create a detailed daily itinerary for a {travel_details['duration']} day trip to {travel_details['destination']} for {travel_details['group_size']} people with a budget of ${travel_details['budget']} per day.

Available attractions:
{', '.join([place['name'] for place in places_data['tourist_attraction']])}

Available restaurants:
{', '.join([place['name'] for place in places_data['restaurant']])}

Available hotels:
{', '.join([place['name'] for place in places_data['hotel']])}

Please include:
1. Daily schedule with timing
2. Estimated costs
3. Transportation suggestions
4. Meal recommendations
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable travel planner."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message['content']
        
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")
