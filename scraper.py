import requests
from bs4 import BeautifulSoup
import datetime

def get_jobs():
    # Pakistan ke top job portals ki list
    sources = [
        {"name": "FPSC", "url": "https://fpsc.gov.pk/jobs/all-jobs"},
        {"name": "PPSC", "url": "https://www.ppsc.gop.pk/(S(v0vujv3zicm2p4fppn25f5uy))/Adds.aspx"},
        {"name": "NJP", "url": "https://njp.gov.pk/"},
        {"name": "Jobz.pk", "url": "https://www.jobz.pk/government-jobs/"}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    all_jobs = []

    for site in sources:
        try:
            response = requests.get(site['url'], headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Yeh hissa har site se links aur titles nikalta hai
                links = soup.find_all('a')
                for link in links:
                    title = link.get_text().strip()
                    # Filter: Sirf wo cheezein jo jobs se mutaliq hain
                    if any(x in title.lower() for x in ["job", "vacancy", "advertisement", "ad no", "apply"]):
                        if len(title) > 20:
                            all_jobs.append({"title": title, "dept": site['name']})
        except:
            continue

    # Agar koi site block ho jaye to backup ke liye Google News se real-time data le lo
    if len(all_jobs) < 5:
        google_news = "https://news.google.com/rss/search?q=government+jobs+pakistan+official&hl=en-PK&gl=PK&ceid=PK:en"
        news_res = requests.get(google_news)
        news_soup = BeautifulSoup(news_res.content, 'xml')
        for item in news_soup.find_all('item')[:10]:
            all_jobs.append({"title": item.title.text, "dept": "Official News"})

    return all_jobs

def generate_html(jobs):
    cards = ""
    for job in jobs:
        cards += f'''
        <div style="background:white; border-left:10px solid #006837; margin:15px auto; padding:20px; max-width:700px; border-radius:10px; box-shadow:0 4px 15px rgba(0,0,0,0.1); text-align:left;">
            <span style="background:#006837; color:white; padding:3px 10px; border-radius:5px; font-size:12px;">{job['dept']}</span>
            <h3 style="margin:10px 0; color:#333;">{job['title']}</h3>
            <a href="https://www.google.com/search?q={job['title']}" target="_blank" style="color:#006837; text-decoration:none; font-weight:bold;">Apply Link →</a>
        </div>
        '''

    html_code = f"""
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#eef2f3; margin:0; padding:20px; text-align:center;">
        <h1 style="color:#006837;">🇵🇰 Pakistan Govt Jobs Master Portal</h1>
        <p>Last Crawl: {datetime.datetime.now().strftime('%d %B, %Y - %I:%M %p')}</p>
        {cards}
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html_code)

if __name__ == "__main__":
    generate_html(get_jobs())
