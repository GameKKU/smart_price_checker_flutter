import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

model = "ep-20250731234418-8kgvb" # Replace with your actual model ID

def get_image_input_from_user():
    """
    Prompts the user to enter a URL for an image.
    """
    while True:
        image_url = input("Please enter the URL of the image: ").strip()
        if image_url.startswith("http://") or image_url.startswith("https://"):
            return image_url
        else:
            print("Error: Invalid URL. Please enter a valid http or https URL.")
            sys.exit(1)

import os
from serpapi import GoogleSearch

def perform_serpapi_search(query):
    SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
    if not SERPAPI_API_KEY:
        print("Error: SERPAPI_API_KEY environment variable not set.")
        return []

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        return organic_results
    except Exception as e:
        print(f"Error performing SerpAPI search: {e}")
        return []

# The search_similar_images_online function is no longer used in the new flow, but keeping it for reference if needed.
# def search_similar_images_online(image_input, search_location="Global"):
#     print(f"\nSearching for similar images online for: {image_input} in {search_location}")

#     SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
#     if not SERPAPI_API_KEY:
#         print("Error: SERPAPI_API_KEY environment variable not set.")
#         return []

#     params = {
#         "q": image_input, # Use the image_input as the query
#         "engine": "google_images",
#         "ijn": "0",
#         "api_key": SERPAPI_API_KEY
#     }

#     # Add location parameter if specified and not 'Global'
#     # if search_location != "Global":
#     #     params["location"] = search_location # SerpAPI handles location for Google Images

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     image_urls = []
#     if "images_results" in results:
#         for img_result in results["images_results"]:
#             if "original" in img_result:
#                 image_urls.append(img_result["original"])
    
#     print("Found similar images:")
#     for url in image_urls:
#         print(f"- {url}")

#     return image_urls

from byteplussdkarkruntime import Ark

def analyze_image_with_llm(client, image_url, search_results=None):
    """
    Analyzes the image using the provided LLM and returns a suggested resell price range.
    """
    text_prompt = "Analyze the quality of the item based on the user-provided image and the provided search results. Suggest a resell price range for the item in Thai Baht. Consider the item's condition from the image and the prices found in the search results. Provide the answer in Thai."
    if search_results:
        text_prompt = f"Analyze the quality of the item based on the user-provided image and the following search results. Suggest a resell price range for the item in Thai Baht. Consider the item's condition from the image and the prices found in the search results. Search Results: {search_results}. Provide the answer in Thai."

    response = client.chat.completions.create(
        model="ep-20250731234418-8kgvb", # Updated Model ID
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": text_prompt},
                ],
            }
        ],
    )
    if response.usage:
        print(f"LLM Analysis - Input Tokens: {response.usage.prompt_tokens}, Output Tokens: {response.usage.completion_tokens}")
    return response.choices[0].message.content

if __name__ == "__main__":
    image_input = get_image_input_from_user()
    print(f"You selected: {image_input}")

    # If the input is a URL, we can directly use it for LLM analysis.
    # If it's a local file, you'd typically upload it first or use a service that accepts local files.
    # For this example, we'll proceed with the URL directly for LLM analysis.
    print(f"\nAnalyzing image quality and determining resell price range for: {image_input}")

    # Define the model to be used for LLM calls
    

    # Initialize the Ark client
    client = Ark(
        base_url="https://ark.ap-southeast.bytepluses.com/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),
    )

    # Step 1: LLM generates a keyword for SerpAPI search
    print("\nLLM generating search keyword...")
    keyword_prompt = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_input}},
                    {"type": "text", "text": "Based on this image, identify the main item, its series, and year of production. Only output the item, series, and year, nothing else."}
                ]
            }
        ]
    }
    try:
        keyword_response = client.chat.completions.create(**keyword_prompt)
        if keyword_response.usage:
            print(f"LLM Keyword Generation - Input Tokens: {keyword_response.usage.prompt_tokens}, Output Tokens: {keyword_response.usage.completion_tokens}")
        item_info = keyword_response.choices[0].message.content.strip()
        print(f"Identified item: {item_info}")
    except Exception as e:
        print(f"Error generating search keyword with LLM: {e}")
        sys.exit(1)

    # Step 2: Perform SerpAPI search with the generated keyword
    print("\nPerforming SerpAPI search...")
    search_query = f"{item_info} ราคา มือสอง"
    search_results = perform_serpapi_search(search_query)
    print("SerpAPI Search Results:")
    for result in search_results:
        print(f"- {result.get('title')} - {result.get('link')}")

    # Step 3: LLM analyzes search results and image to suggest price range
    print("\nLLM analyzing search results and image for price range...")
    print(f"Item identified: {item_info}")
    try:
        final_analysis = analyze_image_with_llm(client, image_input, search_results)
        print("\nLLM Analysis and Suggested Resell Price:")
        print(final_analysis)
    except Exception as e:
        print(f"Error analyzing with LLM: {e}")
        sys.exit(1)