# Chapter 14 – Insecure Deserialization

## Mental Model

Server takes untrusted data and **deserializes** it into objects.  
If the format supports arbitrary object graphs, you may get:

- Remote code execution
- Authentication / authorization bypass
- Data tampering

Common formats:

- Java: serialized objects, `JSession`-like cookies
- PHP: `serialize()` / `unserialize()` in cookies or hidden fields
- .NET: `ViewState` (older setups)
- JWT-like custom tokens with base64’d objects

## Recon Checklist

- Cookies / parameters that are:
  - Base64 blobs
  - Long ASCII strings with `O:`, `a:`, `s:` (PHP)
  - Binary blobs starting with known magic bytes
- Hidden fields containing encoded user data
- Framework hints:
  - Spring / Java stack
  - Old PHP apps
  - Legacy .NET

## Practical Testing

1. **Identify serialization format**
   - Base64 decode and inspect.
   - Look for:
     - `O:8:"stdClass"` (PHP)
     - `ac ed 00 05` magic bytes (Java)
   - Libraries like `phpggc`, `ysoserial`, `ysoserial.net`.

2. **Safe tampering first**
   - Change benign fields:
     - `role` from `user` to `admin`
     - `is_premium` from `false` to `true`
   - Re-encode and send back.

3. **Look for gadget chains (only when allowed!)**
   - Match the stack with gadget libraries:
     - e.g., Java + Spring = check ysoserial payloads.
   - Many bounty programs don’t allow full RCE; focus on **proof** of code execution (e.g., DNS callback).

## Automation Ideas

- Build a small script that:
  - Extracts suspected serialized values
  - Decodes and prints them for quick inspection
- For PHP:
  - Use `phpggc` to generate test payloads in a controlled lab environment before touching real targets.

## Reporting Tips

- Clearly describe:
  - Where the serialized data is stored (cookie, param, hidden field)
  - What you could change (role escalation, flags)
- Evidence:
  - Before/after screenshots
  - Example modified payload (sanitized)
- Impact:
  - Auth bypass
  - Potential RCE if gadget chain exploited
- Remediation:
  - Avoid unserializing untrusted data
  - Use safer formats (JSON) and explicit validation
  - Sign / MAC any tokens that must be trusted
