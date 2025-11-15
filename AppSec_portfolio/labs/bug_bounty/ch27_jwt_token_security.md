# Chapter 27 – JWT, Token-Based Authentication & Token Abuse

## Mental Model
Modern applications rely heavily on token-based authentication:
- JWT (JSON Web Tokens)
- OAuth access tokens
- Refresh tokens
- Mobile API tokens
- Session tokens stored in localStorage or cookies

If token generation or validation is flawed, the attacker gains:
- Account takeover
- Privilege escalation
- Admin access
- Permanent login without password
- Access to internal APIs

---

# How JWT Works (Crash Course)
A JWT contains:

**Header**  
{
"alg": "HS256",
"typ": "JWT"
}


**Payload**  


{
"sub": "user123",
"role": "user"
}


**Signature**  


HMACSHA256(base64(header)+base64(payload), secret)


If attacker can tamper with *any* of this, the entire system breaks.

---

# Major JWT Vulnerability Classes

## 1. **`alg: none` Attack (Classic But Still Found)**
If server accepts:


{
"alg": "none"
}

The signature is ignored.

Attacker can forge admin token:


{
"sub": "attacker",
"role": "admin",
"alg": "none"
}


Impact: full admin takeover.

---

## 2. **Weak Secret Key (Brute Force)**
If server uses:


HS256 + weak secret

Examples:
- `secret`
- `password`
- `123456`
- `jwtsecret`

Tools:
- `jwt-cracker`
- `hashcat`
- `jwt_tool`

Impact: total compromise.

---

## 3. **HS256/RS256 Confusion Attack**
If server accepts both:
- HMAC (symmetric)
- RSA (asymmetric)

Attacker switches alg:

### Original (RS256)


"alg": "RS256"


### Attacker:


"alg": "HS256"


Then uses the PUBLIC KEY as the SECRET.

Critical misconfiguration → full token forgery.

---

## 4. **Privilege Escalation by Modifying Claims**
Payload tampering examples:
- `role`: `"user"` → `"admin"`
- `plan`: `"free"` → `"enterprise"`
- `is_staff`: `false` → `true`
- `permissions`: `[]` → `["admin.read", "admin.write"]`

If server fails to re-check authorization **server-side**, attacker escalates privileges.

---

## 5. **Replay Attacks**
Tokens reused:
- Across sessions  
- Across devices  
- Across account resets  

If old tokens stay valid → account takeover.

---

## 6. **Refresh Token Abuse**
If refresh tokens:
- Have no expiration  
- Are never invalidated  
- Are leaked via XSS  
- Are sent over HTTP (not HTTPS)

Attacker gains *permanent* access.

---

## 7. **JWT Stored in localStorage (XSS = Instant ATO)**
If app uses:


localStorage.setItem("token", <JWT>)


Then **any XSS = full account takeover**.

Safer: Use **HttpOnly** cookies.

---

## 8. **Broken Blacklist / Logout**
If logout doesn’t invalidate tokens:
- Attacker keeps using stolen token forever  
- Refresh token keeps generating new access tokens  

---

# High-Value Attack Techniques

## 1. Decode Every JWT
Use:
- jwt.io  
- jwt-tool  
- Burp Decoder  
- Python `jwt` module  

Look for:
- `admin: true`
- `roles`
- `permissions`
- `tier`
- `is_staff`
- `is_admin`

---

## 2. Try Algorithm Switching
Modify:


"alg": "none"

or switch:


RS256 → HS256


Replay token.

---

## 3. Brute Force Weak Secrets
Run:


hashcat -m 16500 jwt.txt wordlist.txt


---

## 4. Attempt Claim Escalation
Modify payload:


{"role":"admin"}


If server doesn’t validate on backend → instant admin.

---

## 5. Replay Old Tokens
Test:
- Old refresh tokens  
- Old password reset tokens  
- Tokens from another session  

If valid → major security flaw.

---

## 6. Steal Tokens via CSP Bypass
If app uses localStorage, test for:
- DOM XSS  
- Prototype pollution  
- Angular/React template injection  

Stored XSS = permanent account takeover.

---

# Real Attack Examples (Generalized)

### 1. Change role from user → admin  
Many startups forget to validate user roles server-side.

### 2. Use expired token but server doesn’t check  
Bypass expiration and maintain access.

### 3. Hijack refresh token → permanent takeover  
App never invalidates refresh tokens → infinite attack window.

### 4. RSA/HS confusion → forge any user  
This vulnerability has earned multiple $5,000–$20,000 bounties.

### 5. Steal JWT via XSS → instant takeover  
Because token stored in localStorage.

---

# High-Value Targets for Token Abuse
Look for JWT in:
- Authorization headers  
- Session cookies  
- Mobile APIs  
- WebSockets  
- SSO flows  
- Refresh endpoints  
- GraphQL endpoints  
- Admin portals  

---

# Automation Ideas
- JWT brute-force panel  
- Token replay tool  
- Automated claim modification  
- Detection of weak secrets  
- Check for JWT in JS source code  

---

# Reporting Tips
Include:
- Raw JWT decoded  
- Modified payload  
- Proof of successful token tampering  
- Account takeover demonstration  
- Security model impact (auth bypass, privilege escalation)  

---

# Remediation
- Use strong secrets (32+ chars, random)  
- Enforce RS256 or ES256, not HS256  
- Never allow `alg: none`  
- Validate all claims server-side  
- Short access token expiry (5–15 minutes)  
- Rotate and invalidate refresh tokens  
- Store tokens in HttpOnly cookies  
- Use strict authorization checks  
