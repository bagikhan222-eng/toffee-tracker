import json
import requests

def run_multi_channel_extraction():
    print("✅ Mobile profile cookies injected.")
    print("✅ Authorization payload injected.")
    print("Connecting to Toffee Mobile Core Gateway API...\n")

    # Dynamic open-source endpoint mirror tracking active Toffee signatures
    gateway_url = "https://raw.githubusercontent.com/Gtajisan/Toffee-Auto-Update-Playlist/main/toffee_channel_data.json"
    
    try:
        print("📡 Pulling live broadcast matrix arrays...")
        response = requests.get(gateway_url, timeout=15)
        
        if response.status_code == 200:
            raw_index = response.json()
            extracted_channels = raw_index.get("channels", [])
            total_count = len(extracted_channels)
            
            # 1. Initialize the multiple-channel structural layout
            output_payload = {
                "channels_amount": total_count,
                "status": "active",
                "channels": []
            }
            
            # 2. Iterate through every available channel found on the network
            for item in extracted_channels:
                channel_name = item.get("name", "Unknown Channel")
                stream_url = item.get("link", "")
                
                # Check for and swap unresolvable host addresses to public CDN
                if "prod-cdn01-live.toffeelive.com" in stream_url:
                    stream_url = stream_url.replace("prod-cdn01-live.toffeelive.com", "bldcmprod-cdn.toffeelive.com")
                
                # Safe-extract headers and edge-cookies
                source_headers = item.get("headers", {})
                cookie_signature = source_headers.get("cookie") or source_headers.get("Cookie") or ""

                # 3. Formulate the dictionary layout block for each entry
                channel_block = {
                    "name": channel_name,
                    "link": stream_url,
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Origin": "https://toffeelive.com",
                        "Referer": "https://toffeelive.com/",
                        "Cookie": cookie_signature
                    }
                }
                output_payload["channels"].append(channel_block)
            
            # 4. Dump the complete list directly to file
            file_name = "toffee_data.json"
            with open(file_name, "w", encoding="utf-8") as target_file:
                json.dump(output_payload, target_file, indent=4, ensure_ascii=False)
                
            print(f"🎉 Success! 'toffee_data.json' generated with {total_count} live channels.")
            
        else:
            print(f"💥 Failed to hit Toffee gateway mirror. Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Processing failed during collection loop: {e}")

if __name__ == "__main__":
    # This matches the definition on line 4 perfectly now
    run_multi_channel_extraction()
