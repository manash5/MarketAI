from datetime import datetime

from crewai import Agent, Crew, Task, LLM, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool, ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# LLM Configuration — Ollama (local, no limits)
# Make sure Ollama is running in the background
# and mistral is pulled: ollama pull mistral
# ─────────────────────────────────────────────

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7,
)

llm_gemini = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7
)

llm_fast = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7,
)


# ─────────────────────────────────────────────
# Crew Definition
# ─────────────────────────────────────────────

@CrewBase
class TheMarketingCrew():
    """
    Agentic Marketing Crew for content creation and cold outreach.
    Agents:
      1. Head of Marketing          — market research + strategy
      2. Creative Content Creator   — social posts, reel scripts, content calendar
      3. Cold Email Template Writer — ICP research + cold email sequences
      4. Social Media Outreacher    — LinkedIn + Instagram DM playbooks
    """

    agents_config = 'config/agents.yaml'
    tasks_config  = 'config/tasks.yaml'

    # ── Agents ────────────────────────────────

    @agent
    def head_of_marketing(self) -> Agent:
        return Agent(
            config=self.agents_config['head_of_marketing'],
            tools=[
                FileWriterTool(),   
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=False,
            max_rpm=3,
        )

    @agent
    def creative_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_content_creator'],
            tools=[
                FileWriterTool(),
            ],
            inject_date=True,
            llm=llm_gemini,
            allow_delegation=False,
            max_iter=5,
            max_rpm=3,
        )

    @agent
    def cold_email_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['cold_email_writer'],
            tools=[
                FileWriterTool(),
            ],
            inject_date=True,
            llm=llm_fast,
            allow_delegation=False,
            max_iter=5,
            max_rpm=3,
        )

    @agent
    def social_media_outreacher(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_outreacher'],
            tools=[
                FileWriterTool(),
            ],
            inject_date=True,
            llm=llm_gemini,
            allow_delegation=False,
            max_iter=5,
            max_rpm=3,
        )

    # ── Tasks ─────────────────────────────────

    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config['market_research'],
            agent=self.head_of_marketing(),
        )

    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_marketing_strategy'],
            agent=self.head_of_marketing(),
            context=[self.market_research()],
        )

    @task
    def create_content_calendar(self) -> Task:
        return Task(
            config=self.tasks_config['create_content_calendar'],
            agent=self.creative_content_creator(),
            context=[self.prepare_marketing_strategy()],
        )

    @task
    def create_social_media_posts(self) -> Task:
        return Task(
            config=self.tasks_config['create_social_media_posts'],
            agent=self.creative_content_creator(),
            context=[self.create_content_calendar()],
        )

    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_scripts_for_reels'],
            agent=self.creative_content_creator(),
            context=[self.create_content_calendar()],
        )

    @task
    def icp_research(self) -> Task:
        return Task(
            config=self.tasks_config['icp_research'],
            agent=self.cold_email_writer(),
            context=[self.prepare_marketing_strategy()],
        )

    @task
    def write_cold_email_templates(self) -> Task:
        return Task(
            config=self.tasks_config['write_cold_email_templates'],
            agent=self.cold_email_writer(),
            context=[self.icp_research()],
        )

    @task
    def write_outreach_messages(self) -> Task:
        return Task(
            config=self.tasks_config['write_outreach_messages'],
            agent=self.social_media_outreacher(),
            context=[self.icp_research(), self.prepare_marketing_strategy()],
        )

    # ── Crew ──────────────────────────────────

    @crew
    def marketingcrew(self) -> Crew:
        """Creates the Marketing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=False,
            max_rpm=3,
        )


