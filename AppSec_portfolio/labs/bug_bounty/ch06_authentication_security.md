# Chapter 6 — Authentication Security (Elite Notes)

Authentication is the first gate. If it’s weak, everything else falls.

## Key Attack Surfaces
- Login form (username / email / phone)
- Password reset and account recovery
- Multi-factor authentication (2FA/OTP)
- “Remember me” and device trust
- Social login (OAuth, SSO)

## Elite Testing Workflow

1. **Fingerprint the auth flow**
   - What identifiers are used? (email, username, phone)
   - Are there rate limits or CAPTCHA?
   - Are responses different for valid vs invalid accounts?

2. **Username / account enumeration**
   - Compare responses for:
     - Valid vs invalid usernames
     - Valid vs invalid emails
   - Look at:
     - Error messages
     - HTTP status codes
     - Response times

3. **Password reset testing**
   - Can you reset a password using only a username or ID?
   - Are reset tokens:
     - Single-use?
     - Long-lived?
     - Tied to IP/device?
   - Can tokens be guessed or reused?

4. **2FA / OTP bypass paths**
   - Check alternate login flows:
     - Mobile vs web
     - SSO vs normal login
   - Look for endpoints that:
     - Skip 2FA after certain steps
     - Allow session upgrade without OTP
   - Check if OTP can be:
     - Reused
     - Used on multiple accounts

## Common Vulnerabilities
- Account enumeration through error messages
- Weak password reset logic
- Missing 2FA enforcement on sensitive actions
- No rate limiting on login / reset
- Reuse of old reset links or tokens

## Automation Ideas
- Script to test login responses for enumeration
- Script to replay reset links and tokens
- Script to test many OTP submissions with timing checks

## Reporting Tips
- Include full request/response pairs
- Show realistic attacker impact (account takeover, 2FA bypass)
- Propose clear mitigations (rate limiting, better token design, consistent error messages)
