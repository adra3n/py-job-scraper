import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(location, country, job_title):
    try:
        #target url
        target_url = f"https://{country}.indeed.com/jobs?q={job_title}&l={location}"
        
        #request
        response = requests.get(target_url)
        response.raise_for_status()  #check response
        soup = BeautifulSoup(response.content, "html.parser")

        #job count
        job_count_span = soup.find("span", class_="jobsearch-JobCountAndSortPane-jobCount")
        job_count_text = job_count_span.text.strip()
        job_count = int(job_count_text.split()[0])
        print(f"Job count: {job_count}\n")

        #jobs
        job_listings = []

        job_cards = soup.find_all("div", class_="resultContent")
        for card in job_cards:
            title = card.find("h2", class_="jobTitle").text.strip()
            company = card.find("span", class_="company_name").text.strip()
            location = card.find("div", class_="company_location").text.strip()
            metadata = card.find("div", class_="metadata").text.strip()

            job_listings.append({
                "title": title,
                "company": company,
                "location": location,
                "metadata": metadata
            })

        for job in job_listings:
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Meta Data: {job['metadata']}")
            print("\n")

    except requests.RequestException as e:
        print(f"error fetching data: {e}")

if __name__ == "__main__":
    location_input = input("Enter the location (e.g., istanbul): ")
    country_input = input("Enter the country code (e.g., tr): ")
    job_title_input = input("Enter the job title (e.g., developer): ")

    scrape_indeed_jobs(location_input, country_input, job_title_input)
