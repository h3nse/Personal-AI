import os
from dotenv import load_dotenv

load_dotenv()

def get_human_input(quiry):
    return input(quiry + ' ')

from serpapi import GoogleSearch

def quick_search(query):
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google",
        "q": query,
        "hl": "en",
        "gl": "dk",
        "google_domain": "google.com",
        }
    search = GoogleSearch(params)
    results = search.get_dict()

    return results['answer_box'] if 'answer_box' in results else "No answer"