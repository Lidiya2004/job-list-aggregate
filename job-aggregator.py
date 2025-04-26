from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time



# headless browser setup
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-size=1920x1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://remoteok.com/remote-dev-jobs")

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

jobs = []
job_rows = soup.find_all('tr', class_='job')

print(f"Found {len(job_rows)} jobs")

for job in job_rows:
    try:
        td = job.find('td', class_='company')
        title = td.find('h2').get_text(strip=True) if td.find('h2') else "N/A"
        company = td.find('h3').get_text(strip=True) if td.find('h3') else "N/A"
        location_tag = td.find('div', class_='location')
        location = location_tag.get_text(strip=True) if location_tag else "Remote"
        link = job.get('data-href')
        full_link = f"https://remoteok.com{link}" if link else "N/A"

        jobs.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Link': full_link
        })
    except Exception as e:
        print(f"Error parsing job: {e}")
        continue

df = pd.DataFrame(jobs)
df.to_csv('remoteok_all_jobs.csv', index=False)
print(f"Scraped {len(df)} jobs. Saved to remoteok_all_jobs.csv")