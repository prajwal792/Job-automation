import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import os

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

KEYWORDS = [
    "junior",
    "entry",
    "associate",
    "ui",
    "ux",
    "product designer"
]

LOCATIONS = [
    "remote",
    "india",
    "bangalore"
]

jobs = []


def is_relevant(text):
    text = text.lower()
    return any(k in text for k in KEYWORDS)


# ----------------
# RemoteOK
# ----------------
try:
    data = requests.get("https://remoteok.com/api").json()

    for job in data:
        if isinstance(job, dict):

            role = job.get("position", "")
            company = job.get("company", "")
            link = job.get("url", "")
            location = job.get("location", "")

            combined = f"{role} {company} {location}".lower()

            if is_relevant(combined):
                jobs.append({
                    "role": role,
                    "company": company,
                    "link": link,
                    "location": location
                })
except:
    pass


# ----------------
# Dribbble
# ----------------
try:
    url = "https://dribbble.com/jobs"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select("a.job-board-item"):
        title = job.select_one(".job-board-item__title")
        company = job.select_one(".job-board-item__company")

        if title and company:

            text = title.text.lower()

            if is_relevant(text):

                link = "https://dribbble.com" + job["href"]

                jobs.append({
                    "role": title.text.strip(),
                    "company": company.text.strip(),
                    "link": link,
                    "location": "Unknown"
                })
except:
    pass


# Remove duplicates
unique = []
seen = set()

for j in jobs:
    key = j["role"] + j["company"]
    if key not in seen:
        seen.add(key)
        unique.append(j)

jobs = unique[:20]


# ----------------
# Format Email
# ----------------
lines = []

for i, job in enumerate(jobs, 1):
    lines.append(
        f"{i}. {job['role']} — {job['company']}\n"
        f"Location: {job['location']}\n"
        f"Apply: {job['link']}\n"
    )

body = "\n".join(lines)

if not body:
    body = "No relevant UI/UX jobs found today."

msg = MIMEText(body)
msg["Subject"] = "Daily Entry-Level UI/UX Jobs"
msg["From"] = EMAIL
msg["To"] = EMAIL

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select("a.job-board-item"):
        title = job.select_one(".job-board-item__title")
        company = job.select_one(".job-board-item__company")

        if title and company:
            text = title.text.lower()

            if "designer" in text or "ux" in text or "ui" in text:
                link = "https://dribbble.com" + job["href"]
                jobs.append(f"{title.text} — {company.text}\n{link}")
except:
    pass


# ----------------
# Limit results
# ----------------
jobs = list(dict.fromkeys(jobs))[:20]

body = "\n\n".join(jobs)

if body.strip() == "":
    body = "No UI/UX jobs found today."

msg = MIMEText(body)
msg["Subject"] = "Daily UI/UX Startup Jobs"
msg["From"] = EMAIL
msg["To"] = EMAIL

server = smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()
