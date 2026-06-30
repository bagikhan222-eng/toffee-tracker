import requests

# 1. Your stream URL and headers as before
stream_url = "# Swap the unresolvable 'prod-cdn01-live' host with the public web CDN host
stream_url = "https://bldcmprod-cdn.toffeelive.com/live/FIFA-2026-6/index.m3u8?edge-cache-token=Expires=1782802409~Starts=1782802109~URLPrefix=aHR0cHM6Ly9wcm9kLWNkbjAxLWxpdmUudG9mZmVlbGl2ZS5jb20~Signature=uQn5bEgN5NLSyoIOpfwn58A5pGVW9ZtR3cy93jKtGz03LlvFVh52HfHHXvbvdWcs0_CuDWv4ohvphQ5fKa9SDg"
headers = {
    "User-Agent": "Mozilla/5.0 ...",
    "Origin": "https://toffeelive.com"
}

# 2. Add a Bangladeshi Residential/Datacenter Proxy 
# Format: http://username:password@proxy_ip:port
proxies = {
    "http": "http://your_bd_proxy_ip:port",
    "https": "http://your_bd_proxy_ip:port" 
}

try:
    # 3. Pass the proxies parameter into your requests call
    response = requests.get(stream_url, headers=headers, proxies=proxies, timeout=10)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print(f"Connection failed: Ensure your proxy is active and located inside BD.")
