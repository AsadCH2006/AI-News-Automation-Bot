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
            
            # 1. Fetch latest raw news via Serper
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=json.dumps({"q": "latest artificial intelligence developments breakthroughs 2026", "num": 3}).encode("utf-8"),
                headers={"X-API-KEY": serper_api_key, "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                search_data = json.loads(response.read().decode())
                
            news_items = search_data.get("organic", [])
            slack_message = "🚀 *AI News Intelligence Briefing*\n\n"
            count = 0
            
            for item in news_items:
                title = item.get("title")
                snippet = item.get("snippet")
                link = item.get("link")
                
                if not title or not link:
                    continue
                
                # 2. Use Groq LLM to rewrite/synthesize the article professionally
                ai_summary = snippet
                if groq_api_key:
                    groq_payload = json.dumps({
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a professional tech journalist. Summarize the following news headline and snippet into one punchy, highly engaging, professional 2-sentence update for an audience."
                            },
                            {
                                "role": "user",
                                "content": f"Title: {title}\nSnippet: {snippet}"
                            }
                        ],
                        "temperature": 0.5
                    }).encode("utf-8")
                    
                    groq_req = urllib.request.Request(
                        "https://api.groq.com/openai/v1/chat/completions",
                        data=groq_payload,
                        headers={"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
                    }
                    try:
                        with urllib.request.urlopen(groq_req) as g_resp:
                            g_data = json.loads(g_resp.read().decode())
                            ai_summary = g_data["choices"][0]["message"]["content"].strip()
                    except Exception as ge:
                        print(f"Groq generation error: {ge}")

                # Format for Slack output
                slack_message += f"📌 *{title}*\n{ai_summary}\n<{link}|Read Source Article>\n\n"
                
                # 3. Push synthesized details to Google Sheets
                if sheets_webhook:
                    sheet_payload = json.dumps({
                        "date": "2026-08-12",
                        "headline": title,
                        "summary": ai_summary,
                        "url": link
                    }).encode("utf-8")
                    sheet_req = urllib.request.Request(sheets_webhook, data=sheet_payload, headers={"Content-Type": "application/json"})
                    try:
                        urllib.request.urlopen(sheet_req)
                    except Exception as se:
                        print(f"Sheet error: {se}")
                
                count += 1
                if count >= 3:
                    break

            # 4. Broadcast to Slack
            if slack_webhook and count > 0:
                slack_payload = json.dumps({"text": slack_message}).encode("utf-8")
                slack_req = urllib.request.Request(slack_webhook, data=slack_payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(slack_req)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "synthesized_articles": count}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
