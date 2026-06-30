import os
import json
import requests
import sys

TOFFEE_API_URL = "https://analytics.google.com/g/collect?v=2&tid=G-02M4D9SN5F&gtm=45je66q0v9189838959za200zb9193602521zd9193602521&_p=1782789372230&gcd=13l3l3l3l1l1&npa=0&dma=0&ecid=1486718028&_eu=AAAAAGQC&_fid=cj13SDHY0BiSrD0zAyOYXh&cid=1184542220.1782739083&frm=0&pscdl=noapi&rcb=10&sr=1366x768&ul=en-us&gaf=2&_s=4&tag_exp=115616985~115938465~115938468~118897920~118897930~119027224~119576881~119576885~119576891~119576895&sid=1782789372&sct=3&seg=1&dl=https://toffeelive.com/en/account/profile&dt=Account & Settings - Toffee&en=user_engagement&ep.origin=firebase&_et=3682&tfd=97517"

# .strip() cleanly removes accidental spaces or newline characters (\n) 
# that might have broken the HTTP headers
COOKIE_DATA = os.getenv("TOFFEE_COOKIE", "").strip()
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN", "").strip()

def fetch_toffee_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/",
    }
    
    # Safely inject headers only if they are not empty strings
    if COOKIE_DATA:
        headers["Cookie"] = COOKIE_DATA
        print("✅ Cookie sanitized and loaded.")
    else:
        print("⚠️ Warning: TOFFEE_COOKIE is empty.")

    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        print("✅ Auth Token sanitized and loaded.")
    
    try:
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
            print(response.text[:500])
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 An unexpected script error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
