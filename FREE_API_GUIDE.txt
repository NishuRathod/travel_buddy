# Free API Guide for AI Travel Planner
### Option 1: Download as ZIP
1. Click the "Download ZIP" button 
2. Extract the ZIP file to your computer
3. Open the folder in VS Code

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

