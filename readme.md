# 🏢 UK Company Information & Officer Scraper

This project is a Python-based web scraper that collects data about UK companies and their officers from the Companies House public register:  
🔗 https://find-and-update.company-information.service.gov.uk/

---

## ⚙️ Features

- Scrapes company details:
  - Company name, number, incorporation date, address, status, SIC codes
- Scrapes officer details:
  - Name, role, DOB, nationality, country, appointment date, address
- Exports results to:
  - `companies.csv` — company-level data
  - `officers.csv` — officer-level data

---

## 📦 Installation Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/uk-company-scraper.git
cd uk-company-scraper

### Step 2 (Optional but Recommended): Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

### Step 3: Install Required Packages
pip install -r requirements.txt