from scrapers.indeed_scraper import search_indeed
from llm.jd_filter_llm import check_relevance
from llm.cover_letter_llm import generate_cover_letter
from appliers.email_apply import send_email
from config.settings import PROFILE
import time

def main():
    print("Starting Daily Job Apply Bot...")

    jobs = search_indeed()
    applied = 0
    max_apply = PROFILE["applications_per_day"]

    for job in jobs:
        if applied >= max_apply:
            break

        jd_text = job["title"] + "\n" + job["snippet"]
        result = check_relevance(jd_text)

        print("LLM decision:", result)

        if '"apply": true' in result.lower():
            cover = generate_cover_letter(
                job["title"], job["company"], PROFILE["keywords"]
            )

            send_email(
                PROFILE["email"],
                f"Application for {job['title']}",
                cover
            )

            print("Applied to:", job["title"])
            applied += 1
            time.sleep(5)

    print(f"Done. Total applied: {applied}")

if __name__ == "__main__":
    main()
