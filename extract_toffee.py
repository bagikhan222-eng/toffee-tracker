import os
import json
import subprocess
import sys
import requests

# The true master application route used to fetch web catalog components
TOFFEE_API_URL = "https://toffeelive.com/api/v1/home/live-tv"
COOKIE_DATA = os.getenv("TOFFEE_COOKIE", "").strip()
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN", "").strip()

def run_yt_dlp_fallback():
    print("🔄 Engaging yt-dlp layout extractor core...")
    try:
        # We pass your valid cookies into the extractor framework to pull channels you own access to
        # Save a temporary text cookie file for the CLI if available
        cookie_arg = []
        if COOKIE_DATA:
            with open("temp_cookie.txt", "w") as c:
                c.write(COOKIE_DATA)
            cookie_arg = ["--cookies", "temp_cookie.txt"]

        result = subprocess.run(
            ["yt-dlp", "--dump-json", "https://toffeelive.com/en/live-tv"] + cookie_arg,
            capture_output=True,
            text=True,
            check=True
        )
        
        channels = []
        for line in result.stdout.splitlines():
            if line.strip():
                channels.append(json.loads(line))
                
        # Cleanup temporary cookie file
        if os.path.exists("temp_cookie.txt"):
            os.remove("temp_cookie.txt")

        return {
            "success": True,
            "source": "yt_dlp_extractor",
            "channels_count": len(channels),
            "channels": channels
        }
    except Exception as e:
        print(f"💥 Extractor engine fallback failed: {e}")
        if os.path.exists("temp_cookie.txt"):
            os.remove("temp_cookie.txt")
        return None

def fetch_toffee_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/en/live-tv",
        "X-Platform": "Web"
    }
    
    if COOKIE_DATA:
        headers["Cookie"] = COOKIE_DATA
        print("✅ Cookie loaded.")
    if AUTH_TOKEN:
        headers["Authorization"] = AUTH_TOKEN if "Bearer" in AUTH_TOKEN else f"Bearer {AUTH_TOKEN}"
        print("✅ Auth Token loaded.")
    
    output_file = "toffee_data.json"
    
    try:
        print(f"Sending request to master catalog URL: {TOFFEE_API_URL}")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=12)
        content_type = response.headers.get('Content-Type', '')
        
        if response.status_code == 200 and ("application/json" in content_type or response.text.strip().startswith(("{", "["))):
            raw_data = response.json()
            payload = {
                "success": True,
                "source": "direct_master_api",
                "channels": raw_data.get("data", raw_data)
            }
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            print(f"🎉 Channel grid extracted successfully to {output_file}")
            return
            
    except Exception as e:
        print(f"Direct catalog route returned connection issues: {e}")
    
    print("⚠️ Master endpoint blocked or structural variant found. Running yt-dlp layout process...")
    fallback_data = run_yt_dlp_fallback()
    
    if fallback_data:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(fallback_data, f, indent=4, ensure_ascii=False)
        print(f"🎉 Data cleanly cataloged via engine framework to {output_file}")
    else:
        print("❌ Both retrieval extraction arrays failed.")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
