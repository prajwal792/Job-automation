import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import os

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

jobs = []

# ----------------
# RemoteOK API
# ----------------
try:
    data = requests.get("https://remoteok.com/api").json()

    for job in data:
        if isinstance(job, dict):
            role = job.get("position", "")
            company = job.get("company", "")
            link = job.get("url", "")

            text = f"{role} {company}".lower()

            if "design" in text or "ux" in text or "ui" in text:
                jobs.append(f"{role} — {company}\n{link}")
except:
    pass


# ----------------
# Dribbble Jobs
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
