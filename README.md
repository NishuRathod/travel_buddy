# AI Travel Planner

An AI-powered travel planning application that generates personalized itineraries with dynamic recommendations and interactive exploration tools.

## Project Structure
```
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── assets/
│   └── style.css        # Custom styling
├── components/
│   ├── displays.py      # Display components
│   └── forms.py         # Input form components
├── utils/
│   ├── api_handlers.py  # API integration
│   ├── itinerary_generator.py  # AI itinerary generation
│   └── place_images.py  # Image handling
└── main.py              # Main application file
```

## Dependencies
Install the following Python packages:
```bash
pip install streamlit streamlit-folium folium openai python-dotenv requests trafilatura
```

## Environment Variables
Create a `.env` file in the root directory with the following:
```
OPENWEATHER_API_KEY=your_openweather_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_PLACES_API_KEY=your_google_places_api_key
```

## Setup Instructions

1. Clone the repository to your local machine
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with the required API keys
5. Start the application:
   ```bash
   streamlit run main.py
   ```

## Features
- Interactive travel planning interface
- AI-generated personalized itineraries
- Weather information integration
- Interactive maps with points of interest
- Hotel and restaurant recommendations
- Dynamic place information with images

## Development in VS Code
1. Install the Python extension for VS Code
2. Open the project folder in VS Code
3. Select your Python interpreter (preferably from your virtual environment)
4. Install the Streamlit extension for better development experience
5. Use the integrated terminal to run the application

## Troubleshooting
- If you encounter API timeout issues, the application will use fallback data
- Ensure all API keys are correctly set in your `.env` file
- Check your internet connection for map and weather data

## Notes
- The application uses OpenStreetMap for place data (no API key required)
- Weather data is fetched from OpenWeather API
- Place images are fetched from Wikipedia API
