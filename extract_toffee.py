import os
import json
import requests

# 1. Define the API endpoint and headers
# (It's best practice to pass sensitive data via Environment Variables)
TOFFEE_API_URL = "https://toffeelive.com/api/v1/user/subscriptions" # Replace with the actual inspected endpoint
COOKIE_DATA = os.getenv("TOFFEE_COOKIE")
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN")

def fetch_toffee_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Cookie": COOKIE_DATA,
        "Authorization": f"Bearer {AUTH_TOKEN}" if AUTH_TOKEN else ""
    }
    
    try:
        print("Fetching data from Toffee...")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Save the extracted data to a file
            output_file = "toffee_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Successfully extracted data and saved to {output_file}")
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_toffee_data()
