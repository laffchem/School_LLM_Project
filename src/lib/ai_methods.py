from google import genai


def get_ai_response(client: genai.Client, text: str, company_name: str, ticker: str):
    prompt = f"""
    Extract information about new product announcements from the following SEC 8-K filing text.
    
    Company Name: {company_name}
    Stock Ticker: {ticker}
    
    8-K Filing Text:
    {text}  # Limiting text length to avoid token limits
    
    Please extract the following information:
    1. New Product Name: The name of any newly announced product or service
    2. Product Description: A concise description of the product (less than 180 characters)
    Can you figure out if there is a new product announcement in this filing? If so, please put forth your best guess into what it is.
    Anything of relevance in the filing should fit in the response as formatted below. This does not necessarily need to be a product, but I want it to fit into the response format below.
    Format your response as: 
    New Product: [product name]
    Product Description: [short description]
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text


def parse_llm_response(response):
    """Parse the LLM response to extract product name and description"""
    if "No new product found" in response:
        print("AI response indicates no new product found.")
        return None, None

    product_name = None
    product_description = None

    # Split the response into lines and try to extract the relevant information
    lines = response.strip().split("\n")
    # print(f"Parsed Response Lines: {lines}")

    for line in lines:
        print(f"Processing line: {line}")
        if line.startswith("New Product:"):
            product_name = line.replace("New Product:", "").strip()
        elif line.startswith("Product Description:"):
            product_description = line.replace("Product Description:", "").strip()
    print(product_name, product_description)
    return product_name, product_description
