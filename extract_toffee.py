import os
import json
import requests
import sys

# Change this URL if you find a different API endpoint via your F12 Network inspection
TOFFEE_API_URL = "https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?VER=8&database=projects/prj-tof-analytics/databases/(default)&gsessionid=ZxOZG47CngH7OAF90Dg3tTCRwOX4VB8gLmeuGedMnXvP1OomU5WHig&SID=fB3i3WI3SrajYw5W394uiw&RID=41536&AID=34&zx=xl1m5gj44j3k&t=1" 
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
        print("✅ Cookie sanitized and loaded.")
    if AUTH_TOKEN:
        headers["Authorization"] = AUTH_TOKEN if "Bearer" in AUTH_TOKEN else f"Bearer {AUTH_TOKEN}"
        print("✅ Auth Token sanitized and loaded.")
    
    try:
        print("Sending request to Toffee API...")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=15)
        
        print(f"API Response Status Code: {response.status_code}")
        
        output_file = "toffee_data.json"
        
        if response.status_code == 200:
            data = response.json()
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"🎉 Successfully extracted data and saved to {output_file}")
            
        elif response.status_code == 204:
            # Server accepted the login/token but returned no data text
            placeholder_data = {
                "status": "success",
                "message": "Authenticated successfully, endpoint returned no body (204 No Content)."
            }
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(placeholder_data, f, indent=4)
            print(f"ℹ️ Auth verified. Placeholder metadata saved to {output_file}")
            
        else:
            print("❌ Server rejected request. Response body snapshot:")
            print(response.text[:500])
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 An unexpected script error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
