import os
import json
import requests
import sys

# Update this URL with the exact one from your F12 Network inspection tab
TOFFEE_API_URL = "https://prod-services.toffeelive.com/subscription/v1/subscriber/7f086965-7c9a-4192-b1b8-83b6ecfb90ef/subscription?offset=1&limit=100&multi_status=ACTIVE,PENDING" 
COOKIE_DATA = os.getenv("TOFFEE_COOKIE")
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN")

def fetch_toffee_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/",
        "Cookie": COOKIE_DATA,
    }
    
    # Only add authorization header if it's explicitly passed
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    
    try:
        print(True if COOKIE_DATA else False, "Cookie detected.")
        print("Sending request to Toffee API...")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=15)
        
        print(f"API Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            output_file = "toffee_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"🎉 Successfully extracted data and saved to {output_file}")
        else:
            print("❌ Server rejected request. Response body snapshot:")
            print(response.text[:500]) # Prints the first 500 characters of the error
            sys.exit(1) # Force Python to exit with an error so GitHub logs it cleanly
            
    except Exception as e:
        print(f"💥 An unexpected script error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
