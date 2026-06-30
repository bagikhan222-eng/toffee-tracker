import os
import json
import requests
import sys

# Ensure this URL matches the exact JSON asset or API route you copied from F12
TOFFEE_API_URL = "https://toffeelive.com/en/collections/5024eb274066fe74ee0b3d0239aa2fbc?_rsc=1m5z1" 
COOKIE_DATA = os.getenv("TOFFEE_COOKIE", "").strip()
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN", "").strip()

def fetch_toffee_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/",
    }
    
    if COOKIE_DATA:
        headers["Cookie"] = COOKIE_DATA
        print("✅ Cookie loaded.")
    if AUTH_TOKEN:
        headers["Authorization"] = AUTH_TOKEN if "Bearer" in AUTH_TOKEN else f"Bearer {AUTH_TOKEN}"
        print("✅ Auth Token loaded.")
    
    try:
        print("Sending request to Toffee URL...")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=15)
        
        print(f"API Response Status Code: {response.status_code}")
        
        # Verify content is JSON before parsing
        content_type = response.headers.get('Content-Type', '')
        print(f"Content-Type received: {content_type}")
        
        output_file = "toffee_data.json"
        
        if "application/json" in content_type or response.text.strip().startswith(("{", "[")):
            raw_data = response.json()
            
            # Format nicely
            channel_payload = {
                "success": True,
                "channels": raw_data.get("data", raw_data) if isinstance(raw_data, dict) else raw_data
            }
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(channel_payload, f, indent=4, ensure_ascii=False)
            print(f"🎉 JSON extraction successful! Saved to {output_file}")
            
        else:
            print("⚠️ Server sent text/HTML instead of JSON. The URL might be wrong or geo-blocked.")
            print("--- Snippet of received response ---")
            print(response.text[:1000]) # Prints the HTML structure to help you debug
            print("-------------------------------------")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 Error processing data stream: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
