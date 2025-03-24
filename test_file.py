from bs4 import BeautifulSoup
import requests as r

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

response = r.get(
    "https://finance.yahoo.com/quote/NVDA/press-releases/",
    headers=headers,
)

soup = BeautifulSoup(response.content, "html.parser")

# Extract the filing details you want. For example, the filing date, document type, and other relevant info.

# Example to extract filing date and document types:
print(soup)
