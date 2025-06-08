import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os

BASE_URL = "https://find-and-update.company-information.service.gov.uk"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_company_numbers(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]
    
def get_company_data(company_number):
    url = f"{BASE_URL}/company/{company_number}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200: return None
    
    soup = BeautifulSoup(r.text, 'html.parser')
    def safe_text(selector):
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else "N/A"
    
# function to get the company data.
def get_company_data(company_number):
    url = f"{BASE_URL}/company/{company_number}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, 'html.parser')

    def safe_text(selector):
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else "N/A"

    #function to get the dt tag (description of term)
    #function definition of what definition term is to find. In this case, I have to find the id tag of company incorporation date.
    dt_tag_selector = soup.find('dt', id='company-birth-type')
    incorporation_date = dt_tag_selector.find_next_sibling('dd').get_text(strip=True) if dt_tag_selector else "N/A"

    #function for getting the description details of the element "Registered office address"
    dt_address = soup.find('dt', string=lambda text: text and "Registered office address" in text)
    registered_address = dt_address.find_next_sibling('dd').get_text(strip=True).replace("\n", ", ") if dt_address else "N/A"

    # Company Status
    dt_status = soup.find('dt', string=lambda text: text and "status" in text.lower())
    company_current_status = dt_status.find_next_sibling('dd').get_text(strip=True).replace("\n", ", ") if dt_status else "N/A"

    # SIC Codes
    sic_codes = ", ".join([span.get_text(strip=True) for span in soup.select("span[id^=sic]")]) or "N/A"

    # Final structured company data
    company = {
        "Company Number": company_number,
        "Company Name": safe_text('h1.heading-xlarge'),
        "Incorporation Date": incorporation_date,
        "Registered Office Address": registered_address,
        "Status": company_current_status,
        "SIC Codes": sic_codes
    }

    return company

def get_officers_data(company_number):
    url = f"{BASE_URL}/company/{company_number}/officers"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    officers = []

    # Each officer name is under <h2 class="heading-medium">
    for h2 in soup.select("h2.heading-medium"):
        officer_name_tag = h2.select_one("span[id^=officer-name] a.govuk-link")
        officer_name = officer_name_tag.get_text(strip=True) if officer_name_tag else "N/A"

        container = h2.find_parent("li") or h2.find_parent("div") or h2.parent

        def get_dd_after_dt(label):
            dt = container.find("dt", string=lambda text: text and label.lower() in text.lower())
            if not dt:
                return "N/A"
            dd = dt.find_next_sibling("dd")
            return dd.get_text(strip=True) if dd else "N/A"

# this is the structure of the generated object, that will be translated into csv file.
        officer = {
            "Company Number": company_number,
            "Officer Name": officer_name,
            "Role": get_dd_after_dt("role"),
            "Date of Birth": get_dd_after_dt("date of birth"),
            "Nationality": get_dd_after_dt("nationality"),
            "Country of Residence": get_dd_after_dt("country of residence"),
            "Appointed On": get_dd_after_dt("appointed on"),
            "Address": get_dd_after_dt("correspondence address")
        }
        officers.append(officer)
    return officers

# function that saves the scraped data from the web into dedicated csv folders.
def save_to_csv(companies, officers):
    companies_path = os.path.abspath("companies.csv")
    officers_path = os.path.abspath("officers.csv")

    pd.DataFrame(companies).to_csv(companies_path, index=False)
    pd.DataFrame(officers).to_csv(officers_path, index=False)

    print(f"Saved companies to {companies_path}")
    print(f"Saved officers to {officers_path}")
    
def save_to_sqlite(companies, officers, db_name="companies.db"):
    conn = sqlite3.connect(db_name)
    pd.DataFrame(companies).to_sql("companies", conn, if_exists="append",index=False)
    pd.DataFrame(officers).to_sql("officers", conn, if_exists="append", index=False)
    conn.close()
    print("Saved to SQLite")