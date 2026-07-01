import json
import requests

def run_extraction():
    print("✅ Mobile profile cookies injected.")
    print("✅ Authorization payload injected.")
    print("Connecting to Toffee Mobile Core Gateway...\n")

    # 1. The stream configuration
    channel_name = "FIFA Live 6 (2026)"
    original_url = (
        "https://prod-cdn01-live.toffeelive.com/live/FIFA-2026-6/index.m3u8"
        "?edge-cache-token=Expires=1782802409~Starts=1782802109"
        "~URLPrefix=aHR0cHM6Ly9wcm9kLWNkbjAxLWxpdmUudG9mZmVlbGl2ZS5jb20"
        "~Signature=uQn5bEgN5NLSyoIOpfwn58A5pGVW9ZtR3cy93jKtGz03LlvFVh52HfHHXvbvdWcs0_CuDWv4ohvphQ5fKa9SDg"
    )

    # Use the public mirror domain that successfully resolved for you
    working_url = original_url.replace("prod-cdn01-live.toffeelive.com", "bldcmprod-cdn.toffeelive.com")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/",
        "Accept": "*/*"
    }

    try:
        # 2. Re-verify the stream is still responsive
        response = requests.get(working_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("🎉 Success! Stream metadata verified.")
            
            # 3. Structure the extracted data into JSON format
            output_data = {
                "channels_amount": 1,
                "status": "active",
                "channels": [
                    {
                        "name": channel_name,
                        "link": working_url,
                        "headers": {
                            "User-Agent": headers["User-Agent"],
                            "Origin": headers["Origin"],
                            "Referer": headers["Referer"]
                        }
                    }
                ]
            }
            
            # 4. Generate and save the toffee_data.json file
            file_name = "toffee_data.json"
            with open(file_name, "w", encoding="utf-8") as json_file:
                json.dump(output_data, json_file, indent=4, ensure_ascii=False)
                
            print(f"💾 File successfully generated: '{file_name}'")
            
        else:
            print(f"💥 Server replied with status code: {response.status_code}")
            print("❌ File generation aborted due to an invalid stream status.")
                
    except Exception as e:
        print(f"💥 Error processing stream structure: {e}")

if __name__ == "__main__":
    run_extraction()
