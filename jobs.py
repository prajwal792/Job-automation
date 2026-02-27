import requests
import smtplib
import os
from email.mime.text import MIMEText

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

ENTRY_KEYWORDS = [
    "junior","entry","fresher","graduate","trainee","associate","intern","0-1","0-2"
]

ROLE_KEYWORDS = [
    "ui","ux","designer","product designer","web designer",
    "frontend","react","javascript","developer"
]

BLOCK_WORDS = [
    "senior","lead","manager","principal","director","architect","5+","7+","10+"
]

def valid_job(title):
    t = title.lower()

    entry = any(k in t for k in ENTRY_KEYWORDS)
    role = any(k in t for k in ROLE_KEYWORDS)
    not_senior = not any(k in t for k in BLOCK_WORDS)

    return entry and role and not_senior


url = "https://remotive.com/api/remote-jobs"
data = requests.get(url).json()

jobs = []

for job in data["jobs"]:
    title = job["title"]

    if valid_job(title):
        jobs.append({
            "title": title,
            "company": job["company_name"],
            "link": job["url"]
        })


message = ""

for job in jobs[:10]:
    message += f"{job['title']} — {job['company']}\n{job['link']}\n\n"

if message == "":
    message = "No matching entry level jobs today."


msg = MIMEText(message)
msg["Subject"] = "Daily Fresher Job Alert"
msg["From"] = EMAIL
msg["To"] = EMAIL


server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()
