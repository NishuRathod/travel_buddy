
   ```

1. **Free APIs:**
   This project uses several free APIs - see [FREE_API_GUIDE.txt]for details on:
   - Which APIs are completely free
   - Which APIs are optional
   - How to use the app without API keys

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
└── app.py              # Main application file
```

## Features
- Interactive travel planning interface
- AI-generated personalized itineraries
- Weather information integration
- Interactive maps with points of interest
- Hotel and restaurant recommendations
- Dynamic place information with images

## Setup Instructions

1. Clone the repository to your local machine
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
    pip install streamlit streamlit-folium folium python-dotenv requests trafilatura
   ```
4. Set up your `.env` file with the required API keys (optional)
5. Start the application:
   ```bash
   streamlit run app.py