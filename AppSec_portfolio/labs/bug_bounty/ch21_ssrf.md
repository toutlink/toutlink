# Chapter 21 – Server-Side Request Forgery (SSRF) & Internal Network Pivoting

## Mental Model
SSRF happens when an application fetches a URL or resource **on behalf of the user**.

If you can control that URL → you can make the server:
- Reach internal networks  
- Hit metadata services  
- Access internal admin panels  
- Trigger internal-only APIs  
- Bypass firewalls  
- Download files  
- Leak credentials  

SSRF is one of the highest-impact vulnerabilities in modern cloud environments.

---

## Where SSRF Appears
Common triggers:
1. **Image upload → “fetch URL” function**
2. **PDF/Document generator**
3. **Webhook systems**
4. **URL preview (Slack-like link unfurling)**
5. **SSO/OAuth callback URLs**
6. **Import-from-URL functions**
7. **Server-to-server integrations**

If the app retrieves something from a URL you control → test SSRF.

---

## Core SSRF Payloads

### 1. Internal Network Enumeration
http://127.0.0.1

http://localhost

http://::1
http://[::1]

Test variations:
127.0.0.1:22
localhost:8080
http://169.254.169.254/latest/meta-data/

---

### 2. Cloud Metadata Endpoints (Critical)
AWS:

http://169.254.169.254/latest/meta-data/

GCP:

http://metadata.google.internal/

Azure:

http://169.254.169.254/metadata/instance?api-version=2021-02-01

If server responds → severe impact (credential leak).

---

### 3. Protocol Smuggling
Try non-HTTP protocols disguised as HTTP:

http://127.0.0.1:3306/

http://127.0.0.1:6379/

If the server attempts to connect → port alive.

---

### 4. DNS Rebinding Payloads
Use attacker-controlled DNS domain:

http://yourdomain.com

You change DNS A-record → internal IP.

---

## Blind SSRF Detection
If you don't get a direct response but suspect SSRF, use:

- Burp Collaborator  
- interact.sh  
- DNS logging server  

Indicator of SSRF:
- DNS lookup from victim  
- HTTP request from victim  
- Any traffic to your server  

---

## High-Value SSRF Targets

### 1. Cloud Metadata
Because it leads to:
- AWS access keys  
- GCP service tokens  
- Instance identity  
→ You can pivot into full cloud takeover.

### 2. Internal Admin Panels
Examples:
- `http://127.0.0.1/admin`
- `http://localhost:8080/dashboard`
- `http://internal-service/`
- Kubernetes APIs (common)

### 3. File Protocol Abuse (where enabled)
file:///etc/passwd
file:///var/www/private/config.yml

### 4. Redis / Memcached
Possible RCE via SSRF if protocols exposed.

---

## SSRF + Other Vulnerabilities = Critical Chain

### SSRF + RCE
Hit internal services that accept commands.

### SSRF + IDOR
Internal admin APIs → modify other user data.

### SSRF + Credential Exposure
Pull cloud credentials → pivot deeper.

### SSRF + File Read
If file:// allowed → direct data leak.

---

## Testing Strategy

### Step 1 — Check for URL Fetching Features
Common parameters:

?url=
?target=
?fetch=
?img=
?resource=
?import=

### Step 2 — Test Localhost Access

http://127.0.0.1

### Step 3 — Probe Local Ports
http://127.0.0.1:22

http://127.0.0.1:6379

### Step 4 — Try Cloud Metadata
Check for timeouts, redirects, errors.

### Step 5 — Blind SSRF
Use DNS logging services.

### Step 6 — Pivot
Enumerate:
- `http://internal-service/`
- `http://host.docker.internal`
- Service discovery endpoints

---

## Automation Ideas
- Build a local SSRF test list (~200 payloads)  
- Script for cloud metadata probing  
- DNS rebinding scripts  
- Port scanning via SSRF (semi-automated)  
- Use Turbo Intruder for mass endpoint probing  

---

## Reporting Tips
Include:
- Triggering endpoint  
- Payload used  
- Response received  
- Internal service accessed  
- Whether metadata was retrievable  
- Business impact (admin access, credential leak)

---

## Remediation
- Enforce strict allowlists for outbound requests  
- Block internal IP ranges:  
  - `127.0.0.0/8`  
  - `10.0.0.0/8`  
  - `169.254.0.0/16`  
- Use SSRF-safe URL parsers  
- Disable file:// and gopher:// schemes  
- Add network-level egress filters  
- Require authentication for metadata endpoints  

