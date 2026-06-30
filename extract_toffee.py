import os
import json
import requests
import sys

# Change this URL if you find a different API endpoint via your F12 Network inspection
TOFFEE_API_URL = "https://pubads.g.doubleclick.net/gampad/ads?slotname=/22419763167/AnyMind_BD_Toffee_Website_Live_LiveSports_FIFA_C1_pre_Instream&sz=640x360|640x480|1280x720|1920x1080&url=https://toffeelive.com/en/watch/9TTspp4Bb1O6C9k7yfhl&unviewed_position_start=1&env=vp&gdfp_req=1&ad_rule=0&output=xml_vast4&video_url_to_fetch=https://toffeelive.com/&useragent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0,gzip(gfe)&vad_type=linear&vpos=preroll&pod=1&vrid=1394760&min_ad_duration=0&max_ad_duration=90000&ppos=1&lip=true&sid=5E59AEBD-490D-4B57-A714-72384CF99BEB&cookie_enabled=1&correlator=4080349782796376&eoidce=1&ged=ve4_td640_tt1_pd640_la640000_er78.0.245.1349_vi0.0.342.1349_vp100_ts1_eb24171&is_amp=0&npa=false&osd=2&ptt=20&pvsid=2900080003547884&vis=1&u_so=l&adk=1405868112&dt=1782790108696&omid_p=Google1/h.3.774.0&scor=2429448489420294&sdk_apis=2,7,8&frm=0&dc_vo=0&vpa=auto&vpmute=false&eid=95322027,95331589,95332046&hl=en&media_url=blob:https%3a//toffeelive.com/717aacc0-6a78-437f-9cf2-55884d336f2a&plcmt=1&sdki=100000445&sdkv=h.3.774.0&sdr=1&kfa=0&tfcd=0&ctv=0&vo=0&top=https://toffeelive.com/en/watch/9TTspp4Bb1O6C9k7yfhl&loc=https://toffeelive.com/en/watch/9TTspp4Bb1O6C9k7yfhl" 
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
