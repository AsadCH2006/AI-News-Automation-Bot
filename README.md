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
- **⏰ Automated & On-Demand Cadence:** Configured via `vercel.json` to trigger scheduled updates autonomously alongside instant manual web triggers.

---

## 🏗️ System Architecture & Workflow

1. **Trigger Phase:** The bot initiates via an automated cron schedule or a manual dashboard button click.
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
```

---

## ⚙️ Environment Variables Configuration

To run this project successfully, ensure the following environment variables are securely added to your Vercel project settings:

| Variable Name | Description | Example Value |
| :--- | :--- | :--- |
| `SERPER_API_KEY` | API Key for Google Search queries via Serper.dev | `41e7105dc4ce...` |
| `GROQ_API_KEY` | API Key for Groq Cloud LLM text summarization | `gsk_w0piCUQH2...` |
| `SLACK_WEBHOOK_URL` | Incoming Webhook URL for your Slack notification channel | `https://hooks.slack.com/services/...` |
| `GOOGLE_SHEETS_WEBHOOK_URL` | Google Apps Script Webhook URL for database logging | `https://script.google.com/macros/s/...` |
| `SPREADSHEET_NAME` | Target Google Sheets database name | `AI_News_Database` |

---

## 🚀 Local Development & Deployment Guide

### 1. Clone the repository
```bash
git clone https://github.com/AsadCH2006/AI-News-Automation-Bot.git
cd AI-News-Automation-Bot
```

### 2. Install dependencies locally
```bash
pip install -r requirements.txt
```

### 3. Export environment variables locally
```bash
export SERPER_API_KEY="your_serper_key"
export GROQ_API_KEY="your_groq_key"
export SLACK_WEBHOOK_URL="your_slack_webhook"
export GOOGLE_SHEETS_WEBHOOK_URL="your_sheets_webhook"
```

### 4. Run the Flask app locally
```bash
python api/index.py
```
*Open your browser and navigate to `http://127.0.0.1:5000` to view the local dashboard.*

### 5. Deploy to Vercel
Push your repository to GitHub, import it directly into your Vercel Dashboard, map your environment variables, and deploy!
