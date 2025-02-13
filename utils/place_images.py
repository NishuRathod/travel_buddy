import requests
import urllib.parse

def get_place_image(place_name, city):
    """
    Fetch an image URL for a place using Wikipedia API - No API key required!
    This function uses Wikipedia's free public API to:
    1. Search for the place in Wikipedia
    2. Get the page's images
    3. Return a suitable image URL

    Args:
        place_name: Name of the place (e.g., "Eiffel Tower")
        city: City name for better search results

    Returns:
        str: URL of the image, or None if no image found
    """
    try:
        # Step 1: Search for the place in Wikipedia (free, no API key needed)
        search_query = f"{place_name} {city}"
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_query,
            "utf8": 1
        }

        response = requests.get(search_url, params=search_params)
        data = response.json()

        if not data['query']['search']:
            return None

        # Step 2: Get the first result's page ID
        page_id = data['query']['search'][0]['pageid']

        # Step 3: Get images from the page
        image_params = {
            "action": "query",
            "format": "json",
            "prop": "images|pageimages",
            "pageids": page_id,
            "piprop": "original"
        }

        response = requests.get(search_url, params=image_params)
        data = response.json()

        # Try to get the main image first
        page = data['query']['pages'][str(page_id)]
        if 'original' in page:
            return page['original']['source']

        # If no main image, try to get first image from images list
        if 'images' in page:
            for image in page['images']:
                if any(ext in image['title'].lower() for ext in ['.jpg', '.jpeg', '.png']):
                    image_title = image['title']
                    # Get the actual image URL
                    file_params = {
                        "action": "query",
                        "format": "json",
                        "prop": "imageinfo",
                        "titles": image_title,
                        "iiprop": "url"
                    }
                    response = requests.get(search_url, params=file_params)
                    data = response.json()
                    pages = data['query']['pages']
                    for page_id in pages:
                        if 'imageinfo' in pages[page_id]:
                            return pages[page_id]['imageinfo'][0]['url']

        return None
    except Exception as e:
        print(f"Error fetching image: {str(e)}")
        return None

# Example usage:
# image_url = get_place_image("Eiffel Tower", "Paris")
# No API key needed - Wikipedia API is completely free!