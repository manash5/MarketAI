# 🚀 Agentic Marketing Crew — CrewAI

An AI-powered multi-agent marketing system built with **CrewAI** that
autonomously handles your entire marketing workflow — from market research
and strategy, to content creation and cold outreach — all from a single
command.

You provide your product details. The crew does the rest.

---

## 💡 What Does This Project Do?

Given a product name, description, target audience, and budget, this system
spins up 4 specialised AI agents that work sequentially to produce a full
week's worth of marketing output:

- **Market research** — competitor analysis, customer pain points, channel insights
- **Marketing strategy** — positioning, ICP, budget allocation, weekly plan
- **Content calendar** — 7-day schedule with posting times per platform
- **Social media posts** — 2 platform-native posts (LinkedIn + Instagram)
- **Reel script** — 1 Instagram reel script with hook, scenes, and CTA
- **ICP research** — 3 detailed buyer personas with pain points and language
- **Cold email templates** — 2 personalised sequences with A/B subject lines and follow-ups
- **Social outreach playbooks** — LinkedIn and Instagram DM sequences per persona

All outputs are saved as markdown files to your local `resources/drafts/` folder,
ready for review, editing, and publishing.

---

## 🤖 Agents

| Agent | Role | Responsibilities |
|---|---|---|
| **Head of Marketing** | Strategy Lead | Market research, marketing strategy |
| **Creative Content Creator** | Content Lead | Content calendar, social posts, reel scripts |
| **Cold Email Template Writer** | Outreach Lead | ICP research, cold email sequences |
| **Social Media Outreacher** | DM Lead | LinkedIn + Instagram outreach playbooks |

---

## 📋 Task Pipeline (Sequential)

```
1. market_research              → Head of Marketing
2. prepare_marketing_strategy   → Head of Marketing
3. create_content_calendar      → Creative Content Creator
4. create_social_media_posts    → Creative Content Creator
5. prepare_scripts_for_reels    → Creative Content Creator
6. icp_research                 → Cold Email Writer
7. write_cold_email_templates   → Cold Email Writer
8. write_outreach_messages      → Social Media Outreacher
```

Each task's output is automatically passed as context to the next relevant
task via CrewAI's memory system — no manual handoff needed.

---

## 📁 Output Folder Structure

After a successful run, your `resources/drafts/` folder will contain:

```
resources/
└── drafts/
    ├── market_research.md       ← competitor + trend analysis
    ├── marketing_strategy.md    ← full one-week strategy
    ├── content_calendar.md      ← 7-day posting schedule
    ├── icp_research.md          ← 3 buyer personas
    ├── posts/
    │   ├── post_1.md            ← LinkedIn post
    │   └── post_2.md            ← Instagram post
    ├── reels/
    │   └── reel_1.md            ← Instagram reel script
    ├── cold_emails/
    │   ├── email_persona_1.md   ← cold email sequence for persona 1
    │   └── email_persona_2.md   ← cold email sequence for persona 2
    └── outreach/
        ├── linkedin_outreach.md ← LinkedIn DM playbook
        └── instagram_outreach.md← Instagram DM playbook
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install crewai crewai-tools python-dotenv
```

### 2. Configure environment
```bash
cp .env.example .env
```
Fill in your API keys in `.env`:
```env
SERPER_API_KEY=your_serper_key   # https://serper.dev (free: 2,500 searches/month)
```

### 3. Set up Ollama (local LLM — no API cost)
```bash
# Install Ollama from https://ollama.com
# Then pull a model:
ollama pull mistral        # recommended for most machines
ollama pull llama3.1       # better quality if you have 16GB+ RAM
```

### 4. Create output directories
```bash
mkdir -p resources/drafts/posts resources/drafts/reels \
         resources/drafts/cold_emails resources/drafts/outreach
```

### 5. Run the crew
```bash
python crew.py
```

---

## 🎯 Customise Your Inputs

Edit these in `crew.py` under `if __name__ == "__main__"`:

```python
inputs = {
    "product_name": "Your Product Name",
    "target_audience": "Your Target Audience",
    "product_description": "What your product does and who it helps",
    "budget": "Your Marketing Budget",
    "current_date": datetime.now().strftime("%Y-%m-%d"),
}
```

---

## 🔧 Swapping Models

The crew uses **Ollama (local)** by default — no API costs, no rate limits.
Update the `llm` variables at the top of `crew.py` to switch:

```python
# Ollama — local, free, no limits (default)
llm = LLM(model="ollama/mistral", base_url="http://localhost:11434", temperature=0.7)

# Gemini 2.0 Flash — free API, best tool-use reliability
llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7)
# Requires: GEMINI_API_KEY in .env — get free key at https://aistudio.google.com

# Groq — fast free API, good for prototyping
llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.7)
# Requires: GROQ_API_KEY in .env — get free key at https://console.groq.com
```

---

## ⚠️ Known Limitations with Local Models

Running local models (Mistral, Llama) works but has some quirks:

| Issue | Cause | Status |
|---|---|---|
| Tool name hallucination | Small models call wrong tool names | Handled via `max_iter=3` |
| Encoding errors | Emojis in output on Windows | Fixed via `UTF8FileWriterTool` |
| Slow inference | Large context on CPU | Reduced via short task descriptions |
| Timeout on later tasks | Accumulated context too large | Reduced via minimal context chaining |

For the most reliable results, use **Gemini 2.0 Flash** (free API key from Google AI Studio).

---

## 🗂️ Project Structure

```
marketAI/
├── crew.py                  ← main entry point
├── config/
│   ├── agents.yaml          ← agent roles, goals, backstories
│   └── tasks.yaml           ← task descriptions and expected outputs
├── resources/
│   └── drafts/              ← all generated marketing content
├── .env                     ← your API keys (never commit this)
├── .env.example             ← template for .env
└── README.md                ← this file
```