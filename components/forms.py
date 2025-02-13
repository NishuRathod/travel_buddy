import streamlit as st

def render_input_form():
    """
    Render the travel planning input form
    """
    st.sidebar.header("Plan Your Trip")
    
    with st.sidebar.form("travel_form"):
        destination = st.text_input("Destination City", placeholder="e.g., Paris")
        
        col1, col2 = st.columns(2)
        with col1:
            group_size = st.number_input(
                "Group Size",
                min_value=1,
                max_value=10,
                value=2
            )
        with col2:
            duration = st.number_input(
                "Duration (days)",
                min_value=1,
                max_value=14,
                value=3
            )
            
        budget = st.slider(
            "Daily Budget per Person ($)",
            min_value=50,
            max_value=500,
            value=200,
            step=50
        )
        
        preferences = st.multiselect(
            "Preferences",
            options=[
                "Cultural",
                "Food",
                "Nature",
                "Shopping",
                "Adventure"
            ],
            default=["Cultural"]
        )
        
        submitted = st.form_submit_button("Generate Plan")
        
        if submitted and destination:
            return {
                "destination": destination,
                "group_size": group_size,
                "duration": duration,
                "budget": budget,
                "preferences": preferences
            }
        return None
