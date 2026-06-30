import os
import json
import subprocess
import sys
import requests

# The foundational endpoint for the Live TV matrix
TOFFEE_API_URL = "https://api.toffeelive.com/api/v2/home/live-tv"
COOKIE_DATA = os.getenv("TOFFEE_COOKIE", "").strip()
AUTH_TOKEN = os.getenv("TOFFEE_AUTH_TOKEN", "").strip()

def run_yt_dlp_fallback():
    print("🔄 Initiating platform extractor engine...")
    try:
        # We query the landing page using yt-dlp to dump the underlying channel layout JSON
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "https://toffeelive.com/en/live-tv"],
            capture_output=True,
            text=True,
            check=True
        )
        
        channels = []
        for line in result.stdout.splitlines():
            if line.strip():
                channels.append(json.loads(line))
                
        return {
            "success": True,
            "source": "extractor_engine",
            "channels_count": len(channels),
            "channels": channels
        }
    except Exception as e:
        print(f"💥 Extractor engine fallback failed: {e}")
        return None

def fetch_toffee_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/",
        "X-Platform": "Web"
    }
    
    if COOKIE_DATA:
        headers["Cookie"] = COOKIE_DATA
    if AUTH_TOKEN:
        headers["Authorization"] = AUTH_TOKEN if "Bearer" in AUTH_TOKEN else f"Bearer {AUTH_TOKEN}"
    
    output_file = "toffee_data.json"
    
    try:
        print("Attempting connection to raw Toffee API subdomain...")
        response = requests.get(TOFFEE_API_URL, headers=headers, timeout=12)
        content_type = response.headers.get('Content-Type', '')
        
        if response.status_code == 200 and "application/json" in content_type:
            raw_data = response.json()
            payload = {
                "success": True,
                "source": "direct_api",
                "channels": raw_data.get("data", raw_data)
            }
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            print(f"🎉 API JSON extraction successful! Saved to {output_file}")
            return
            
    except Exception as e:
        print(f"Direct connection timed out or was refused: {e}")
    
    # If direct API fails or returns HTML, engage the fallback engine
    print("⚠️ Direct API route blocked or unavailable. Falling back to extractor framework...")
    fallback_data = run_yt_dlp_fallback()
    
    if fallback_data:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(fallback_data, f, indent=4, ensure_ascii=False)
        print(f"🎉 Successfully generated channels data via extractor framework to {output_file}")
    else:
        print("❌ Both retrieval pathways failed.")
        sys.exit(1)

if __name__ == "__main__":
    fetch_toffee_data()
