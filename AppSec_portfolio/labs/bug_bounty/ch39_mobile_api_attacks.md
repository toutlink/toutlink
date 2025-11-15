# Chapter 39 – Mobile API + Mobile App Attacks  
Android • iOS • API Reverse Engineering • Certificate Pinning Bypass • Hidden Endpoints • Mobile-Specific BOLA

Mobile apps are **the richest attack surface** in modern bug bounty.  
Almost every mobile app exposes internal APIs that web clients never see.

This chapter teaches you how elite hunters extract, reverse, and abuse mobile app APIs.

---

# 1. Why Mobile Apps Are Gold Mines

Mobile apps often contain:
- Hidden admin APIs  
- Unused but still active endpoints  
- Hardcoded secrets  
- AWS keys  
- Firebase tokens  
- Internal API URLs  
- Feature flags  
- Undocumented GraphQL operations  

Most companies forget mobile apps expose everything.

---

# 2. Tools You Need

## Android:
- **jadx-gui** (APK decompiler)
- **apktool** (resource extraction)
- **frida** (dynamic instrumentation)
- **objection** (no-code frida wrapper)

## iOS:
- **ipa extractor** (via jailbroken or proxy)
- **class-dump** / **Frida**

## Network:
- Burp Suite  
- mitmproxy  
- Android emulator w/ proxy  
- iOS device with CA certificate installed  

---

# 3. Extracting the Mobile App (APK)

If you have the APK file:

jadx-gui app.apk

diff
Copy code

Look for:
- API URLs  
- OAuth endpoints  
- JWT secrets  
- Payment API  
- Admin-only functions  

Search inside the app for:
/admin
/internal
/v3/private
/experimental
/debug
/staging

yaml
Copy code

These often lead to critical bugs.

---

# 4. Certificate Pinning Bypass (The #1 Blocker)

Most modern apps pin SSL certificates.

### Using Objection:
objection -g com.company.app explore
android sslpinning disable

shell
Copy code

### Using Frida Script:
frida -U -f com.company.app -l bypass.js --no-pause

yaml
Copy code

After bypass → Burp sees ALL traffic.

If you can intercept mobile traffic:
→ **You now own the entire mobile API attack surface**.

---

# 5. Mobile API BOLA (Extremely Common)

Mobile apps often call APIs like:

GET /api/v3/messages/23934
GET /api/v2/transactions/1104
GET /api/v1/orders/5021

markdown
Copy code

But the mobile **UI hides other IDs**.

Try replacing ID:

/messages/23935

yaml
Copy code

If it returns another user’s messages → **High severity BOLA**.

Mobile apps almost always miss:
- per-object authorization  
- role validation  
- account isolation

---

# 6. Hidden Feature Abuse

Mobile apps often ship code for:
- Beta features  
- Admin functionality  
- Future releases  
- Employee features  

Look in code for:
isInternalUser
isAdmin
enableDebugMode
internalBaseUrl

yaml
Copy code

Often they lead to:
- Admin dashboards  
- Internal APIs  
- Debug commands  
- Environment switching  
- Internal test accounts  

---

# 7. Hardcoded Secrets (Very High Impact)

Search for:

AKIA
SECRET_KEY
FIREBASE
PRIVATE_KEY
oauth_client
stripe
sendgrid
twilio

yaml
Copy code

Hardcoded credentials allow:
- backend access  
- cloud control  
- payment abuse  
- impersonation  
- full takeover of mobile backend services  

---

# 8. Attack Surface Expanded via Reverse Engineering

Look inside:
- `assets/`  
- `lib/`  
- `res/raw/`  
- `res/xml/`  
- `/smali` code  

Huge vulnerabilities often appear in:
- offline login fallback  
- debugging modes  
- staging environment keys  
- alternate API hosts  

---

# 9. Mobile API Rate Limit Abuse

Mobile endpoints often lack limits.

Test:
/otp/send
/otp/verify
/password/reset
/username/available

yaml
Copy code

If infinite tries:
- brute force  
- SMS spam  
- credential stuffing  
- account takeover  

---

# 10. Business Logic Flaws (Mobile-Specific)

Examples:
- Add item to cart with negative quantity  
- Override subscription tier fields  
- Modify price in API request  
- Skip onboarding steps  
- Abuse promo codes  
- Redeem coupons multiple times  

Mobile clients often trust the UI but do NOT validate logic.

---

# 11. Jailbreak/Root Detection Bypass

Apps attempt to block reverse engineering.

### Using Frida:
frida -U -f com.app -l jailbreak_bypass.js

yaml
Copy code

### Typical detection flags:
- presence of `su`
- files at `/data/local/tmp`
- debugger ports
- iOS jailbreak paths

Once bypassed:
→ You can run full dynamic analysis.

---

# 12. Mobile-Specific SSRF (yes, it exists)

Look for:
image upload
profile picture fetch
pdf renderer
url preview

markdown
Copy code

If app fetches from URL → test SSRF.

---

# 13. Mobile App WebViews

Test:
- JavaScript injection  
- origin bypass  
- local file read  
- file URL access  
- insecure JS bridges (`addJavascriptInterface`)  

These lead to:
- Account takeover  
- Local file theft  
- RCE in Android if JS interfaces exposed  

---

# 14. Reporting Template (Professional)

Include:

1. **Mobile version + platform**  
2. **Entry point** (app action → API request)  
3. **Reverse engineering evidence**  
4. **Original request** vs **modified malicious request**  
5. **Impact** (always big with mobile APIs)  
6. **Recommended fix**  
   - per-object authorization  
   - enforce server-side ownership  
   - remove secrets from client  
   - restrict unused endpoints  

---

# Summary

Mobile APIs are a *goldmine* because they expose:
- internal APIs  
- hidden features  
- sensitive keys  
- business logic  
- undocumented GraphQL  
- over-privileged endpoints  

Mastering mobile API analysis gives you:
- consistent medium/high-severity findings  
- access to backend systems  
- access to internal features  
- critical bug bounty payouts  

This is a required skill for elite-level AppSec engineers and top bug bounty hunters.
