from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()  # For Chrome, make sure you have 'chromedriver' installed

# Navigate to the portal
driver.get('https://www.naukri.com/data-analyst-data-scientist-data-engineer-product-analyst-product-manager-ai-ml-engineer-ml-engineer-jobs?k=data%20analyst%2C%20data%20scientist%2C%20data%20engineer%2C%20product%20analyst%2C%20product%20manager%2C%20ai%20ml%20engineer%2C%20ml%20engineer&nignbevent_src=jobsearchDeskGNB')  # Replace with the actual URL of the job portal

time.sleep(3)

job_titles = []
company_names = []
locations = []
experience_required = []
role_categories = []
industry_types = []
departments = []
employment_types = []
education_ug = []
education_pg = []
key_skills = []

def auto_scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_job_details():
    job_cards = driver.find_elements(By.CLASS_NAME, 'job-card-class')  # Update class name accordingly

    for card in job_cards:
        try:
            # Extract job title from the main page
            job_title = card.find_element(By.CLASS_NAME, 'job-title-class').text  # Update with correct class name
            job_titles.append(job_title)
        except:
            job_titles.append('N/A')

        try:
            # Extract company name from the main page
            company_name = card.find_element(By.CLASS_NAME, 'company-name-class').text  # Update with correct class name
            company_names.append(company_name)
        except:
            company_names.append('N/A')

        try:
            # Extract job location from the main page
            location = card.find_element(By.CLASS_NAME, 'location-class').text  # Update with correct class name
            locations.append(location)
        except:
            locations.append('N/A')

        try:
            # Extract experience required from the main page
            experience = card.find_element(By.CLASS_NAME, 'experience-class').text  # Update with correct class name
            experience_required.append(experience)
        except:
            experience_required.append('N/A')

        # Click the job card to navigate to the detailed job page
        try:
            card.click()
            time.sleep(2)

            try:
                role_category = driver.find_element(By.XPATH, "//span[text()='Role Category']/following-sibling::span").text
                role_categories.append(role_category)
            except:
                role_categories.append('N/A')

            try:
                industry_type = driver.find_element(By.XPATH, "//span[text()='Industry Type']/following-sibling::span").text
                industry_types.append(industry_type)
            except:
                industry_types.append('N/A')

            try:
                department = driver.find_element(By.XPATH, "//span[text()='Department']/following-sibling::span").text
                departments.append(department)
            except:
                departments.append('N/A')

            try:
                employment_type = driver.find_element(By.XPATH, "//span[text()='Employment Type']/following-sibling::span").text
                employment_types.append(employment_type)
            except:
                employment_types.append('N/A')

            try:
                ug_education = driver.find_element(By.XPATH, "//span[text()='UG']/following-sibling::span").text
                education_ug.append(ug_education)
            except:
                education_ug.append('N/A')

            try:
                pg_education = driver.find_element(By.XPATH, "//span[text()='PG']/following-sibling::span").text
                education_pg.append(pg_education)
            except:
                education_pg.append('N/A')

            try:
                skills = driver.find_element(By.XPATH, "//span[text()='Key Skills']/following-sibling::span").text
                key_skills.append(skills)
            except:
                key_skills.append('N/A')

            driver.back()
            time.sleep(2)

        except:
            print("Failed to retrieve job details")

def go_to_next_page():
    try:
        next_button = driver.find_element(By.XPATH, "//a[@class='next-page-class']")  # Update with correct class for the "Next" button
        next_button.click()
        time.sleep(3)  # Wait for the next page to load
        return True
    except:
        print("No more pages available or failed to click 'Next'.")
        return False

while True:
    auto_scroll()  # Auto scroll to load more job cards
    scrape_job_details()  # Scrape job details from the current page
    
    # Go to the next page, break the loop if no more pages are available
    if not go_to_next_page():
        break

driver.quit()

jobs_df = pd.DataFrame({
    'Job Title': job_titles,
    'Company Name': company_names,
    'Location': locations,
    'Experience Required': experience_required,
    'Role Category': role_categories,
    'Industry Type': industry_types,
    'Department': departments,
    'Employment Type': employment_types,
    'Education UG': education_ug,
    'Education PG': education_pg,
    'Key Skills': key_skills
})

jobs_df.to_csv('raw_data.csv', index=False)
