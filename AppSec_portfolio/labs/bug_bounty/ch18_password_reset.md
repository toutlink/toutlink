# Chapter 18 – Password Reset & Account Recovery Attacks

## Mental Model
Password reset flows are extremely sensitive because they allow access **without a password**.  
If any step is weak or misvalidated, attackers can take over accounts.

This chapter focuses on identifying flaws in:
- Token generation  
- Token verification  
- Identity verification  
- Cross-user resets  
- Reset flow logic

---

## Core Components of a Secure Reset Flow
A proper password reset must enforce:

1. **Correct user identity**  
2. **Unique, unpredictable reset token**  
3. **Token bound to specific user**  
4. **Single-use and short expiration**  
5. **Strict validation at each step**

Break any of these → account takeover.

---

## Common Vulnerabilities

### 1. User Enumeration
Attackers discover which emails/phones exist.

Examples:
- “User not found” vs “Reset link sent!”
- Different status codes
- Different response times

**Test:**
Try valid vs invalid emails and compare responses.

---

### 2. Token Leaks in Logs or URLs
Tokens should never appear in:
- Referrer headers  
- Redirect URLs  
- JavaScript console logs  
- Analytics beacons  
- Customer support logs  

**Test:**
Check browser network tab for token exposure.

---

### 3. Predictable or Weak Tokens
Bad examples:
- Base64(email)  
- Simple UUID without randomness  
- Incrementing tokens  

**Test:**
Reset multiple times and compare token patterns.

---

### 4. Token Not Bound to User
If the system checks only token validity but not which user it belongs to:

**Impact:**  
Attacker requests reset for their own account → gets a token → uses it to reset someone else’s password.

**Test:**
Try applying your reset token to another user's email reset form.

---

### 5. Token Reuse
A token should be single-use.

**Test:**
Submit the same token twice:
- First time: should succeed  
- Second time: should FAIL  

If both succeed → critical vulnerability.

---

### 6. Reset Without Old Password (Improper Verification)
Some sites allow sensitive changes without validating identity.

**Test:**
Check if you can:
- Change email without verifying password  
- Reset via "logged-in" mode without verifying user  
- Change 2FA settings without re-authenticating  

---

### 7. No Rate Limiting / Bruteforce on Reset Codes
Applies to:
- OTP codes  
- Email-based tokens  
- SMS codes  

**Test:**
Send 100 OTP attempts:
- If no lockout → vulnerable  
- If fixed-length codes (e.g., 6 digits) → easy to bruteforce  

---

### 8. Reset Link Not Expiring or Very Long TTL
Weak TTL:
- 24–72 hours  
- No expiration at all  

**Test:**
Use old tokens from days ago.

---

### 9. Password Reset via Registered Email Change
Some platforms allow users to change email, then immediately request reset to the attacker-controlled email.

**Test:**
Try updating email → trigger password reset → reset target’s account.

---

## High-Value Targets
Common places where reset flows are implemented incorrectly:
- Legacy enterprise systems  
- Custom auth systems (not OAuth)  
- Banking & fintech portals  
- Healthcare systems  
- E-commerce platforms  
- Social media and messaging apps  

---

## Automation Ideas
- Generate multiple reset tokens and compare randomness  
- Bruteforce OTP codes (rate-limit detection)  
- Check for user enumeration using a script  
- Attempt cross-user token reuse  
- Map full reset workflow automatically  

---

## Reporting Tips
Include:
- Step-by-step reproduction  
- Screenshots of reset flow  
- Exact token behavior  
- Demonstrated account takeover  
- Business impact: unauthorized access, fraud, identity theft  

---

## Remediation
- Enforce per-user token binding  
- Use cryptographically secure random values  
- Enforce short TTL (5–15 mins)  
- Invalidate token after first use  
- Require re-authentication for sensitive changes  
- Add rate limiting & monitoring  

---
