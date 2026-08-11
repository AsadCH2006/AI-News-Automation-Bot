import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            serper_api_key = os.environ.get("SERPER_API_KEY")
            slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
            sheets_webhook = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL")
            
            # 1. Fetch targeted news items
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=json.dumps({"q": "latest artificial intelligence breakthroughs news 2026", "num": 5}).encode("utf-8"),
                headers={"X-API-KEY": serper_api_key, "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                search_data = json.loads(response.read().decode())
                
            news_items = search_data.get("organic", [])
            summary_text = "🤖 *Latest AI News Update*\n\n"
            seen_urls = set()
            count = 0
            
            for item in news_items:
                title = item.get("title")
                snippet = item.get("snippet")
                link = item.get("link")
                
                # Prevent duplicates and ensure valid links
                if link in seen_urls or not link or not title:
                    continue
                seen_urls.add(link)
                
                summary_text += f"• *{title}*\n{snippet}\n<{link}|Read Full Article>\n\n"
                
                # 2. Send unique items to Google Sheets Webhook
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
                
                count += 1
                if count >= 3:  # Limit to top 3 unique articles max per run
                    break

            # 3. Send clean consolidated message to Slack
            if slack_webhook and count > 0:
                slack_payload = json.dumps({"text": summary_text}).encode("utf-8")
                slack_req = urllib.request.Request(slack_webhook, data=slack_payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(slack_req)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "articles_sent": count}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
