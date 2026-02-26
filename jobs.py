import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

url = "https://remoteok.com/remote-design-jobs"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

jobs = []

for job in soup.select("tr.job"):
    title = job.select_one("h2")
    company = job.select_one("h3")

    if title and company:
        jobs.append(f"{title.text.strip()} - {company.text.strip()}")

body = "\n".join(jobs[:15])

msg = MIMEText(body)
msg["Subject"] = "Daily UI/UX Jobs"
msg["From"] = EMAIL
msg["To"] = EMAIL

server = smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login(EMAIL, PASSWORD)
server.send_message(msg)
server.quit()
