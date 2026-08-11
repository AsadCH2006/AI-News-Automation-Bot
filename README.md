# 🤖 AI News Automation Bot & Intelligence Hub

[![Vercel Deployment](https://img.shields.io/badge/Deployed%20to-Vercel-black?style=for-the-badge&logo=vercel)](https://ai-news-automation-bot-flame.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Serverless-lightgrey?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-UI-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

An autonomous, serverless AI-powered news aggregator and intelligence pipeline. It continuously scans the web for the latest artificial intelligence breakthroughs, transforms raw snippets into professional journalist-grade briefings using **Groq's LLM (Llama 3)**, and automatically broadcasts them to **Slack** and **Google Sheets**—all wrapped in a sleek, real-time dark-mode web dashboard.

---

## ✨ Core Features

- **⚡ Real-Time Interactive Dashboard:** Built with Flask and styled with Tailwind CSS, featuring live system status monitoring and manual pipeline execution.
- **🧠 AI-Powered Content Synthesis:** Utilizes Groq (`llama-3.3-70b-versatile`) to convert raw search snippets into professional, engaging tech journalism updates instead of raw data dumps.
- **🔄 Multi-Channel Synchronization:** Automatically pushes formatted intelligence briefings to your **Slack Channel** via Webhooks while appending structured records into **Google Sheets**.
- **🚀 Serverless Architecture:** Optimized for Vercel Serverless functions with lightweight Python execution to avoid compilation crashes and heavy package bloat.
- **⏰ Automated Cron Scheduling:** Configured via `vercel.json` to trigger scheduled updates autonomously.

---

## ⚠️ Limiting Factor: Execution Frequency & Cron Limitations

You asked: **"Do we have to add the time like every 1 hour it does an updated query search for a new news article?"**

This introduces a core architectural **limiting factor** based on your hosting tier:

- **Vercel Hobby (Free) Tier Restriction:** Vercel strictly limits cron jobs on free hobby plans to run **at most once per day** (e.g., scheduled at midnight via `0 0 * * *`). Attempting to configure an hourly interval (`0 * * * *`) on a Hobby account will trigger a build deployment validation error.
- **On-Demand Manual Workaround:** Even on the free tier, you are not locked out of fresh updates. You can access your live web dashboard at any time and click **"Run Manual Pipeline"** to trigger a real-time fetch cycle on demand.
- **Hourly Updates via Pro Plan:** If you upgrade to Vercel Pro, you can unlock high-frequency cron executions and adjust your `vercel.json` schedule to run queries **every hour** (`0 * * * *`) around the clock.

---

## 🏗️ System Architecture & Workflow



1. **Trigger Phase:** The bot initiates via a cron schedule or a manual dashboard button click.
2. **Search Phase:** Real-time search queries are processed via the **Serper API** to extract top-ranking tech headlines.
3. **Synthesis Phase:** Raw content is securely fed into **Groq Cloud** to generate structured, professional technical summaries.
4. **Broadcast Phase:** Formatted text payloads are dispatched to **Slack** and logged cleanly into **Google Sheets**.

---

## 📂 Project Structure

```text
AI-News-Automation-Bot/
├── api/
│   └── index.py         # Main Flask server, Dashboard template, and Pipeline logic
├── requirements.txt     # Python dependencies (Flask runtime)
├── vercel.json          # Deployment routing and cron scheduler rules
└── README.md            # Comprehensive repository documentation

⚙️ Environment Variables ConfigurationTo run this project successfully, ensure the following environment variables are securely added to your Vercel project settings:Variable NameDescriptionExample ValueSERPER_API_KEYAPI Key for Google Search queries via Serper.dev41e7105dc4ce...GROQ_API_KEYAPI Key for Groq Cloud LLM text summarizationgsk_w0piCUQH2...SLACK_WEBHOOK_URLIncoming Webhook URL for your Slack notification channelhttps://hooks.slack.com/services/...GOOGLE_SHEETS_WEBHOOK_URLGoogle Apps Script Webhook URL for database logginghttps://script.google.com/macros/s/...SPREADSHEET_NAMETarget Google Sheets database nameAI_News_Database🚀 Local Development & Deployment GuideClone the repository:Bashgit clone [https://github.com/AsadCH2006/AI-News-Automation-Bot.git](https://github.com/AsadCH2006/AI-News-Automation-Bot.git)
cd AI-News-Automation-Bot
Install dependencies locally:Bashpip install -r requirements.txt
Export environment variables locally (or create a local configuration file):Bashexport SERPER_API_KEY="your_serper_key"
export GROQ_API_KEY="your_groq_key"
export SLACK_WEBHOOK_URL="your_slack_webhook"
export GOOGLE_SHEETS_WEBHOOK_URL="your_sheets_webhook"
Run the Flask app locally:Bashpython api/index.py
Open your browser and navigate to http://127.0.0.1:5000 to view the local dashboard.Deploy to Vercel:Push your repository to GitHub, import it directly into your Vercel Dashboard, map your environment variables, and deploy!
