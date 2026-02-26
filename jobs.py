import requests
import smtplib
from email.mime.text import MIMEText
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

jobs = []

headers = {"User-Agent": "Mozilla/5.0"}

try:
    r = requests.get("https://remoteok.com/api", headers=headers)
    data = r.json()

    for job in data:
        if isinstance(job, dict):

            role = job.get("position", "")
            company = job.get("company", "")
            link = job.get("url", "")

            text = (role + " " + company).lower()

            if "design" in text or "ui" in text or "ux" in text:
                jobs.append(f"{role} — {company}\n{link}")

except Exception as e:
    jobs.append("Error fetching jobs: " + str(e))


body = "\n\n".join(jobs[:10])

if not body:
    body = "No jobs found today."


msg = MIMEText(body)
msg["Subject"] = "Daily UI UX Jobs"
msg["From"] = EMAIL
msg["To"] = EMAIL


server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()
