from dotenv import load_dotenv
from newsapi import NewsApiClient as ApiClient
from datetime import datetime, timedelta
import os
import re
from bs4 import BeautifulSoup
import html

load_dotenv()

class NewsApiClient():
    def __init__(self):
        self.client = ApiClient(api_key=os.getenv("API_KEY_NEWSAPI"))

    def get_search_result(self, query: str) -> str:
        now = datetime.now()
        to_date = now.strftime("%Y-%m-%d")
        from_date = now - timedelta(days=5)
        results = self.client.get_everything(q=query, from_param=from_date, to=to_date, language="en", sort_by="popularity", page_size=15)
        cleaned_texts = []

        for article in results["articles"]:
            self.__clean_or_skip_text(article["title"], cleaned_texts)
            self.__clean_or_skip_text(article["content"], cleaned_texts)

        return "\n".join(cleaned_texts)

    def __clean_or_skip_text(self, text: str, texts_list: list[str]) -> None:
        if ("If you click 'Accept all'" in text) or (text == "None") or (text == "[Removed]"):
            return
        texts_list.append(self.__clean_text(text))

    def __clean_text(self, text: str) -> str:
        # Step 1: Remove HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()

        # Step 2: Decode HTML character entities
        text = html.unescape(text)

        # Step 3: Replace newlines (\r\n, \r, \n) with a single space
        text = re.sub(r"[\r\n]+", " ", text)

        # Step 4: Remove unicode escape sequences like '\xa0', '\uXXXX'
        text = re.sub(r"\\[xXuU][0-9a-fA-F]+", "", text)

        # Step 5: Replace \" by "
        text = text.replace('\\"', '"')

        # Step 6: Remove any strings followed by three dots or an ellipsis
        text = re.sub(r"\S+(?:\.\.\.|…)", "", text)

        # Step 7: Remove patterns like '[+1234 chars]'
        text = re.sub(r"\[\+\d+ chars\]", "", text)

        # Step 8: Remove URLs
        text = re.sub(r"(https?://\S+|www\.\S+)", "", text, flags=re.IGNORECASE)

        # Step 9: Replace text
        text = text.replace("Skip to comments.", "")

        # Step 10: Remove extra spaces
        text = " ".join(text.split())

        return text
