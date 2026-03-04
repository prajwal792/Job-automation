import requests
from bs4 import BeautifulSoup
import smtplib
import os
from datetime import datetime

EMAIL = os.getenv("prajjuprajwal330@gmail.com")
PASSWORD = os.getenv("kndjpomggrrfsnsa")
TO_EMAIL = os.getenv("prajjuprajwal330@gmail.com")

keywords = [
    "entry level data analyst",
    "junior data analyst",
    "data analyst intern",
    "business analyst fresher"
]

blocked_words = ["senior", "lead", "manager", "principal", "director"]

jobs = []

def search_indeed():
    url = "https://www.indeed.com/jobs?q=data+analyst&l=India&fromage=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select(".job_seen_beacon"):
        title = job.select_one("h2").text.strip()
        link = "https://indeed.com" + job.select_one("a")["href"]
        company = job.select_one(".companyName").text.strip()

        if any(word in title.lower() for word in blocked_words):
            continue

        jobs.append({
            "title": title,
            "company": company,
            "link": link
        })

def generate_email():
    message = f"Subject: Daily Entry-Level Data Analyst Jobs\n\n"
    message += f"Found {len(jobs)} jobs today\n\n"

    for job in jobs:
        linkedin_msg = f"""
Hi {job['company']} team,

I came across the {job['title']} role and it really interested me.
I have a background in Python, data analysis, and dashboards,
and I'm currently seeking an entry-level opportunity.

I’d love to connect and learn more.

Best regards,
Prajwal
"""

        message += f"""
{job['title']} — {job['company']}
Apply: {job['link']}

LinkedIn message:
{linkedin_msg}

-----------------------
"""

    return message

def send_email(content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, content)
    server.quit()

def main():
    search_indeed()

    if not jobs:
        print("No jobs found today")
        return

    email_content = generate_email()
    send_email(email_content)
    print("Email sent!")

if __name__ == "__main__":
    main()
