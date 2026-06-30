import requests

# 1. Your stream URL and headers as before
stream_url = "https://prod-cdn01-live.toffeelive.com/live/FIFA-2026-6/0/master_200020260630064802680.ts?hdntl=Expires=1782888509~_GO=Generated~URLPrefix=aHR0cHM6Ly9wcm9kLWNkbjAxLWxpdmUudG9mZmVlbGl2ZS5jb20~Signature=AeQsclCl2-P1zk3AMSNJM0ohZS5YkPhrL_AvwzHFYqqXmuscDRI7rSWV0ICkspY2a9gWivDkaxuZBKng6IfjbBweiEUE"
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
