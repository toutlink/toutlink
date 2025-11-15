# Chapter 19 – Two-Factor Authentication (2FA) Bypass Attacks

## Mental Model
2FA is intended to prevent login even if an attacker has the password.  
A 2FA bypass means:  
**You authenticate WITHOUT ever providing the second factor.**

Attackers target weaknesses in:
- Session state
- Step ordering
- Token validation
- Alternate login flows
- Device trust features
- Backup code systems

---

## 1. Login Flow Skip Attacks
Many apps enforce 2FA only on **the intended login endpoint**.

Attackers can bypass by:
- Using an alternate login path
- Using mobile API endpoints
- Logging in via OAuth or SSO
- Using legacy authentication flows

**Tests:**
- Attempt login via `/api/login`
- Attempt login via `/mobile/auth`
- Try SSO login without 2FA requirement
- Replay the pre-2FA session cookie

If the session becomes authenticated before 2FA → vulnerability.

---

## 2. Session Misbinding (The #1 2FA Bug)
Flow should be:

1. Login with password  
2. Mark session as **2FA_PENDING**  
3. After OTP success → session becomes **AUTHENTICATED**

If a site incorrectly does:

1. Login with password  
2. Immediately sets full session  
3. Shows 2FA page “for show”

You can skip 2FA entirely.

**Test:**
Capture session cookie **before** confirming 2FA.  
Reuse it on another browser.

If it logs you in → critical bypass.

---

## 3. Missing “2FA Required” Check on Sensitive Endpoints
Some apps enforce 2FA at login, but NOT on:
- Password change  
- Email change  
- Payment actions  
- Account deletion  
- API tokens creation  

Attackers simply log in (with password only) and skip 2FA by attacking other endpoints.

---

## 4. OTP Reuse  
Each OTP should be single-use.

**Test:**
1. Request OTP  
2. Use OTP  
3. Try same OTP again  

If it works twice → vulnerability.

---

## 5. OTP Guessing / Bruteforce
Most OTP codes are 6 digits = 1,000,000 possibilities.

If site has:
- No rate limiting  
- No lockouts  
- Unlimited attempts  

→ Easily brute-forced.

**Bonus test:**  
Try sending the same code many times to see if server handles duplicates correctly.

---

## 6. Backup Codes Abuse
Backup codes allow login *without phone/email*.

Common vulnerabilities:
- Unlimited use  
- Non-random codes  
- Weak format (4 digits, words, etc.)  
- Code not invalidated after use  
- Visible unmasked in user profile

---

## 7. Trusted Device / Remember Me Bypass
2FA is often skipped on “trusted devices”.

Weaknesses include:
- Token stored in cookies without binding  
- Token guessable or reusable  
- Token not tied to IP, browser, or device fingerprint  
- Long-lived trust (months or years)

**Test:**
Copy trusted device cookie to a new browser.  
If it bypasses 2FA → vulnerable.

---

## 8. Account Recovery Flaws
Account recovery flows often **skip 2FA entirely**.

Check:
- Password reset via email (no 2FA check)
- Recovery questions (weak)
- Changing phone number without old number verification

If attacker takes over recovery, they bypass 2FA by design.

---

## High-Value Targets
- Banking  
- Crypto exchanges  
- Corporate SaaS (Slack, GitHub, Atlassian)  
- Healthcare portals  
- Government systems  
- Business email platforms  

These systems rely strongly on 2FA for real-world protection.

---

## Automation Ideas
- Scrape login flow to identify alternate endpoints  
- Build OTP replay scripts  
- Analyze session cookies automatically for pre-2FA access  
- Fuzz trusted-device cookie values  
- Enumerate API versions (v1, v2, mobile endpoints)

---

## Reporting Tips
Include:
- Full login flow description  
- Proof-of-bypass (video or screenshots)  
- Exact vulnerable endpoints  
- Impact (complete account takeover)  
- Recommendations tailored to their implementation

---

## Remediation
- Enforce server-side **2FA_REQUIRED** state  
- Block access to all sensitive endpoints until 2FA is passed  
- Single-use OTPs  
- Strong rate limiting  
- Bind trusted devices to:
  - User
  - Browser fingerprint  
  - IP patterns  
- Require full re-authentication for:
  - Email change  
  - Password change  
  - 2FA reset  

---
