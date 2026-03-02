import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BraveSearchAPI:
    """
    A simple wrapper for the Brave Search API that provides search functionality
    using the Brave Search API key. This is a free tier API with rate limits.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Brave Search API client.
        
        Args:
            api_key (str): Brave Search API key. If not provided, will look for 
                          BRAVE_SEARCH_API_KEY in environment variables.
        """
        self.api_key = api_key or os.getenv("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise ValueError("Brave Search API key not provided")
            
        self.base_url = "https://api.search.brave.com/res/v1"
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
    
    def search(self, query, count=10, offset=0, country="US", language="en"):
        """
        Perform a search using Brave Search API.
        
        Args:
            query (str): Search query string
            count (int): Number of results to return (1-100)
            offset (int): Offset for pagination
            country (str): Country code (ISO 3166-1 alpha-2)
            language (str): Language code (ISO 639-1)
            
        Returns:
            dict: Search results in JSON format
        """
        params = {
            "q": query,
            "count": min(count, 100),  # Max 100 results per request
            "offset": max(offset, 0),
            "country": country,
            "language": language,
            "freshness": "d",  # Results from last day (optional)
            "safe": "off",     # Disable safe search
            "spellcheck": "true"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/web/search",
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Search failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error performing search: {str(e)}")
    
    def search_news(self, query, count=10, offset=0, country="US", language="en"):
        """
        Search for news articles using Brave Search API.
        
        Args:
            query (str): Search query string
            count (int): Number of results to return (1-100)
            offset (int): Offset for pagination
            country (str): Country code (ISO 3166-1 alpha-2)
            language (str): Language code (ISO 639-1)
            
        Returns:
            dict: News results in JSON format
        """
        params = {
            "q": query,
            "count": min(count, 100),
            "offset": max(offset, 0),
            "country": country,
            "language": language,
            "freshness": "d"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/news/search",
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"News search failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error performing news search: {str(e)}")
    
    def search_images(self, query, count=10, offset=0, country="US", language="en"):
        """
        Search for images using Brave Search API.
        
        Args:
            query (str): Search query string
            count (int): Number of results to return (1-100)
            offset (int): Offset for pagination
            country (str): Country code (ISO 3166-1 alpha-2)
            language (str): Language code (ISO 639-1)
            
        Returns:
            dict: Image results in JSON format
        """
        params = {
            "q": query,
            "count": min(count, 100),
            "offset": max(offset, 0),
            "country": country,
            "language": language,
            "size": "all",  # all, large, medium, small
            "color": "all", # all, color, grayscale, transparent
            "type": "all"   # all, photo, clipart, lineart, face
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/images/search",
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Image search failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error performing image search: {str(e)}")
    
    def get_trending_topics(self, country="US", language="en"):
        """
        Get trending topics from Brave Search.
        
        Args:
            country (str): Country code (ISO 3166-1 alpha-2)
            language (str): Language code (ISO 639-1)
            
        Returns:
            dict: Trending topics in JSON format
        """
        params = {
            "country": country,
            "language": language
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/trending",
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Trending topics failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error getting trending topics: {str(e)}")


# Usage example (for testing)
if __name__ == "__main__":
    try:
        # Initialize API client
        api = BraveSearchAPI()
        
        # Test web search
        print("=== Web Search Test ===")
        results = api.search("Kalshi BTC 15-minute contracts", count=5)
        if "web" in results and "results" in results["web"]:
            for i, result in enumerate(results["web"]["results"], 1):
                print(f"{i}. {result['title']}")
                print(f"   {result['url']}")
                print(f"   {result['description'][:100]}...\n")
        
        # Test trending topics
        print("=== Trending Topics Test ===")
        trending = api.get_trending_topics()
        if "topics" in trending:
            for topic in trending["topics"]:
                print(f"- {topic['title']}")
        
    except Exception as e:
        print(f"Error: {e}")
