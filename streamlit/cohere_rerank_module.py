from dotenv import load_dotenv
import os
import cohere

load_dotenv()  # This loads the variables from .env

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

co = cohere.Client(COHERE_API_KEY)

def rerank_search_results(company_name: str, search_results: list[str], top_n: int):
    query = f"Filter and prioritize news headlines explicitly discussing factors influencing {company_name}'s stock price, including market trends, financial reports, corporate announcements, and industry-specific news impacting {company_name}'s performance."
    results = co.rerank(model="rerank-english-v2.0", query=query, documents=search_results, top_n=top_n)
    return [result.document['text'] for result in results]