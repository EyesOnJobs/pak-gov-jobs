import requests
from bs4 import BeautifulSoup
import datetime

def get_jobs():
    # Hum aik aisi site use kar rahy hain jo block nahi karti
    url = "https://www.paperpk.com/government-jobs-in-pakistan/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    jobs = []
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Latest jobs dhoondna
        job_links = soup.find_all('h2')[:10] 
        
        for link in job_links:
            title = link.get_text().strip()
            if len(title) > 10:
                jobs.append({"title": title, "dept": "Government Department", "date": str(datetime.date.today())})
        
        return jobs
    except:
        return [{"title": "Updating Jobs...", "dept": "Please wait", "date": "-"}]

def generate_html(jobs):
    job_html = ""
    for job in jobs:
        job_html += f'''
        <div class="job-card">
            <h3>{job["title"]}</h3>
            <p><strong>Org:</strong> {job["dept"]}</p>
            <p class="date">Dated: {job["date"]}</p>
            <a href="https://www.paperpk.com/" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 15px; background:#006837; color:white; text-decoration:none; border-radius:5px;">Check Details</a>
        </div>
        '''
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sarkari Jobs Pakistan</title>
        <style>
            body {{ font-family: sans-serif; background: #f4f4f4; padding: 20px; }}
            .job-card {{ background: white; margin: 10px auto; padding: 15px; max-width: 500px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-left: 5px solid #006837; text-align: left; }}
            .header {{ background: #006837; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🇵🇰 Government Jobs</h1>
            <p>Updated: {datetime.datetime.now().strftime('%d %b, %I:%M %p')}</p>
        </div>
        {job_html}
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_html(get_jobs())
