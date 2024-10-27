from dotenv import load_dotenv
import os
from tavily import TavilyClient as TC

load_dotenv()

class TavilyClient():
    def __init__(self):
        self.client = TC(api_key=os.getenv("API_KEY_TAVILY"))

    def get_search_result(self, query: str) -> str:
        response = self.client.search(query, topic="news")
        return self.extract_results(response)
    
    def extract_results(self, response: dict) -> str:
        results = []

        for res in response["results"]:
            results.append(res["title"])
            results.append(res["content"])

        return "\n".join(results)