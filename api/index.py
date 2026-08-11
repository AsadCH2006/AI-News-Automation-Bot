import os
import json
import urllib.request
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Intelligence Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-indigo-500 selection:text-white">
    <div class="max-w-4xl mx-auto px-6 py-12 w-full">
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-6 mb-8 gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="inline-block w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
                    <h1 class="text-2xl font-bold tracking-tight text-white">AI News Automation Hub</h1>
                </div>
                <p class="text-sm text-slate-400 mt-1">Autonomous intelligence briefing streamed to Slack & Google Sheets.</p>
            </div>
            <button onclick="triggerFetch()" id="fetch-btn" class="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 font-medium text-sm transition-all shadow-lg shadow-indigo-600/20 active:scale-95 flex items-center gap-2 cursor-pointer">
                <span>⚡ Run Manual Pipeline</span>
            </button>
        </header>

        <div id="status-box" class="hidden mb-8 p-4 rounded-xl bg-slate-900 border border-slate-800 text-sm"></div>

        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl">
                <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">System Status</h3>
                <p class="text-lg font-semibold text-emerald-400">Online & Ready</p>
                <p class="text-xs text-slate-500 mt-1">Flask WSGI Active</p>
            </div>
            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl">
                <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Schedule Type</h3>
                <p class="text-lg font-semibold text-indigo-400">Daily Automated</p>
                <p class="text-xs text-slate-500 mt-1">Cron Enabled via Config</p>
            </div>
            <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl">
                <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Integrations</h3>
                <p class="text-lg font-semibold text-purple-400">Slack & Sheets</p>
                <p class="text-xs text-slate-500 mt-1">Real-time webhook sync</p>
            </div>
        </section>

        <div class="space-y-4">
            <h2 class="text-lg font-semibold tracking-tight text-white mb-4">Latest Processed Briefings</h2>
            <div id="news-container" class="space-y-4">
                <div class="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/60 text-slate-400 text-center">
                    Click <span class="text-indigo-400 font-semibold">"Run Manual Pipeline"</span> above to fetch and process fresh AI headlines instantly.
                </div>
            </div>
        </div>
    </div>

    <footer class="border-t border-slate-900 py-6 text-center text-xs text-slate-600">
        AI News Automation Bot &bull; Powered by Groq, Serper, & Vercel.
    </footer>

    <script>
        async function triggerFetch() {
            const btn = document.getElementById('fetch-btn');
            const statusBox = document.getElementById('status-box');
            const container = document.getElementById('news-container');
            
            btn.disabled = true;
            btn.innerHTML = '<span>Processing...</span>';
            statusBox.className = 'mb-8 p-4 rounded-xl bg-blue-950/40 border border-blue-800/50 text-blue-300 text-sm flex items-center gap-2';
            statusBox.innerHTML = '<span class="animate-spin">⏳</span> Fetching live articles, generating Groq AI summaries, and syncing databases...';
            statusBox.classList.remove('hidden');

            try {
                const res = await fetch('/api/run');
                const data = await res.json();
                
                if (data.status === 'success') {
                    statusBox.className = 'mb-8 p-4 rounded-xl bg-emerald-950/40 border border-emerald-800/50 text-emerald-300 text-sm';
                    statusBox.innerHTML = '✅ Successfully processed and broadcasted <strong>' + data.synthesized_articles + '</strong> articles to Slack & Sheets!';
                    
                    if (data.articles && data.articles.length > 0) {
                        container.innerHTML = data.articles.map(art => `
                            <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-all">
                                <h3 class="font-semibold text-white text-base mb-1">` + art.title + `</h3>
                                <p class="text-sm text-slate-300 mb-3 leading-relaxed">` + art.summary + `</p>
                                <a href="` + art.link + `" target="_blank" class="text-xs font-medium text-indigo-400 hover:text-indigo-300 underline underline-offset-4">Read Original Source &rarr;</a>
                            </div>
                        `).join('');
                    }
                } else {
                    throw new Error(data.error || 'Unknown execution error');
                }
            } catch (err) {
                statusBox.className = 'mb-8 p-4 rounded-xl bg-rose-950/40 border border-rose-800/50 text-rose-300 text-sm';
                statusBox.innerHTML = '❌ Error executing pipeline: ' + err.message;
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<span>⚡ Run Manual Pipeline</span>';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/run', methods=['GET'])
def run_pipeline():
    try:
        serper_api_key = os.environ.get("SERPER_API_KEY")
        groq_api_key = os.environ.get("GROQ_API_KEY")
        slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
        sheets_webhook = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL")
        
        req = urllib.request.Request(
            "https://google.serper.dev/search",
            data=json.dumps({"q": "latest artificial intelligence breakthroughs news 2026", "num": 3}).encode("utf-8"),
            headers={"X-API-KEY": serper_api_key, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            search_data = json.loads(response.read().decode())
            
        news_items = search_data.get("organic", [])
        slack_message = "🚀 *AI News Intelligence Briefing*\n\n"
        processed_list = []
        count = 0
        
        for item in news_items:
            title = item.get("title")
            snippet = item.get("snippet")
            link = item.get("link")
            
            if not title or not link:
                continue
            
            ai_summary = snippet
            if groq_api_key:
                groq_payload = json.dumps({
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are a professional tech journalist. Summarize the news headline and snippet into a punchy, engaging 2-sentence update."},
                        {"role": "user", "content": f"Title: {title}\nSnippet: {snippet}"}
                    ],
                    "temperature": 0.5
                }).encode("utf-8")
                
                groq_req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    data=groq_payload,
                    headers={"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
                )
                try:
                    with urllib.request.urlopen(groq_req) as g_resp:
                        g_data = json.loads(g_resp.read().decode())
                        ai_summary = g_data["choices"][0]["message"]["content"].strip()
                except Exception:
                    pass

            slack_message += f"📌 *{title}*\n{ai_summary}\n<{link}|Read Source Article>\n\n"
            processed_list.append({"title": title, "summary": ai_summary, "link": link})
            
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
                except Exception:
                    pass
            
            count += 1
            if count >= 3:
                break

        if slack_webhook and count > 0:
            slack_payload = json.dumps({"text": slack_message}).encode("utf-8")
            slack_req = urllib.request.Request(slack_webhook, data=slack_payload, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(slack_req)

        return jsonify({"status": "success", "synthesized_articles": count, "articles": processed_list})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
