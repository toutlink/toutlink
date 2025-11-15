# Chapter 32 – JWT & Modern Token Attacks  
Algorithm Confusion • KID Injection • JWK Manipulation • Key Substitution • Token Forgery

---

# Why JWT Attacks Matter
Most modern apps use JWT for:
- Authentication
- SSO sessions
- API tokens
- Mobile app auth
- OAuth authorization

A single JWT flaw = **full account takeover**, often **Critical** severity.

This is an elite category very few hunters truly master.

---

# JWT Core Structure
A JWT has 3 parts:

header.payload.signature

makefile
Copy code

Example:

eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.hYBn...

yaml
Copy code

---

# 1. Algorithm Confusion Attacks

## Case A: “alg”: “none” Attack
Old vulnerability but still appears in bad implementations.

JWT:

```json
{"alg": "none"}
If the server accepts unsigned tokens → instant admin.

Payload example:

json
Copy code
{"user": "admin"}
Case B: RS256 → HS256 Confusion
Server mixes asymmetric & symmetric signing.

If backend mistakenly treats public RSA key as an HMAC secret, you can forge tokens.

Steps:
Export server’s public key

Use it as the HMAC secret

Sign your forged JWT with HS256

Become admin

Tools:
jwt_tool

jwt-cracker

custom python signing

Impact:

Full account takeover

Bypass 2FA

API admin access

2. KID Header Injection
Many backends use the kid (Key ID) header to choose the signing key.

Example header:

json
Copy code
{
  "alg": "HS256",
  "kid": "main"
}
Attack A: Path Traversal
Set:

json
Copy code
"kid": "../../../../../../dev/null"
Or:

json
Copy code
"kid": "../../../../../../etc/passwd"
If backend tries to read the file → signature bypass possible depending on behavior.

Attack B: SQL Injection via KID
json
Copy code
"kid": "main' OR '1'='1"
If backend builds SQL-based key lookup:

sql
Copy code
SELECT secret FROM keys WHERE id = '$kid';
You obtain ANY key → forge ANY token.

Attack C: NoSQL Injection
MongoDB example:

kotlin
Copy code
"kid": {"$ne": null}
Backend finds the first key in DB.

3. JWK Manipulation Attacks (Modern + Critical)
Some apps allow passing a JWK Set URL (jku) or inline JWK (jwk) as part of the header.

Example vulnerable header:

json
Copy code
{
  "alg": "RS256",
  "jku": "https://attacker.com/jwks.json"
}
If server fetches your JWK file → you provide the signing keys.

Steps:
Host malicious JWK JSON file

Generate your own key pair

Publish public key in JWK format

Forge a JWT signed with your private key

Server verifies using your attacker-controlled JWK

Become admin

Impact:

Critical severity

Multi-user account takeover

SSO bypass

4. JWK Key Confusion Attack (2022–2024)
You provide a JWK that looks like an RSA key:

json
Copy code
{
  "kty": "RSA",
  "kid": "evil",
  "n": "base64...",
  "e": "AQAB",
  "alg": "HS256",
  "k": "secret-value-here"
}
But contains both:

RSA fields (n, e)

Symmetric key (k)

Some JWT libraries get confused:

Think it's RSA

But treat it as HMAC
→ Signature bypass

Forging tokens is trivial.

5. Public JWK Injection Logic Flaws
If a server chooses the key using weak logic:

Examples:

Picks the first JWK in the set

Picks JWK with null fields

Accepts JWKs with use="sig" but no actual key

Accepts JWK with empty "n"

You can:

Override keys

Force default code paths

Skip signature verification

6. Key Substitution Attacks
If the backend uses:

Multiple tenant keys

Multiple issuer keys

Multiple OAuth providers

Then key mixups occur.

Example:
You take Google’s public JWKS and feed it to the app.

App mistakenly validates your token using Google’s key.

Impact:

Log in as ANY Google account

Often gain admin panels or SAML-like privileges

7. Weak Signing Keys
Common issues:

Weak HMAC secrets (secret, password)

32-bit or 64-bit keys

Keys leaked in GitHub

Hardcoded secrets inside JS bundles

Test:

swift
Copy code
jwtcrack -t <token> -d /usr/share/wordlists/rockyou.txt
Or custom HMAC brute force.

8. Expired Token Resurrecting
Misconfigured backends may:

Not validate exp

Validate only nbf

Ignore iat

Allow refresh using old tokens

Attack:

Capture expired admin token

Resend with crafted headers

Backend misinterprets → admin restored

9. Incorrect Audience / Issuer Validation
Common flaws:

aud wildcard

Missing iss validation

Multiple issuers allowed

Accepts tokens issued for different apps

Impact:

Cross-app authentication

Using OAuth tokens from another environment

Confused deputy attacks

High-Value Targets
Critical endpoints:

/auth/refresh

/token/refresh

/api/auth/me

/api/admin/*

OAuth callback endpoints

Mobile app API endpoints

Token storage locations to check:

Local storage

Session storage

Cookies

Authorization headers

Automation Ideas
Create JWT fuzzer that:

Mutates kid

Modifies alg

Inserts malicious JWK

Inserts jku pointing to your server

Removes signature

Swaps algorithms RS256 ↔ HS256

Adds extra fields (padding confusion)

Build JWT brute-forcing tools:

Wordlist-based HMAC cracking

Key-length tester

Substitution generator

Reporting Tips
Show:

Original token

Modified malicious token

Server response difference

Why validation is bypassed

Documentation proving expected behavior

Screenshots of impact

Tools used

Steps to reproduce

Severity justification

Remediation
Enforce strict algorithm allowlist

Disallow jku, jwk, external JWKS

Validate kid

Validate iss and aud strictly

Use strong HMAC secrets

Enforce token expiration on backend

Do not mix RSA and HMAC key logic

Rotate signing keys

Disable dynamic key loading

Summary
JWT attacks are one of the most profitable bug classes in modern bug bounty hunting.

Master:

JWA confusion

KID traversal

JWK remote loading

JWK manipulation

Key substitution

Token forgery

