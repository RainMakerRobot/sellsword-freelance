import requests
from bs4 import BeautifulSoup
import openai
import smtplib
from email.mime.text import MIMEText
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

SOURCES = [
    "https://weworkremotely.com/categories/remote-writing-jobs",
    "https://problogger.com/jobs/",
    "https://www.freelancewritingjobs.com/jobs/"
]

def get_links():
    links = []
    for url in SOURCES:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "job" in href or "jobs" in href:
                links.append(href if href.startswith("http") else url + href)
    return list(set(links))

def extract_text(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(" ", strip=True)[:4000]
    except:
        return ""

def evaluate(text):
    prompt = f"""
Determine if this is a freelance writing job paying at least $50/hr.
Answer only YES or NO.

{text}
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return "YES" in resp.choices[0].message["content"]

def send_email(results):
    if not results:
        return

    body = "\n\n".join(results)

    msg = MIMEText(body)
    msg["Subject"] = "Freelance Writing Jobs"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_USER")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)

def main():
    links = get_links()
    good = []

    for link in links[:30]:
        text = extract_text(link)
        if text and evaluate(text):
            good.append(link)

    send_email(good)

if __name__ == "__main__":
    main()
