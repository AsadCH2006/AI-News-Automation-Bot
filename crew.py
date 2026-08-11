import os
from crewai import Agent, Task, Crew, Process
from tools.news_fetcher_tool import NewsFetcherTool
from tools.summarizer_tool import SummarizerTool
from tools.slack_tool import SlackBotTool
from tools.sheets_tool import SheetsLoggerTool

def run_news_pipeline():
    # Instantiate custom tools
    news_fetcher = NewsFetcherTool()
    summarizer = SummarizerTool()
    slack_bot = SlackBotTool()
    sheets_logger = SheetsLoggerTool()

    # Define Agents
    news_researcher = Agent(
        role='Senior News Researcher',
        goal='Find the absolute latest and trending news about Artificial Intelligence.',
        backstory='An expert digital researcher who scours the internet for breaking tech and AI developments.',
        tools=[news_fetcher],
        verbose=True
    )

    news_editor = Agent(
        role='Managing News Editor',
        goal='Review raw news, filter duplicates, summarize cleanly, dispatch to Slack, and log to Sheets.',
        backstory='A sharp-eyed editor who turns noisy articles into concise briefs ready for distribution.',
        tools=[summarizer, slack_bot, sheets_logger],
        verbose=True
    )

    # Define Tasks
    fetch_task = Task(
        description='Fetch the latest trending news articles regarding Artificial Intelligence using the News Fetcher Tool for topic "Artificial Intelligence".',
        expected_output='A raw block of text containing titles, snippets, and source links.',
        agent=news_researcher
    )

    publish_task = Task(
        description='Take the raw news text, generate clean summaries, post them to Slack, and log the records to Google Sheets.',
        expected_output='A confirmation string verifying that records were pushed to Slack and logged to Sheets.',
        agent=news_editor
    )

    # Assemble the Crew
    news_crew = Crew(
        agents=[news_researcher, news_editor],
        tasks=[fetch_task, publish_task],
        process=Process.sequential
    )

    result = news_crew.kickoff()
    return result