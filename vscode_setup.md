# VS Code Setup Guide

## Required VS Code Extensions
1. Python (by Microsoft)
2. Streamlit
3. Python Environment Manager

## Project Setup Steps

1. Create a new folder and clone/copy these project files:
```
├── .streamlit/
│   └── config.toml
├── assets/
│   └── style.css
├── components/
│   ├── displays.py
│   └── forms.py
├── utils/
│   ├── api_handlers.py
│   ├── itinerary_generator.py
│   └── place_images.py
└── main.py
```

2. Open Terminal in VS Code and run:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install streamlit streamlit-folium folium openai python-dotenv requests trafilatura
```

3. Create a `.env` file in the root directory:
```
OPENWEATHER_API_KEY=your_openweather_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_PLACES_API_KEY=your_google_places_api_key
```

4. Running the Application:
```bash
streamlit run main.py
```

## VS Code Debugging Setup

1. Create a `.vscode/launch.json` file:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Streamlit",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": [
                "run",
                "main.py"
            ],
            "justMyCode": true
        }
    ]
}
```

2. Press F5 to start debugging

## Troubleshooting Tips
- If packages are not found, ensure your virtual environment is activated
- Check that all API keys are correctly set in the `.env` file
- Verify Python interpreter is selected in VS Code (Ctrl+Shift+P > Python: Select Interpreter)
