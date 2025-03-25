import requests as r
from bs4 import BeautifulSoup
import pandas as pd

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def get_company_tickers():
    """Retrieve company tickers and CIKs from SEC"""
    url = "https://www.sec.gov/files/company_tickers.json"

    response = r.get(url, headers=headers)

    if response.status_code == 200:
        company_data = response.json()
        print(f"Successfully retrieved data for {len(company_data)} companies")

        # Convert to DataFrame for easier handling
        companies = []
        for _, company_info in company_data.items():
            companies.append(
                {
                    "ticker": company_info["ticker"],
                    "cik": str(company_info["cik_str"]),  # Check for cik_str
                    "title": company_info["title"],
                }
            )
        df = pd.DataFrame(companies)
        print(df.head())
        return df
    else:
        print(f"Failed to retrieve company data: Status code {response.status_code}")
        return pd.DataFrame()


def get_8k_filings(cik, count=10):
    """Retrieve 8-K filings for a given CIK"""
    search_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&count={count}&output=atom"
    print(f"Search URL: {search_url}")
    response = r.get(search_url, headers=headers)

    if response.status_code != 200:
        print(
            f"Failed to retrieve filings for CIK {cik}: Status code {response.status_code}"
        )
        return []

    soup = BeautifulSoup(response.content, "xml")
    entries = soup.find_all("entry")
    filings = []
    for entry in entries:
        title = entry.find("title").text
        filing_time = entry.find("updated").text
        link_element = entry.find("link")

        # print(f"Title: {title}, Filing Time: {filing_time}, Link: {link_element}")
        if link_element:
            link = link_element.get("href")

            # Get the actual 8-K document
            filing_info = {"title": title, "filing_time": filing_time, "link": link}
            # print(filing_info)
            filings.append(filing_info)

    return filings


def get_8k_text(filing_link):
    """Extract text from an 8-K filing"""
    try:
        response = r.get(filing_link, headers=headers, timeout=10)

        if response.status_code != 200:
            print(
                f"Failed to retrieve filing content: Status code {response.status_code}"
            )
            return ""

        soup = BeautifulSoup(response.content, "html.parser")

        return soup.get_text()
    except Exception as e:
        print(f"Error retrieving filing content: {e}")
        return ""
