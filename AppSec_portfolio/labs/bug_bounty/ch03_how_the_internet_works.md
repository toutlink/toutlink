# Chapter 3 — How the Internet Works (Elite Notes)

## Mental Models

### Request Life Cycle
1. DNS resolution
2. TCP handshake
3. TLS handshake
4. HTTP request
5. Server processing
6. Response

### Where Bugs Live
- DNS → Subdomain takeover
- TLS → Misconfigurations
- HTTP → XSS, SQLi, SSTI, IDOR
- Cookies → session flaws
- Caching → cache poisoning
- Load balancer → header attacks

## Browser Security
- Same-Origin Policy
- CORS misconfigurations
- Cookie flags: HttpOnly, Secure, SameSite

## Tools to Understand It Better
- curl, httpie
- Burp Suite
- Browser DevTools
- Wireshark
- dig / nslookup
