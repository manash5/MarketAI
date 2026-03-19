# 🚀 Agentic Marketing Crew — CrewAI

A multi-agent marketing system built with **CrewAI** that handles both
**content creation** and **cold outreach** for any product.

---

## 🤖 Agents

| Agent | Role | Model |
|---|---|---|
| **Head of Marketing** | Market research + strategy | `llama-3.3-70b` (Groq) |
| **Creative Content Creator** | Social posts + reel scripts + content calendar | `llama-3.3-70b` (Groq) |
| **Cold Email Template Writer** | ICP research + cold email sequences | `llama-3.1-8b-instant` (Groq) |
| **Social Media Outreacher** | LinkedIn + Instagram DM playbooks | `llama-3.1-8b-instant` (Groq) |

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

---

## 🆓 Free API Options (pick one)

| Provider | Model | Free Limits | Sign Up |
|---|---|---|---|
| **Groq** ⭐ (recommended) | `llama-3.3-70b-versatile` | 30 RPM, 14,400 req/day | https://console.groq.com |
| Google Gemini | `gemini-2.0-flash` | 15 RPM, 1,500 req/day | https://aistudio.google.com |
| Google Gemini | `gemini-2.5-flash` | 10 RPM, 500 req/day | https://aistudio.google.com |
| Cerebras | `llama-3.3-70b` | Generous free tier | https://cloud.cerebras.ai |

> **Why Groq?** It's the fastest free inference provider, supports tool use,
> has the highest free RPM (30), and works out-of-the-box with CrewAI's LLM class.

---

## 📁 Output Folder Structure

```
resources/
└── drafts/
    ├── market_research.md
    ├── marketing_strategy.md
    ├── content_calendar.md
    ├── icp_research.md
    ├── posts/
    │   ├── post_1.md
    │   ├── post_2.md
    │   ├── post_3.md
    │   ├── post_4.md
    │   └── post_5.md
    ├── reels/
    │   ├── reel_1.md
    │   └── reel_2.md
    ├── cold_emails/
    │   ├── email_persona_1.md
    │   ├── email_persona_2.md
    │   └── email_persona_3.md
    └── outreach/
        ├── linkedin_outreach.md
        └── instagram_outreach.md
```

---

## ⚙️ Setup

```bash
# 1. Install dependencies
pip install crewai crewai-tools python-dotenv groq

# 2. Configure environment
cp .env.example .env
# Fill in GROQ_API_KEY and SERPER_API_KEY

# 3. Create output directories
mkdir -p resources/drafts/posts resources/drafts/reels \
         resources/drafts/cold_emails resources/drafts/outreach

# 4. Run the crew
python crew.py
```

---

## 🔧 Swapping Models

In `crew.py`, update the `llm` and `llm_fast` variables:

```python
# Groq (default)
llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.7)

# Switch to Gemini 2.0 Flash
llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7)

# Switch to Cerebras
llm = LLM(model="cerebras/llama-3.3-70b", temperature=0.7)
```

---

## 🎯 Inputs

Customise these in `crew.py` → `__main__`:

```python
inputs = {
    "product_name": "Your Product Name",
    "target_audience": "Your Target Audience",
    "product_description": "What your product does",
    "budget": "Your Budget",
    "current_date": datetime.now().strftime("%Y-%m-%d"),
}
```