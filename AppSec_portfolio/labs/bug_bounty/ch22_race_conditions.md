# Chapter 22 – Race Conditions (TOCTOU), Parallel Requests & Concurrency Attacks

## Mental Model
A race condition happens when **two or more requests hit the server faster than it can update state**, creating inconsistencies.

TOCTOU → Time Of Check, Time Of Use  
If CHECK and ACTION are not atomic → you break the system.

Attackers exploit this by sending **many parallel requests at once** to force:
- Double spends  
- Free purchases  
- Bypassed limits  
- Duplicate withdrawals  
- Overwritten security checks  
- Skipped validation  
- Multi-use one-time tokens  

This category produces **EXTREMELY high-impact bugs**.

---

## Where Race Conditions Are Likely
Look for features involving:

### 1. Money or Digital Assets (Top Priority)
- Wallets / balances  
- Refunds  
- Credits  
- Coupons  
- Gift cards  
- Payment flows  
- Subscription invoices  

**If money is involved → race it.**

---

### 2. Counters & Limits
Targets:
- Rate limits  
- OTP usage  
- Promo codes  
- Password attempts  
- API quotas  
- Inventory stock  
- Download limits  

If server checks first, then updates → it’s vulnerable.

---

### 3. Multi-Step Operations
Examples:
- Checkout → confirm → pay  
- KYC workflows  
- Approval flows  
- Two-step settings updates  
- Password/email changes  

**Attack idea:** Execute Step 2 multiple times before Step 1 completes.

---

### 4. Redeemable Items
- “Use coupon”  
- “Redeem reward”  
- “Claim bonus”  
- “Apply discount”  

If redeeming twice works → jackpot.

---

### 5. File Upload/Overwrite
If server saves the file before checking → overwrite important files (rare but real).

---

## Attack Methods

### Method 1 — Burp Intruder (Turbo Mode)
Send 20–200 parallel requests.

Common payloads:
{
"coupon": "DISCOUNT100"
}

### Method 2 — Turbo Intruder (Most Powerful)
Python-based script inside Burp that sends **hundreds of requests simultaneously**.

Attack logic:
```python
for i in range(200):
    engine.queue(req, pause=False)
Method 3 — DIY Script (curl + xargs)

Example: seq 1 50 | xargs -n1 -P50 curl -X POST https://target/api/redeem

Method 4 — Browser Automation

If web-only:

Selenium

Playwright

Puppeteer

Real SSR Race Attack Examples (Generalized)
1. Double Withdrawal

Legit flow:
CHECK: Balance = 100
USE: Withdraw 100 → new balance = 0
Attacker sends 20 requests → balance check retrieves 100 each time.

Impact:
Withdraw 100 × 20 = $2000 stolen.

2. Bypassing One-Time Token

Password reset or email change tokens:

Server verifies token, THEN invalidates it.

Attacker fires multiple requests → ALL succeed.

Impact:
Email changed multiple times or takeover.

3. Free Purchases

E-commerce race:

Apply coupon multiple times

Checkout before price recalculation

Race between “item availability” and “payment accepted”

Impact:
$0 orders or negative prices.

4. Quota Bypass

API rate limit → 60 requests/min.

Attacker sends 60 requests in 1 millisecond → server counts it as 1 second window.

5. Account Upgrade Abuse

Race premium feature upgrade to credit the user more than once.

Indicators of Race-Condition Vulnerability

Check server responses:

Duplicate “success” messages

Balance not deducted

Multiple “redeem success” outputs

Inventory becomes negative

Server logs errors for collisions

Repeated charges/refunds

High-Value Programs for Race Testing

Nearly all financial or SaaS platforms:

Exchanges

FinTech apps

Reward/loyalty systems

Subscription businesses

E-commerce

Banks

These pay high bounties for race conditions.

Testing Strategy
Step 1 — Identify a State-Changing Operation

Look for endpoints that modify:

Money

Credits

Tokens

Settings

Inventory

Redeemable items

Step 2 — Capture the Request in Burp
Step 3 — Send 50–500 Parallel Requests
Step 4 — Check server artifact changes:

Logs

Repeated success responses

Balance changes

Stock changes

Duplicate orders

Step 5 — Try Real-World Variants

Change request order

Include delays

Exploit retries

Play with caching

Automation Ideas

Turbo Intruder script templates

Race-condition scanner focusing on POST/PUT/PATCH

Queue-based attack generator

Workflow race mapper

Cluster-based burst sender

Reporting Tips

Include:

Targeted endpoint

Step-by-step POC

Number of parallel requests used

Actual vs expected behavior

Financial impact (quantified)

Screenshot of duplicate success messages

Recommended fix (atomic transactions)

Remediation

Make operations atomic

Use database transactions

Lock rows or resources

Use versioning for updates

Prevent repeated tokens

Add idempotency keys

Enforce server-side serialization

Apply rate limiting AT THE SERVER, not client-side
