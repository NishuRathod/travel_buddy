# Free API Guide for AI Travel Planner

## Free APIs (No API Key Required)
1. **OpenStreetMap/Nominatim API**
   - Used for getting place information and locations
   - Completely free, no registration needed
   - Already integrated in the code

2. **Wikipedia API**
   - Used for fetching place images
   - Completely free, no registration needed
   - Already integrated in the code

## Optional APIs (Free Tiers Available)
If you want enhanced features, you can optionally use these APIs:

1. **OpenWeather API** (for weather information)
   - Sign up at: https://openweathermap.org/api
   - Free tier includes:
     - 60 calls/minute
     - Current weather & forecasts
     - No credit card required

2. **OpenAI API** (for AI-generated itineraries)
   - Sign up at: https://platform.openai.com/api-keys
   - New users get free credits
   - Optional: The app will use template itineraries if no API key is provided

## Download and Setup Instructions

### Option 1: Download as ZIP
1. Click the "Download ZIP" button at the top of this Replit project
2. Extract the ZIP file to your computer
3. Open the folder in VS Code

### Option 2: Clone the Repository
```bash
git clone [your-repository-url]
cd ai-travel-planner
```

### Setup Steps
1. Install required packages:
```bash
pip install streamlit streamlit-folium folium python-dotenv requests trafilatura
```

2. Create a `.env` file:
- Copy `.env.example` to `.env`
- You can leave the API keys empty, the app will use fallback data

3. Run the application:
```bash
streamlit run main.py
```

## Using Without API Keys
The application will work without any API keys:
- Places and images will be fetched from free APIs
- Weather data will show placeholder information
- Itineraries will use template suggestions

## Getting Support
If you need help with setup or have questions about the APIs:
1. Check the README.md file for detailed setup instructions
2. Refer to vscode_setup.md for VS Code specific setup
3. See export_guide.md for additional deployment options
