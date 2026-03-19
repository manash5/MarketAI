from datetime import datetime
import os
import sys
import re
import time
from MarketAI.crew import TheMarketingCrew


_RETRY_AFTER_RE = re.compile(r"try again in\s+([0-9]+)m([0-9]+(?:\.[0-9]+)?)s", re.IGNORECASE)


def _parse_retry_after_seconds(message: str) -> float | None:
    match = _RETRY_AFTER_RE.search(message)
    if not match:
        return None
    minutes = int(match.group(1))
    seconds = float(match.group(2))
    return minutes * 60 + seconds


def _is_groq_rate_limit_error(message: str) -> bool:
    lowered = message.lower()
    return (
        "groqexception" in lowered
        and ("rate limit" in lowered or "rate_limit_exceeded" in lowered)
    )


def run():
    if not os.getenv("GROQ_API_KEY"):
        print(
            "❌ Missing GROQ_API_KEY.\n\n"
            "This project is configured to use Groq via LiteLLM (model='groq/...'). "
            "Create a .env file in the project root (or export the env var) and set:\n"
            "  GROQ_API_KEY=...\n"
        )
        return 1

    # 🔹 Define inputs for your agents
    inputs = {
        "product_name": "AI Powered Excel Automation Tool",
        "target_audience": "Small and Medium Enterprises (SMEs)",
        "product_description": (
            "A tool that automates repetitive tasks in Excel using AI, "
            "saving time and reducing errors."
        ),
        "budget": "Rs. 50,000",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }

    print("🚀 Starting Marketing Crew...\n")

    # 🔹 Initialize crew
    crew_instance = TheMarketingCrew()

    # 🔹 Run crew
    try:
        result = crew_instance.marketingcrew().kickoff(inputs=inputs)
    except Exception as exc:  # crewai/litellm surface provider-specific exceptions
        message = str(exc)
        if _is_groq_rate_limit_error(message):
            retry_after = _parse_retry_after_seconds(message)
            if retry_after is not None:
                print(
                    f"❌ Groq rate limit reached (daily tokens or temporary throttling).\n"
                    f"Try again in ~{int(retry_after)}s, or upgrade your Groq tier.\n"
                    "Tip: set CREWAI_AUTO_WAIT_ON_RATE_LIMIT=true to auto-wait and retry once.\n"
                )
                if os.getenv("CREWAI_AUTO_WAIT_ON_RATE_LIMIT", "").lower() in {"1", "true", "yes"}:
                    print(f"⏳ Waiting {int(retry_after)}s before retrying once...")
                    time.sleep(retry_after)
                    result = crew_instance.marketingcrew().kickoff(inputs=inputs)
                else:
                    return 1
            else:
                print(
                    "❌ Groq rate limit reached. Please wait a bit and rerun (or upgrade your Groq tier).\n"
                )
                return 1
        raise

    print("\n✅ Marketing crew completed successfully.\n")

    # 🔹 Print final result
    print("📊 FINAL OUTPUT:\n")
    print(result)
    return 0


# 🔹 Entry point
if __name__ == "__main__":
    sys.exit(run())