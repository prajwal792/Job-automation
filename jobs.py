import requests
import smtplib
import os
from email.mime.text import MIMEText

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

ENTRY_WORDS = [
"junior","fresher","entry","graduate","associate","intern","trainee","0-1","0-2"
]

ROLE_WORDS = [
"frontend","react","javascript","ui","ux","web","product designer"
]

BLOCK = [
"senior","lead","staff","principal","manager","director","architect","5+","7+","10+"
]


def is_valid(title):
    t = title.lower()

    entry = any(w in t for w in ENTRY_WORDS)
    role = any(w in t for w in ROLE_WORDS)
    bad = any(w in t for w in BLOCK)

    return entry and role and not bad


def fetch_remotive():
    url = "https://remotive.com/api/remote-jobs"
    data = requests.get(url).json()

    results = []

    for job in data["jobs"]:
        if is_valid(job["title"]):
            results.append({
                "title": job["title"],
                "company": job["company_name"],
                "url": job["url"]
            })

    return results


def fetch_remoteok():
    url = "https://remoteok.com/api"
    data = requests.get(url).json()

    results = []

    for job in data[1:]:
        title = job.get("position","")

        if is_valid(title):
            results.append({
                "title": title,
                "company": job.get("company",""),
                "url": job.get("url","")
            })

    return results


jobs = []
jobs += fetch_remotive()
jobs += fetch_remoteok()

# remove duplicates
unique = {(j["title"], j["company"]): j for j in jobs}
jobs = list(unique.values())

jobs = jobs[:20]

report = ""

for job in jobs:

    linkedin_msg = f"""
Hi {job['company']} team,

I’m a frontend developer skilled in JavaScript and React and very interested in this role.

Would love to contribute and learn from your team.

Thanks!
"""

    report += f"""
{job['title']} — {job['company']}
Apply: {job['url']}

LinkedIn Message:
{linkedin_msg}

------------------------
"""

if report == "":
    report = "No fresher roles found today."

msg = MIMEText(report)

msg["Subject"] = "Daily Fresher Developer Jobs"
msg["From"] = EMAIL
msg["To"] = EMAIL

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()
