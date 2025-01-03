from dotenv import load_dotenv
import requests
import os
from datetime import datetime

load_dotenv()  # This loads the variables from .env

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
search_url = "https://newsapi.org/v2/everything"

def bing_search_news(company_name: str):
    headers = {"Authorization": NEWS_API_KEY}
    params  = {
        "q": f"{company_name} stock price AND finance",  # Поиск по названию компании и ключевым словам
        "language": "en",  # Поиск на английском языке
        "sortBy": "publishedAt",  # Сортировка по дате публикации
        "pageSize": 100,  # Максимальное количество результатов
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    current_month = datetime.now().month
    current_year = datetime.now().year

    filtered_articles = []
    for article in search_results["articles"]:
        published_date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        if published_date.month == current_month and published_date.year == current_year:
            filtered_articles.append(article)

    return filtered_articles
