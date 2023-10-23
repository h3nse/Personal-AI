import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

init()
load_dotenv()

def get_human_input(follow_up_question: str):
    """Ask the user a follow up question.
    
    Args:
        follow_up_question: The question for the user, asked politely"""
    return input(f"{Fore.MAGENTA}{follow_up_question}\n>>{Style.RESET_ALL}")

from serpapi import GoogleSearch

def quick_search(query: str):
    """Search something on the internet.
    
    Args:
        query: A targeted search query"""
    print(f"{Fore.YELLOW}doing search for \"{query}\"{Style.RESET_ALL}")
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