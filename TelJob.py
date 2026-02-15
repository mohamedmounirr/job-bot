import requests
import time
from datetime import datetime, timedelta

TOKEN = "8230182665:AAGs5ZEmatbidgQ1-qiaNISfoMO_u-MFfxU"
CHAT_ID = "1224266067"

KEYWORD = "embedded"
HOURS = 24

START_TIME = datetime.utcnow()
since = datetime.utcnow() - timedelta(hours=24)

sent_jobs = set()

def fetch_arbeitnow():
    url = "https://www.arbeitnow.com/api/job-board-api"
    return requests.get(url).json()["data"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def fetch_jobs():
    url = "https://remotive.com/api/remote-jobs"
    data = requests.get(url).json()
    return data["jobs"]


while True:
    print("Checking jobs...")
    jobs = fetch_jobs() + fetch_arbeitnow()

    for job in jobs:
        title = (job.get("title") or job.get("position","")).lower()
        location = job.get("candidate_required_location", "Not specified")
        job_id = job.get("id") or job.get("slug") or job.get("url")
        pub_date = job.get("publication_date")

        print(job["title"])
        print(location)
        ##print(pub_date)
        print("CHECK:", title, pub_date, location)
        if pub_date:
            job_time = datetime.fromisoformat(pub_date.replace("Z",""))
        else:
            job_time = datetime.utcnow()   # اعتبرها جديدة

        if (
            KEYWORD in title
            and job_time > since
            and job_id not in sent_jobs
        ):
                
                message = f"""
💼 {job['title']}
🏢 {job['company_name']}
🌍 {location}
🔗 {{link}}
"""
                send_telegram(message)
                sent_jobs.add(job_id)
                print("Sent:", job["title"])

    time.sleep(60)
