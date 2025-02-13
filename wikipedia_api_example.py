import requests

def simple_wikipedia_search(place_name):
    """
    A simple example of using Wikipedia's free API to search for a place
    No API key required!
    """
    # Wikipedia API endpoint
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # Parameters for the search
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": place_name,
        "utf8": 1
    }
    
    # Make the request
    response = requests.get(api_url, params=params)
    data = response.json()
    
    # Print the results
    if 'query' in data and 'search' in data['query']:
        print(f"\nResults for {place_name}:")
        for result in data['query']['search'][:3]:  # Show top 3 results
            print(f"\nTitle: {result['title']}")
            print(f"Description: {result['snippet']}")
    else:
        print("No results found")

# You can test it like this:
if __name__ == "__main__":
    simple_wikipedia_search("Eiffel Tower")
