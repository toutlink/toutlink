# Chapter 13 – Server-Side Request Forgery (SSRF)

## Mental Model

Application makes HTTP (or other protocol) requests on your behalf to a URL you control.  
If you control the target, you can pivot:

- From internet → internal network
- From web tier → metadata services / admin panels

## High-Value Features

- “Fetch URL” / “Import from URL”:
  - Screenshot, PDF generator, link preview
  - RSS imports, webhook testers
- File upload via URL (instead of local file)
- Webhooks where you can choose the destination URL

## Recon Checklist

- Parameters with URLs:
  - `url`, `target`, `endpoint`, `callback`, `webhook`, `feed`
- JSON keys that look like URLs
- Hint headers:
  - `User-Agent` with internal product name
  - `X-Forwarded-For` echoes

## Exploitation Basics

1. **Prove outbound HTTP**
   - Point the URL to your own server (Burp Collaborator, Interactsh, or your VPS).
   - Confirm the server made a request.

2. **Probe internal IPs**
   - `http://127.0.0.1:80`
   - `http://localhost:8080`
   - `http://169.254.169.254/latest/meta-data/` (cloud metadata)
   - `http://10.x.x.x`, `http://172.16.x.x`, `http://192.168.x.x`

3. **Read internal-only content (if responses are reflected)**
   - Admin panels
   - Stats endpoints (`/metrics`, `/health`, `/debug`)

4. **Blind SSRF**
   - If you don’t see the response, use:
     - DNS-based exfil (different subdomains per path)
     - Timing-based tricks (slow endpoints vs fast)

## Defense Bypasses to Try

- Schemes:
  - `http://`, `https://`, `gopher://`, `file://` (depending on tech)
- Encodings:
  - Decimal IP: `http://2130706433/`
  - Octal, hex, mixed encodings
  - `http://127.0.0.1@evil.com/` style tricks
- Use redirects:
  - Point to your domain that redirects to internal IP

## Automation Ideas

- Build a small SSRF probe list:
  - Internal IPs
  - Metadata URLs for AWS, GCP, Azure
- Script that:
  - Cycles through URLs
  - Compares response codes/lengths
  - Logs hits for manual follow-up

## Reporting Tips

- Show:
  - Parameter and endpoint used
  - Proof of internal access (headers, internal hostnames)
- If you hit metadata service:
  - Mask secrets but show that you could retrieve them.
- Impact:
  - Pivot to internal network
  - Credential theft from metadata
  - Access to admin panels

- Recommend:
  - Allowlist-only outbound destinations
  - No raw URL control by users
  - Network-level egress filtering
