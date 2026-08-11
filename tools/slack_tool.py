import os
import requests
from crewai.tools import BaseTool

class SlackBotTool(BaseTool):
    name: str = "Slack Bot Integration Tool"
    description: str = "Posts summarized news updates directly into a Slack channel."

    def _run(self, message: str) -> str:
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        payload = {"text": message}
        
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            return "Successfully posted updates to Slack."
        else:
            return f"Failed to post to Slack: {response.text}"