# 🤖 AI News Automation Bot & Intelligence Hub

An autonomous, serverless AI-powered news aggregator and intelligence pipeline built to fetch breaking technology updates, synthesize professional briefings using Groq LLM, and instantly broadcast them to **Slack** and **Google Sheets**, complete with a gorgeous real-time interactive **Flask & Tailwind CSS dashboard**.

---

## ✨ Features

- **⚡ Real-Time Interactive Dashboard:** Built with Flask and styled with Tailwind CSS, featuring live system status monitoring and manual pipeline execution.
- **🧠 AI-Powered Content Synthesis:** Utilizes Groq (`llama-3.3-70b-versatile`) to convert raw search snippets into professional, engaging tech journalism updates.
- **🔄 Multi-Channel Broadcasting:** Automatically pushes formatted intelligence briefings to your **Slack Channel** and appends structured logs into **Google Sheets**.
- **🚀 Serverless Architecture:** Optimized for Vercel Edge/Serverless functions with lightweight native Python execution—zero dependency compilation overhead.
- **⏰ Automated Scheduling:** Configured via Vercel Cron to run daily automated fetch cycles.

---

## 🕒 Cron Frequency Note (1-Hour vs Daily)

You asked: **"Do we have to add the time like every 1 hour it does an updated query search for a new news article?"**

- **Vercel Hobby Plan Limitation:** Vercel's free Hobby tier restricts cron jobs to run **at most once per day** (e.g., `0 0 * * *`). Attempting to schedule a cron job every hour (`0 * * * *`) on a free Hobby account will result in a deployment validation error.
- **Pro / Enterprise Plan:** If you upgrade to Vercel Pro, you can unlock high-frequency cron jobs and configure your `vercel.json` schedule to run **every hour** (`0 * * * *`) for real-time news updates.

---

## 🛠️ Project Structure

```text
AI-News-Automation-Bot/
├── api/
│   └── index.py         # Main Flask server, Dashboard template, and Pipeline logic
├── requirements.txt     # Python dependencies (Flask)
├── vercel.json          # Vercel deployment routes and cron job configurations
└── README.md            # Project documentation
```

---

## ⚙️ Environment Variables

Ensure the following environment variables are configured in your Vercel project settings:

| Variable Name | Description |
| :--- | :--- |
| `SERPER_API_KEY` | API Key for Google Search queries via Serper.dev |
| `GROQ_API_KEY` | API Key for Groq Cloud LLM text summarization |
| `SLACK_WEBHOOK_URL` | Incoming Webhook URL for your Slack notification channel |
| `GOOGLE_SHEETS_WEBHOOK_URL` | Google Apps Script Webhook URL for database logging |
| `SPREADSHEET_NAME` | Target Google Sheets database name |

---

## 🚀 Local Development & Deployment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AsadCH2006/AI-News-Automation-Bot.git
   cd AI-News-Automation-Bot
   ```

2. **Install dependencies locally:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app locally:**
   ```python
   python api/index.py
   ```

4. **Deploy to Vercel:**
   Push your repository to GitHub and import it directly into Vercel, or deploy via CLI:
   ```bash
   vercel --prod
   ```
