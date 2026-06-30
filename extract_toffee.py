import os
import json
import requests
import sys

# The actual mobile app API gateway used to load the channel components
TOFFEE_API_URL = "https://edge.api.toffeelive.com/api/v1.1/home"
COOKIE_DATA = os.getenv("TOFFEE_COOKIE", "").strip()
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN", "").strip()

def fetch_toffee_data():
    # Mirroring the strict header signature used by the Toffee Android app core
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B Build/SP1A.210812.016)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "X-Platform": "Android",
        "X-App-Version": "3.1.2",
    }
    
    if COOKIE_DATA:
        headers["Cookie"] = COOKIE_DATA
        print("✅ Mobile profile cookies injected.")
    if AUTH_TOKEN:
        headers["Authorization"] = AUTH_TOKEN if "Bearer" in AUTH_TOKEN else f"Bearer {AUTH_TOKEN}"
        print("✅ Authorization payload injected.")
    
    output_file = "toffee_data.json"
    
    try:
        print("Connecting to Toffee Mobile Core Gateway...")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=15)
        
        print(f"API Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            raw_data = response.json()
            
            # The channel matrix is usually nested within specific homepage layout categories (e.g., 'Live TV')
            channels_extracted = []
            
            # Walk through the dynamic categories returned by the platform core
            categories = raw_data.get("data", {}).get("categories", []) if isinstance(raw_data, dict) else []
            
            for section in categories:
                if "live" in section.get("slug", "").lower() or "tv" in section.get("title", "").lower():
                    channels_extracted = section.get("assets", [])
                    break
            
            # If no specific categories matched, fallback and output the raw structural layer
            if not channels_extracted:
                channels_extracted = raw_data.get("data", raw_data)

            payload = {
                "success": True,
                "channels_count": len(channels_extracted) if isinstance(channels_extracted, list) else 1,
                "channels": channels_extracted
            }
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            print(f"🎉 Channel payload mapped successfully to {output_file}")
            
        else:
            print(f"❌ Mobile endpoint rejected connection. Status: {response.status_code}")
            print(response.text[:400])
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 Failed to authenticate or process stream: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
