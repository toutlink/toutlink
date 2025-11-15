# Chapter 20 – API Security & Common API Attack Paths

## Mental Model
APIs expose raw backend functionality directly to clients.  
They often skip UI-based restrictions, rely too much on client honesty, and reveal internal logic.

As a result, APIs are the **highest-value attack surface** in modern web applications.

---

## API Taxonomy
Understanding API types helps target flaws:

### 1. REST APIs
- JSON input/output  
- Stateless  
- Most common architecture  

### 2. GraphQL APIs
- Single endpoint  
- Arbitrary queries  
- Over-fetching and under-fetching risks  

### 3. Mobile APIs
- Often weaker security  
- Hidden parameters  
- Bypass of web constraints  

### 4. Internal/Unpublished APIs
- Exposed via:
  - JavaScript files  
  - Mobile apps  
  - Browser dev tools  
- Usually less hardened  

---

## Common API Vulnerabilities

### 1. BOLA / IDOR (Broken Object Level Authorization)
#1 most critical API vulnerability.

Occurs when attacker can access others’ data by modifying IDs:

/api/user/123/profile
/api/user/124/profile

If 124 works → vulnerability.

Test with:
- Numerically similar IDs  
- UUIDs  
- Email-based identifiers  
- Relationship IDs (invoice_id, subscription_id, etc.)

---

### 2. Broken Authentication
Weak authentication for APIs:

- No rate limiting  
- Basic auth without CSRF protection  
- Token not tied to user or device  
- Reusable refresh tokens  
- Long-lived session tokens  

Test:
- Replay old access tokens  
- Try refresh tokens multiple times  
- Try login endpoints via mobile API

---

### 3. Mass Assignment
APIs accept **more fields** than intended.

Example:
```json
{
  "email": "user@example.com",
  "is_admin": true
}
Fix: backend must whitelist, not blacklist.

Test:

Add new fields

Mirror database column names

Add dangerous flags: role, privileges, balance, id
4. Excessive Data Exposure

APIs often return too much information.

Examples:

Internal IDs

Admin flags

Password hashes

Internal comments

Debug metadata

Test:
Inspect API responses deeply – nested JSON may hide sensitive values.

5. Improper Rate Limiting

Applies to:

Login

OTP endpoints

File uploads

Search endpoints

Password reset email triggers

Test:
Send 20–100 requests:

If no throttle → vulnerable

6. Weak Input Validation

APIs may trust client inputs too much:

SQL injection

SSTI

LDAP injection

Path traversal

File upload bypasses

Test payloads:

' OR '1'='1

{{7*7}}

../../etc/passwd

XML payloads for XXE

File-type spoofing

7. Business Logic Failures

Same logic issues as web, but easier to exploit in raw API form:

Money transfers

Coupon redemption

Subscription upgrades

Workflow skipping

Test:
Submit steps out of order or directly call internal endpoints.

8. GraphQL-Specific Attacks

Introspection enabled

Deep recursion queries

Query batching (denial of service)

Missing access checks in field resolvers

Payload:

query { __schema { types { name } } }

If introspection enabled in production → high risk.

High-Value Attack Patterns
1. Find Hidden Endpoints

Look in:

/static/js/*.js

Mobile APKs

Swagger/OpenAPI docs

/api/v1/ → try /api/v2/, /admin/, /internal/

2. Token Misuse

Test:

Using one user’s token on another user’s resource

Using expired tokens

Using refresh tokens multiple times

Using tokens without verifying audience/client_id

3. Replaying Old Sessions

Replay:

Old JWTs

Old cookies

Old OAuth tokens

If accepted → vulnerability.

Automation Ideas

Build an API spider from JavaScript files

Enumerate endpoints via wordlists (api, v1, v2, internal)

Test every endpoint for BOLA automatically

Write scripts to mutate JSON bodies with hidden fields

Rate-limit scanners for user enumeration, OTP guessing

GraphQL introspection scanners

Reporting Tips

Include:

Endpoint names

Full request/response samples

Impact in data exposure or privilege escalation

Clear reproduction steps

How the vulnerability could be chained with others

Remediation

Enforce object-level authorization everywhere

Implement strict allowlists for JSON fields

Add global and per-user rate limiting

Disable GraphQL introspection in production

Validate all inputs server-side

Short-lived tokens with rotation
