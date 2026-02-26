import requests
import smtplib
from email.mime.text import MIMEText
import os

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

data = requests.get(url, headers=headers).json()

jobs = []

for job in data:
    if isinstance(job, dict):
        position = job.get("position", "")
        company = job.get("company", "")
        link = job.get("url", "")

        text = f"{position} {company}".lower()

        if "design" in text or "ux" in text or "ui" in text:
            jobs.append(f"{position} — {company}\n{link}")

body = "\n\n".join(jobs[:10])

if body == "":
    body = "No new UI/UX jobs found today."

msg = MIMEText(body)
msg["Subject"] = "Daily UI/UX Jobs"
msg["From"] = EMAIL
msg["To"] = EMAIL

server = smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()
