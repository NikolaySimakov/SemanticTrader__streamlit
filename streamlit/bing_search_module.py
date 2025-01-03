from dotenv import load_dotenv
import requests
import os
from datetime import datetime

load_dotenv()  # This loads the variables from .env

BING_SEARCH_API_KEY = os.getenv('BING_SEARCH_API_KEY')
search_url = "https://api.bing.microsoft.com/v7.0/news/search"

def bing_search_news(company_name: str):
    headers = {"Ocp-Apim-Subscription-Key" : BING_SEARCH_API_KEY}
    params  = {
        "q": f"{company_name} stock price and finance news",
        "mkt": "en-US",  # Search in English
        "textDecorations": True,
        "textFormat": "HTML",
        "freshness": "Month",
        "count": 100,
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    current_month = datetime.now().month
    current_year = datetime.now().year

    filtered_articles = []
    for article in search_results["value"]:
        # Adjust the date format
        date_str = article["datePublished"]
        # Trimming microseconds to six digits and replacing 'Z' with '+00:00'
        date_str = date_str[:-2] + date_str[-1].replace('Z', '+00:00')
        published_date = datetime.fromisoformat(date_str)
        if published_date.month == current_month and published_date.year == current_year:
            filtered_articles.append(article)

    return filtered_articles