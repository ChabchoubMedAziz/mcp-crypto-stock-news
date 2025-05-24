import requests
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

if not API_KEY:
    logger.error("CRYPTOPANIC_API_KEY not found in environment variables")

mcp = FastMCP("crypto_news")
        
@mcp.tool()
def get_crypto_news() -> str:
    """Fetch the latest cryptocurrency news from CryptoPanic API"""
    logger.info("Fetching crypto news...")
    news = fetch_crypto_news()
    readable = concatenate_news(news)
    logger.info(f"Returned {len(news)} news items")
    return readable

def fetch_crypto_news_page(page: int = 1): 
    """Fetch a single page of crypto news"""
    try:
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            "auth_token": API_KEY,
            "kind": "news",  # news, analysis, videos
            "regions": "en",  
            "page": page
        }
        logger.info(f"Fetching page {page} from CryptoPanic API...")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        results = data.get("results", [])
        logger.info(f"Got {len(results)} news items from page {page}")
        return results
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching page {page}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching page {page}: {e}")
        return []
        
def fetch_crypto_news():
    """Fetch multiple pages of crypto news"""
    all_news = []
    for page in range(1, 4):  # Reduced to 3 pages for faster testing
        news_items = fetch_crypto_news_page(page)
        if not news_items:
            logger.info(f"No more news found on page {page}. Stopping.")
            break
        all_news.extend(news_items)
    
    logger.info(f"Total news items fetched: {len(all_news)}")
    return all_news        

def concatenate_news(news_items):
    """Convert news items to readable text format"""
    if not news_items:
        return "No crypto news available at the moment."
    
    concatenated_text = "Latest Cryptocurrency News:\n\n"
    for idx, news in enumerate(news_items[:20], 1):  # Limit to top 20 news items
        title = news.get("title", "No Title")
        url = news.get("url", "")
        published_at = news.get("published_at", "")
        
        concatenated_text += f"{idx}. {title}\n"
        if published_at:
            concatenated_text += f"   Published: {published_at}\n"
        if url:
            concatenated_text += f"   URL: {url}\n"
        concatenated_text += "\n"
       
    return concatenated_text.strip()

def test_locally():
    """Test the crypto news functionality locally"""
    print("Testing crypto news fetcher locally...")
    
    if not API_KEY:
        print("❌ CRYPTOPANIC_API_KEY not found. Please set it in your .env file")
        return
    
    print("✅ API key found")
    print("Fetching crypto news...")
    
    try:
        news = fetch_crypto_news()
        if news:
            print(f"✅ Successfully fetched {len(news)} news items")
            readable = concatenate_news(news)
            print("\n" + "="*50)
            print(readable[:500] + "..." if len(readable) > 500 else readable)
            print("="*50)
        else:
            print("❌ No news items fetched")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    import sys
    
    # Check if we want to test locally
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_locally()
    else:
        logger.info("Starting crypto news MCP server...")
        mcp.run(transport="stdio")