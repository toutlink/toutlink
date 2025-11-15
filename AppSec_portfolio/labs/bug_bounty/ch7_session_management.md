# Chapter 7 — Session Management (Elite Notes)

Sessions keep users authenticated. If sessions are weak, attackers can stay logged in as someone else.

## What to Examine
- Cookies and their attributes
- Session IDs or JWTs
- Login → logout lifecycle
- Token rotation (login, password change, privilege change)

## Key Checks

### 1. Cookie Security
- Is `Secure` set for HTTPS-only sites?
- Is `HttpOnly` used to prevent JS access?
- Is `SameSite` set to help prevent CSRF?

### 2. Session Fixation
- Does the session ID change after login?
- If you start as a guest and then log in, does the token rotate?

### 3. Session Expiration
- What happens if you:
  - Stay idle for a long time?
  - Close the browser?
  - Change password?
- Do old tokens continue to work?

### 4. Logout Behavior
- After logout, are:
  - Cookies invalidated server-side?
  - JWTs still accepted?
- Does logout from one device log out other devices (if advertised)?

### 5. JWT-Specific Issues
- Are tokens properly signed and validated?
- Is the algorithm fixed and enforced (no `none` or confusion)?
- Are long-lived tokens used without reason?

## Common Bugs
- No rotation of session ID after login
- Logout only deletes cookie on client side
- JWTs not invalidated after password change
- Session timeout not enforced (sessions never expire)

## Automation Ideas
- Script to check cookie attributes across environments
- JWT inspector (expiration, algorithm, claims)
- Token replay testing tool

## Reporting Tips
- Demonstrate step-by-step how a stolen or fixed session leads to full account compromise
- Emphasize real risk (stolen machines, shared networks, XSS chaining)
