import argparse
import time
import pandas as pd
from utils import (
    load_company_numbers,
    get_company_data,
    get_officers_data,
    save_to_csv,
    save_to_sqlite
)

def main():
    parser = argparse.ArgumentParser(description="UK Companies House Scraper")
    parser.add_argument("--input", help="File with company numbers", default="company_numbers.txt")
    parser.add_argument("--csv", help="Save to CSV", action="store_true")
    parser.add_argument("--sqlite", help="Save to SQLite", action="store_true")
    args = parser.parse_args()

    company_numbers = load_company_numbers(args.input)

    all_companies = []
    all_officers = []

    for number in company_numbers:
        print(f"Scraping company {number}")
        company_info = get_company_data(number)
        if not company_info:
            print(f"Skipping {number}")
            continue

        officer_info = get_officers_data(number)
        print(f"  Found {len(officer_info)} officers")  # <-- Added status print here

        all_companies.append(company_info)
        all_officers.extend(officer_info)
        time.sleep(1)

    if all_companies:
        print("\n=== Companies Sample ===")
        print(pd.DataFrame(all_companies).head(), "\n")

    if all_officers:
        print("\n=== Officers Sample ===")
        print(pd.DataFrame(all_officers).head(), "\n")

    if args.csv:
        save_to_csv(all_companies, all_officers)
    if args.sqlite:
        save_to_sqlite(all_companies, all_officers)


if __name__ == "__main__":
    main()
