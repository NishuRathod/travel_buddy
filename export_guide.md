# Export Guide for VS Code

## Step 1: Download These Files
Create a new folder on your computer and download these files with the exact same structure:

```
project_folder/
├── .streamlit/
│   └── config.toml      # Server configuration
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

## Step 2: Install Required Packages
Open a terminal in VS Code and run:
```bash
pip install streamlit streamlit-folium folium openai python-dotenv requests trafilatura
```

## Step 3: Set Up Environment Variables
1. Create a file named `.env` in your project folder
2. Copy the contents from `.env.example`
3. Replace with your actual API keys:
   - OPENWEATHER_API_KEY
   - OPENAI_API_KEY
   - GOOGLE_PLACES_API_KEY

## Step 4: Run the Application
In the VS Code terminal:
```bash
streamlit run main.py
```

## Troubleshooting
- If you see API timeout errors, the application will use fallback data automatically
- Make sure all API keys are correctly set in your `.env` file
- If packages are not found, try running pip install again

Need help? Check the detailed setup guide in `vscode_setup.md` for advanced configuration.
