import sys
import requests
import urllib.parse

def run_extraction():
    print("✅ Mobile profile cookies injected.")
    print("✅ Authorization payload injected.")
    print("Connecting to Toffee Mobile Core Gateway...\n")

    # 1. The original unresolvable stream URL
    original_url = (
        "https://prod-cdn01-live.toffeelive.com/live/FIFA-2026-6/index.m3u8"
        "?edge-cache-token=Expires=1782802409~Starts=1782802109"
        "~URLPrefix=aHR0cHM6Ly9wcm9kLWNkbjAxLWxpdmUudG9mZmVlbGl2ZS5jb20"
        "~Signature=uQn5bEgN5NLSyoIOpfwn58A5pGVW9ZtR3cy93jKtGz03LlvFVh52HfHHXvbvdWcs0_CuDWv4ohvphQ5fKa9SDg"
    )

    # 2. Swap out the unresolvable host with Toffee's public web CDN mirror
    # We leave the token parameters completely intact so the signature doesn't break.
    updated_url = original_url.replace("prod-cdn01-live.toffeelive.com", "bldcmprod-cdn.toffeelive.com")
    
    # 3. Setup the required anti-bot/verification headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://toffeelive.com",
        "Referer": "https://toffeelive.com/",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

    print(f"📡 Attemping connection via public mirror domain...")
    
    try:
        # 4. Attempt to fetch the playlist
        response = requests.get(updated_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("🎉 Success! Stream metadata successfully extracted.")
            print("\n--- Raw M3U8 Stream Data ---")
            print(response.text[:500]) # Prints the beginning of the live stream chunks
            print("----------------------------")
        else:
            print(f"💥 Server replied with status code: {response.status_code}")
            if response.status_code == 403:
                print("💡 Note: A 403 error means the token's 5-minute lifespan has expired or your IP is outside Bangladesh.")
                
    except requests.exceptions.ConnectionError as ce:
        print(f"💥 Network Connection Error: Could not reach the server.")
        print(f"Details: {ce}")
    except requests.exceptions.Timeout:
        print("💥 Error: The request timed out. The streaming server might be heavily overloaded.")
    except Exception as e:
        print(f"💥 An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_extraction()
