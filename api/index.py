from flask import Flask, jsonify
import sys
import os

# Ensure the root directory is added to Python path so internal modules import smoothly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crew import run_news_pipeline

app = Flask(__name__)

@app.route("/api/run-news-bot", methods=["GET", "POST"])
def trigger_bot():
    try:
        output = run_news_pipeline()
        return jsonify({"status": "success", "result": str(output)}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)