# Brave Search API Skill

A simple and efficient API wrapper for Brave Search, providing free tier search functionality with rate limits.

## Overview

This skill provides a Python wrapper for the Brave Search API, allowing you to:
- Perform web searches
- Search for news articles
- Find images
- Get trending topics

All functionality uses the free tier API with rate limits (1000 queries per month).

## Installation

```bash
pip install requests python-dotenv
```

## Configuration

1. Get your Brave Search API key from https://brave.com/search/api/
2. Set your API key in the `.env` file:

```env
BRAVE_SEARCH_API_KEY=BSATJWSJ8Sm9eT_H0UgT_fDjiikmgCI
```

## Usage

```python
from brave_search import BraveSearchAPI

# Initialize API client
api = BraveSearchAPI()

# Web search
results = api.search("Kalshi BTC 15-minute contracts", count=5)
for result in results["web"]["results"]:
    print(f"{result['title']} - {result['url']}")
    print(f"{result['description']}\n")

# News search
news = api.search_news("Bitcoin market news", count=3)
for article in news["news"]["results"]:
    print(f"{article['title']} - {article['source']}")
    print(f"{article['url']}\n")

# Trending topics
trending = api.get_trending_topics()
for topic in trending["topics"]:
    print(f"- {topic['title']}")
```

## Features

### Web Search
```python
search(query, count=10, offset=0, country="US", language="en")
```
- `query`: Search string
- `count`: Number of results to return (1-100)
- `offset`: Pagination offset
- `country`: Country code (ISO 3166-1 alpha-2)
- `language`: Language code (ISO 639-1)

### News Search
```python
search_news(query, count=10, offset=0, country="US", language="en")
```
- Searches for news articles with optional freshness filter (last day)

### Image Search
```python
search_images(query, count=10, offset=0, country="US", language="en")
```
- Returns image results with metadata

### Trending Topics
```python
get_trending_topics(country="US", language="en")
```
- Returns current trending topics by country

## Rate Limits

- **Free Tier**: 1000 queries per month
- **Rate Limit**: 5 queries per second
- **Requests per Minute**: 300

## Error Handling

The API will raise exceptions for:
- Invalid API key
- Rate limit exceeded
- Network errors
- Invalid parameters

## Performance

- Uses requests library with connection pooling
- Optional timeout and retry logic
- Efficient JSON parsing
- Caching support via session state

## Compatibility

- Python 3.7+
- Works with Streamlit, Flask, Django, and other frameworks
- Cross-platform (Windows, macOS, Linux)

## License

MIT License - free for personal and commercial use.

## Support

For support, please check:
- https://brave.com/search/api/
- https://brave.com/search/
- https://github.com/brave/brave-api
