import os
import requests
from crewai.tools import BaseTool
from pydantic import Field

class NewsFetcherTool(BaseTool):
    name: str = "News Fetcher Tool"
    description: str = "Fetches the latest trending news articles based on a given topic using the Serper API."

    def _run(self, topic: str) -> str:
        url = "https://google.serper.dev/search"
        payload = f'{{"q": "{topic} news", "tbm": "nsw"}}'
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
            return f"Error fetching news: {response.text}"
            
        data = response.json()
        articles = []
        for item in data.get("news", []):
            articles.append(f"Title: {item.get('title')}\nLink: {item.get('link')}\nSnippet: {item.get('snippet')}\n")
        
        return "\n---\n".join(articles) if articles else "No recent articles found."