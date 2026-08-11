import os
from crewai.tools import BaseTool
from groq import Groq

class SummarizerTool(BaseTool):
    name: str = "Intelligent Summarizer Tool"
    description: str = "Takes raw news text and generates short, structured summaries highlighting key points."

    def _run(self, raw_news: str) -> str:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        prompt = f"""
        Analyze the following raw news articles, remove duplicates, and provide clean, concise summaries for each distinct story. Include the headline, a 2-sentence summary, and the original link.
        
        Raw Articles:
        {raw_news}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return completion.choices[0].message.content