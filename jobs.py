import requests
from bs4 import BeautifulSoup
import smtplib
import os
from datetime import datetime

EMAIL = os.getenv("prajjuprajwal330@gmail.com")
PASSWORD = os.getenv("kndjpomggrrfsnsa")
TO_EMAIL = os.getenv("prajjuprajwal330@gmail.com")

headers = {"User-Agent": "Mozilla/5.0"}

blocked_words = [
    "senior","lead","manager","principal",
    "director","staff","head"
]

target_words = [
    "data analyst",
    "business analyst",
    "data analytics",
    "analytics intern",
    "data intern"
]

jobs = []
seen = set()

# -------------------------
# Helper filter
# -------------------------
def is_relevant(title):

    t = title.lower()

    if any(b in t for b in blocked_words):
        return False

    if any(w in t for w in target_words):
        return True

    return False


# -------------------------
# Indeed
# -------------------------
def search_indeed():

    url = "https://in.indeed.com/jobs?q=data+analyst&l=India&fromage=1"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select(".job_seen_beacon")

    for job in cards:

        title = job.select_one("h2").text.strip()
        company = job.select_one(".companyName").text.strip()
        link = "https://in.indeed.com" + job.select_one("a")["href"]

        if link in seen:
            continue

        if not is_relevant(title):
            continue

        jobs.append({
            "title": title,
            "company": company,
            "link": link,
            "source": "Indeed"
        })

        seen.add(link)


# -------------------------
# Wellfound
# -------------------------
def search_wellfound():

    url = "https://wellfound.com/roles/data-analyst"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):

        title = a.text.strip()

        if len(title) < 10:
            continue

        if not is_relevant(title):
            continue

        link = "https://wellfound.com" + a["href"]

        if link in seen:
            continue

        jobs.append({
            "title": title,
            "company": "Startup (Wellfound)",
            "link": link,
            "source": "Wellfound"
        })

        seen.add(link)


# -------------------------
# YC Jobs
# -------------------------
def search_yc():

    url = "https://www.ycombinator.com/jobs"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):

        title = a.text.strip()

        if not is_relevant(title):
            continue

        link = a["href"]

        if link in seen:
            continue

        jobs.append({
            "title": title,
            "company": "YC Startup",
            "link": link,
            "source": "YC Jobs"
        })

        seen.add(link)


# -------------------------
# Email Builder
# -------------------------
def build_email():

    today = datetime.now().strftime("%d %b %Y")

    body = f"Subject: 📊 Entry Level Data Analyst Jobs — {today}\n\n"

    body += f"Total jobs found: {len(jobs)}\n\n"

    for j in jobs:

        linkedin = f"""
Hi {j['company']} team,

I came across the {j['title']} role and it looks like a great opportunity.

I have experience with Python, data analysis, SQL and dashboard building, and I'm actively seeking an entry-level Data Analyst role.

I'd really appreciate the chance to connect and learn more.

Best regards,
Prajwal
"""

        body += f"""
{j['title']}
Company: {j['company']}
Source: {j['source']}

Apply:
{j['link']}

LinkedIn Outreach Message:
{linkedin}

-----------------------------------------
"""

    return body


# -------------------------
# Email Sender
# -------------------------
def send_email(content):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(EMAIL, PASSWORD)

    server.sendmail(EMAIL, TO_EMAIL, content.encode("utf-8"))

    server.quit()


# -------------------------
# Main
# -------------------------
def main():

    print("Searching jobs...")

    search_indeed()
    search_wellfound()
    search_yc()

    if len(jobs) == 0:
        print("No jobs found today")
        return

    email = build_email()

    send_email(email)

    print("Email sent successfully with", len(jobs), "jobs")


if __name__ == "__main__":
    main()
