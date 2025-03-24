import time
import pandas as pd
from lib.utils import get_8k_filings, get_company_tickers, get_8k_text
from lib.ai_methods import get_ai_response, parse_llm_response
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()  # You'll need to create a .env file to use Gemini's API and get your free API key.

client: genai.Client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

ticker_urls = "https://www.sec.gov/files/company_tickers.json"


def main(client: genai.Client):
    companies_df = get_company_tickers()
    results = []

    # Process companies (limit to a smaller number for testing)
    for index, company in companies_df.head(100).iterrows():
        print(f"Processing {company['title']} ({company['ticker']})")

        filings = get_8k_filings(company["cik"], count=5)  # Start with a small count

        for filing in filings:
            filing_text = get_8k_text(filing["link"])
            print("filing text:\n", filing_text)

            if filing_text:
                product_name, product_description = parse_llm_response(
                    get_ai_response(
                        client, filing_text, company["title"], company["ticker"]
                    )
                )

                if product_name:  # Only add if product was found
                    results.append(
                        {
                            "company_name": company["title"],
                            "stock_name": company["ticker"],
                            "filing_time": filing["filing_time"],
                            "new_product": product_name,
                            "product_description": product_description,
                        }
                    )

            # Be nice to the SEC servers and ensure no more than 6 requests per minute
            time.sleep(10)  # Wait 10 seconds between requests

    # Convert results to DataFrame and save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("8k_product_announcements.csv", index=False)
    print(
        f"Saved {len(results_df)} product announcements to 8k_product_announcements.csv"
    )


if __name__ == "__main__":
    main(client=client)
