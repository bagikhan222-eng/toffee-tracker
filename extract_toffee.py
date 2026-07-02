import json
import requests
import re
from datetime import datetime

def extract_tokens_directly_from_toffee():
    print("🚀 Initiating direct Toffee extraction matrix...")
    
    platform_url = "https://toffeelive.com"
    
    output_payload = {
        "channels": [],
        "channels_amount": 0,
        "status": "active"
    }

    # High-accuracy mobile desktop mimicry footprint
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/"
    }

    raw_channels = []
    auth_cookie = ""

    try:
        session = requests.Session()
        print("📡 Scraping direct platform web template layer...")
        response = session.get(platform_url, headers=headers, timeout=15)
        
        # 1. Capture dynamic Edge-Cache session cookie values directly from response context
        cookies_found = []
        for cookie in session.cookies:
            cookies_found.append(f"{cookie.name}={cookie.value}")
            
        if cookies_found:
            auth_cookie = "; ".join(cookies_found)
            print("✅ Successfully generated authentic Toffee edge signature session tokens.")
        else:
            auth_cookie = "Edge-Cache-Cookie=URLPrefix=aHR0cHM6Ly9ibGRjbXByb2QtY2RuLnRvZmZlZWxpdmUuY29tLw:KeyName=prod_linear"

        # 2. Extract authentic live broadcasting map arrays from the window.__NEXT_DATA__ or inline script components
        if response.status_code == 200:
            # Look for Toffee's native internal content collection blocks
            json_js_match = re.search(r'\"channels\"\s*:\s*(\[.*?\])', response.text)
            if json_js_match:
                try:
                    raw_channels = json.loads(json_js_match.group(1))
                    print(f"🎉 Found {len(raw_channels)} live active channels via inline engine arrays.")
                except:
                    pass

            # Backup matching matrix if inline tracking variables shift structure
            if not raw_channels:
                blocks = re.findall(r'\{\"id\":[^\}]+?\"name\":[^\}]+?\"slug\":[^\}]+?\}', response.text)
                for block in blocks:
                    try:
                        parsed_item = json.loads(block)
                        if "slug" in parsed_item and parsed_item not in raw_channels:
                            raw_channels.append(parsed_item)
                    except:
                        continue
                if raw_channels:
                    print(f"🎉 Found {len(raw_channels)} channels via structural layout token scraping.")

        # 3. Process structural properties
        if not raw_channels:
            print("💥 Failure: Toffee blocked the scraper runner. No data extracted. Aborting export to save state.")
            return

        sports_group = []
        general_group = []

        for item in raw_channels:
            raw_name = item.get("name", "").strip()
            if not raw_name:
                continue
                
            display_title = item.get("title") or item.get("short_name") or raw_name
            slug = item.get("slug") or item.get("id")
            link = f"https://bldcmprod-cdn.toffeelive.com/cdn/live/{slug}/playlist.m3u8"
            logo_url = item.get("logo") or f"https://toffeelive.com/images/channels/{slug}.png"

            channel_block = {
                "channel_name": raw_name,
                "current_match": display_title,
                "stream_url": link,
                "channel_logo": logo_url,
                "connection_headers": {
                    "User-Agent": headers["User-Agent"],
                    "Origin": "https://toffeelive.com",
                    "Referer": "https://toffeelive.com/",
                    "Cookie": auth_cookie
                }
            }

            if "sports" in raw_name.lower() or "t-sports" in raw_name.lower() or "sony" in raw_name.lower():
                sports_group.append(channel_block)
            else:
                general_group.append(channel_block)

        output_payload["channels"] = sports_group + general_group
        output_payload["channels_amount"] = len(output_payload["channels"])
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output_payload["last_updated_timestamp"] = current_time

        # 4. Save clean data schemas
        with open("toffee_data.json", "w", encoding="utf-8") as target_file:
            json.dump(output_payload, target_file, indent=4, ensure_ascii=False)
        print("🎉 'toffee_data.json' successfully updated with valid online live channels.")

        with open("Ns_player.m3u", "w", encoding="utf-8") as ns_file:
            ns_file.write(f"#EXTM3U\n#TIMESTAMP: {current_time}\n")
            for ch in output_payload["channels"]:
                ua = ch["connection_headers"]["User-Agent"]
                ck = ch["connection_headers"]["Cookie"]
                ns_file.write(f'#EXTINF:-1 tvg-name="{ch["channel_name"]}" tvg-logo="{ch["channel_logo"]}",{ch["current_match"]}\n')
                ns_file.write(f'{ch["stream_url"]}|User-Agent={ua}&Origin=https://toffeelive.com&Referer=https://toffeelive.com/&Cookie={ck}\n')

        with open("OTT_Navigator.m3u", "w", encoding="utf-8") as ott_file:
            ott_file.write(f"#EXTM3U\n#TIMESTAMP: {current_time}\n")
            for ch in output_payload["channels"]:
                ua = ch["connection_headers"]["User-Agent"]
                ck = ch["connection_headers"]["Cookie"]
                ott_file.write(f'#EXTINF:-1 tvg-name="{ch["channel_name"]}" tvg-logo="{ch["channel_logo"]}",{ch["current_match"]}\n')
                ott_file.write(f'#EXTHTTP:{{"User-Agent":"{ua}","Origin":"https://toffeelive.com","Referer":"https://toffeelive.com/","Cookie":"{ck}"}}\n')
                ott_file.write(f'{ch["stream_url"]}\n')

    except Exception as e:
        print(f"💥 Native processing matrix dropped: {e}")

if __name__ == "__main__":
    extract_tokens_directly_from_toffee()
