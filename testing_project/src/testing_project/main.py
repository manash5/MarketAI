from datetime import datetime
from testing_project.crew import TheMarketingCrew


def run():
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
    result = crew_instance.marketingcrew().kickoff(inputs=inputs)

    print("\n✅ Marketing crew completed successfully.\n")

    # 🔹 Print final result
    print("📊 FINAL OUTPUT:\n")
    print(result)


# 🔹 Entry point
if __name__ == "__main__":
    run()