import requests
from bs4 import BeautifulSoup
import datetime

def get_jobs():
    # Google News RSS feed for Pakistan Government Jobs (Reliable & No Blocking)
    url = "https://news.google.com/rss/search?q=government+jobs+pakistan+after:2026-01-01&hl=en-PK&gl=PK&ceid=PK:en"
    jobs = []
    
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, 'xml') # RSS is XML
        items = soup.find_all('item')
        
        for item in items[:15]:
            title = item.title.text
            link = item.link.text
            # Sirf relevant titles rakhen
            if any(x in title.lower() for x in ["job", "vacancy", "ppsc", "fpsc", "career"]):
                jobs.append({"title": title, "link": link})
        return jobs
    except:
        return []

def generate_html(jobs):
    job_cards = ""
    if not jobs:
        job_cards = "<h2 style='color:red;'>No new jobs found today.</h2>"
    else:
        for job in jobs:
            job_cards += f'''
            <div style="background:white; margin:15px auto; padding:20px; max-width:600px; border-radius:12px; border-left:8px solid #006837; text-align:left; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                <h3 style="margin:0; font-size:1.1rem; color:#1a1a1a;">{job["title"]}</h3>
                <a href="{job["link"]}" target="_blank" style="display:inline-block; margin-top:10px; color:#006837; font-weight:bold; text-decoration:none;">Read Source Details →</a>
            </div>
            '''
    
    html = f"""
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:sans-serif; background:#f8f9fa; margin:0; padding:0; text-align:center;">
        <div style="background:#006837; color:white; padding:40px;">
            <h1 style="margin:0;">🇵🇰 Real-Time Govt Jobs</h1>
            <p>Verified Source: Google News Pakistan</p>
        </div>
        <div style="padding:20px;">{job_cards}</div>
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    generate_html(get_jobs())
