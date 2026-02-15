import requests
import time
from datetime import datetime
from datetime import timedelta

TOKEN = "8230182665:AAGs5ZEmatbidgQ1-qiaNISfoMO_u-MFfxU"
CHAT_ID = "1224266067"

KEYWORD = "embedded"
HOURS = 24

START_TIME = datetime.utcnow()

sent_jobs = set()


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def fetch_jobs():
    url = "https://remotive.com/api/remote-jobs"
    data = requests.get(url).json()
    return data["jobs"]


while True:
    print("Checking jobs...")
    jobs = fetch_jobs()

    for job in jobs:
        title = job["title"].lower()
        location = job.get("candidate_required_location", "").lower()
        pub_date = job.get("publication_date")
        job_id = job["id"]
        print(job["title"])
        print(location)
        print(pub_date)

        if pub_date:
            job_time = datetime.fromisoformat(pub_date.replace("Z", ""))

        if (
            KEYWORD in title
            and job_time > datetime.utcnow() - timedelta(hours=HOURS)
            and job_id not in sent_jobs
        ):
                message = f"""
💼 {job['title']}
🏢 {job['company_name']}
🌍 {job['candidate_required_location']}
🔗 {job['url']}
"""

                send_telegram(message)
                sent_jobs.add(job_id)
                print("Sent:", job["title"])

    time.sleep(60)
