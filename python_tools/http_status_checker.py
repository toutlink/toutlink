#!/usr/bin/env python3

import sys
import requests

def check_url(url: str) -> None:
    try:
        response = requests.get(url, timeout=10)
        print(f"[+] {url} -> {response.status_code}")
        print("[i] Security-relevant headers:")
        for header in ["Server", "X-Powered-By", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Strict-Transport-Security"]:
            if header in response.headers:
                print(f"    {header}: {response.headers[header]}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error requesting {url}: {e}")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <url1> [url2] ...")
        sys.exit(1)
    for url in sys.argv[1:]:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        check_url(url)

if __name__ == "__main__":
    main()
