import os
import requests
from crewai.tools import BaseTool
from datetime import datetime

class SheetsLoggerTool(BaseTool):
    name: str = "Google Sheets Logger Tool"
    description: str = "Logs structured news updates into Google Sheets via a Web App webhook."

    def _run(self, headline: str, summary: str, url: str) -> str:
        webapp_url = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL")
        
        payload = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "headline": headline,
            "summary": summary,
            "url": url
        }
        
        response = requests.post(webapp_url, json=payload)
        if response.status_code == 200:
            return "Successfully logged row to Google Sheets."
        else:
            return f"Failed to log to Google Sheets: {response.text}"