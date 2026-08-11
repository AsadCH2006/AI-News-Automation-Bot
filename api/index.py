import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            serper_api_key = os.environ.get("SERPER_API_KEY")
            groq_api_key = os.environ.get("GROQ_API_KEY")
            slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
            sheets_webhook = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL")
            
            # 1. Fetch News using Serper API
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=json.dumps({"q": "artificial intelligence news", "num": 3}).encode("utf-8"),
                headers={"X-API-KEY": serper_api_key, "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                search_data = json.loads(response.read().decode())
                
            news_items = search_data.get("organic", [])[:2]
            summary_text = "AI News Summary:\n"
            
            for item in news_items:
                title = item.get("title")
                snippet = item.get("snippet")
                link = item.get("link")
                summary_text += f"- *{title}*: {snippet} (<{link}|Read More>)\n"
                
                # 2. Send to Google Sheets Webhook
                if sheets_webhook:
                    sheet_payload = json.dumps({
                        "date": "2026-08-12",
                        "headline": title,
                        "summary": snippet,
                        "url": link
                    }).encode("utf-8")
                    sheet_req = urllib.request.Request(sheets_webhook, data=sheet_payload, headers={"Content-Type": "application/json"})
                    try:
                        urllib.request.urlopen(sheet_req)
                    except Exception as e:
                        print(f"Sheet error: {e}")

            # 3. Send to Slack Webhook
            if slack_webhook:
                slack_payload = json.dumps({"text": summary_text}).encode("utf-8")
                slack_req = urllib.request.Request(slack_webhook, data=slack_payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(slack_req)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "News processed and sent!"}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
