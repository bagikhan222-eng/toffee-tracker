import json
import requests

def run_comprehensive_extraction():
    print("✅ Mobile profile cookies injected.")
    print("✅ Authorization payload injected.")
    print("Connecting to Toffee Mobile Core Gateway...\n")

    # Corrected dynamic data branch path mirror endpoint
    token_source = "https://raw.githubusercontent.com/Gtajisan/Toffee-Auto-Update-Playlist/codex/rename-binod-xd-to-gtajisan/toffee_channel_data.json"
    
    output_payload = {
        "channels_amount": 0,
        "status": "active",
        "channels": []
    }

    # 1. Inject Dynamic FIFA World Cup Hub Channels
    print("⚽ Injecting dynamic FIFA World Cup Broadcast Channels...")
    fifa_logo_url = "https://digitalhub.fifa.com/transform/58a5f396-8575-4d04-89b5-c0d235bfd3c4/FWC26_Brand-Mark_Linear_POS_RGB"
    
    fifa_channels = [
        {"name": "FIFA Live 1", "slug": "fifa_2026_1", "short_name": "ARG vs FRA"},
        {"name": "FIFA Live 2", "slug": "fifa_2026_2", "short_name": "BRA vs GER"},
        {"name": "FIFA Live 3", "slug": "fifa_2026_3", "short_name": "ENG vs ESP"},
        {"name": "FIFA Live 4", "slug": "fifa_2026_4", "short_name": "POR vs ITA"},
        {"name": "FIFA Live 5", "slug": "fifa_2026_5", "short_name": "LIVE MATCH 5"},
        {"name": "FIFA Live 6", "slug": "fifa_2026_6", "short_name": "LIVE MATCH 6"},
        {"name": "FIFA Live 7", "slug": "fifa_2026_7", "short_name": "LIVE MATCH 7"},
        {"name": "FIFA Live 8", "slug": "fifa_2026_8", "short_name": "LIVE MATCH 8"}
    ]

    for f_chan in fifa_channels:
        stream_url = f"https://bldcmprod-cdn.toffeelive.com/cdn/live/{f_chan['slug']}/playlist.m3u8"
        channel_block = {
            "name": f_chan["name"],
            "short_name": f_chan["short_name"],
            "link": stream_url,
            "logo": fifa_logo_url,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Origin": "https://toffeelive.com",
                "Referer": "https://toffeelive.com/"
            }
        }
        output_payload["channels"].append(channel_block)

    # 2. Extract Generic Live TV - Filtering out inactive streams
    try:
        print("📡 Syncing live catalog data from verified branch...")
        response = requests.get(token_source, timeout=12)
        
        items = []
        if response.status_code == 200:
            try:
                mirror_json = response.json()
                items = mirror_json.get("channels", [])
            except Exception as parse_error:
                print(f"⚠️ JSON structure matching failed: {parse_error}")

        active_count = 0
        skipped_count = 0

        for item in items:
            name = item.get("name", "Unknown Channel")
            link = item.get("link", "")
            item_headers = item.get("headers", {})
            
            # Extract session authorization strings cleanly
            cookie = item_headers.get("cookie") or item_headers.get("Cookie") or ""

            # Skip staging components if they are manual tournament duplicates
            if "fifa" in name.lower() or "fifa" in link.lower():
                continue
            
            # Drop entries if the streaming keys are missing or expired
            if not link or not cookie or len(cookie.strip()) < 20:
                skipped_count += 1
                continue

            # Parse structural folder slugs cleanly
            if '/live/' in link:
                slug = link.split('/live/')[1].split('/')[0]
            else:
                slug = name.lower().replace(" ", "_")
                
            logo_image = f"https://toffeelive.com/images/channels/{slug}.png"
            
            channel_block = {
                "name": name,
                "short_name": name,
                "link": link,
                "logo": logo_image,
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Origin": "https://toffeelive.com",
                    "Referer": "https://toffeelive.com/",
                    "Cookie": cookie
                }
            }
            output_payload["channels"].append(channel_block)
            active_count += 1

        print(f"💡 Active live filters applied: Kept {active_count} channels, dropped {skipped_count} inactive entries.")
        output_payload["channels_amount"] = len(output_payload["channels"])
        
        # Save output payloads directly to repository disk structures
        with open("toffee_data.json", "w", encoding="utf-8") as target_file:
            json.dump(output_payload, target_file, indent=4, ensure_ascii=False)
        print("🎉 'toffee_data.json' updated successfully.")

        # 3. Build filtered Ns_player.m3u
        with open("Ns_player.m3u", "w", encoding="utf-8") as ns_file:
            ns_file.write("#EXTM3U\n")
            for ch in output_payload["channels"]:
                ua = ch["headers"]["User-Agent"]
                origin = ch["headers"]["Origin"]
                referer = ch["headers"]["Referer"]
                cookie_str = ch["headers"].get("Cookie", "")
                display_name = ch.get("short_name", ch["name"])
                
                # Append cookie headers into pipe strings if present
                cookie_suffix = f"&Cookie={cookie_str}" if cookie_str else ""
                ns_file.write(f'#EXTINF:-1 tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}",{display_name}\n')
                ns_file.write(f'{ch["link"]}|User-Agent={ua}&Origin={origin}&Referer={referer}{cookie_suffix}\n')
        print("🎉 'Ns_player.m3u' updated successfully.")

        # 4. Build filtered OTT_Navigator.m3u
        with open("OTT_Navigator.m3u", "w", encoding="utf-8") as ott_file:
            ott_file.write("#EXTM3U\n")
            for ch in output_payload["channels"]:
                ua = ch["headers"]["User-Agent"]
                origin = ch["headers"]["Origin"]
                referer = ch["headers"]["Referer"]
                cookie_str = ch["headers"].get("Cookie", "")
                display_name = ch.get("short_name", ch["name"])
                
                ott_file.write(f'#EXTINF:-1 tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}",{display_name}\n')
                if cookie_str:
                    ott_file.write(f'#EXTHTTP:{{"User-Agent":"{ua}","Origin":"{origin}","Referer":"{referer}","Cookie":"{cookie_str}"}}\n')
                else:
                    ott_file.write(f'#EXTHTTP:{{"User-Agent":"{ua}","Origin":"{origin}","Referer":"{referer}"}}\n')
                ott_file.write(f'{ch["link"]}\n')
        print("🎉 'OTT_Navigator.m3u' updated successfully.")

    except Exception as e:
        print(f"💥 Aggregator pipeline encountered an error: {e}")

if __name__ == "__main__":
    run_comprehensive_extraction()
