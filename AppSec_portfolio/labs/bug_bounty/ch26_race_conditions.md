# Chapter 26 – Race Conditions (TOCTOU) & Advanced Exploitation

## Mental Model
A race condition occurs when **two or more requests are processed at the same time**, and the server:
- Updates shared data incorrectly  
- Uses stale data  
- Executes a critical action twice  
- Fails to enforce atomic operations  

This breaks the application’s intended logic.

This is one of the most profitable bug classes in real bug bounty programs.

---

# TOCTOU Concept (Time of Check → Time of Use)
Server does:

1. **Check** if an action is allowed  
2. **Use** the result to complete the action  

If attacker sends parallel requests between step 1 and 2, they change the outcome.

Example:
- Server checks: “coupon unused?”  
- Attacker sends 20 requests simultaneously  
- Many get processed before system marks coupon “used”  
→ Coupon reused multiple times.

---

# High-Value Race Condition Targets

### 1. Payment Systems
- Coupons  
- Discounts  
- Gift cards  
- Wallet balance  
- Store credit  
- Cashback  
- Promotional codes  

Impact:
- Infinite balance  
- Repeated 100% discount  
- Deposit money without paying  
- Free products  

---

### 2. E-Commerce
- Buy one item multiple times with 1 payment  
- Reduce price by overwriting cart values  
- Reserve all stock and prevent other users from buying  

---

### 3. User Privilege & Role Changes
Race conditions in:
- Account deletion  
- Role promotion  
- Email/phone verification  
- Password reset tokens  

Examples:
- User becomes admin by racing “pending → approved”  
- Multiple password-reset tokens issued → token chaos  

---

### 4. Workflow / State Machines
If states change like:

INIT → PENDING → APPROVED → COMPLETED


Firing parallel requests can skip or duplicate steps:


INIT → COMPLETED
Initiate multiple APPROVE operations


---

### 5. Multi-step Operations
Race attacks frequently break:
- Subscription renewal  
- Order fulfillment  
- Inventory adjustments  
- User onboarding steps  
- KYC verification flows  

---

# How to Test Race Conditions

## 1. Use Turbo Intruder (Burp Suite)
Turbo Intruder is perfect for firing:
- 50–10,000 parallel requests  
- millisecond-level timing  
- payloads for different stages

Common patterns:
- `pitchfork` for multiple parameters  
- `race` mode for simultaneous delivery  

---

## 2. Identify “Critical” Endpoints
Look for:
- Endpoints that modify money  
- Endpoints that change status  
- Endpoints that create or redeem anything  
- Endpoints that mark something “used”  

Anything that should be **done once** is a high-value race target.

---

## 3. Detect Weak Locking
If server uses:
- Client-side state validation  
- Non-atomic DB operations  
- Single-threaded checks  
- Delayed updates  

Then race is likely exploitable.

---

## 4. Look for Parallel API Requests
Test:
- 10 parallel requests  
- 20 parallel requests  
- 50+ parallel requests  

If server responds with:
- Duplicate success  
- Mixed responses  
- Conflicting states  

→ Vulnerable.

---

# Exploitation Techniques

## 1. **Double-Spend**
Redeem the same coupon or gift card repeatedly.

Technique:
- Send 20 redemption requests at exact same time  
- One should mark coupon as “used”  
- Others sneak through before the update applies  

---

## 2. **Wallet Balance Manipulation**
Example:
- Deposit: increases user balance  
- Confirmation: finalizes the deposit  

Send:
1. Deposit request  
2. Confirmation request  
… all in parallel  

Sometimes balance increments multiple times → free money.

---

## 3. **Overwriting Cart Values**
Send updates to the same cart simultaneously.

Results:
- Price set to lowest value  
- Quantity changed unexpectedly  
- Discounts applied repeatedly  

---

## 4. **Race User Privilege Change**
Two simultaneous requests:
- Update profile  
- Change user role  

Server might accidentally apply privileged role.

---

## 5. **Race Password Reset**
Password reset flows often:
- Generate token  
- Validate token  
- Expire token  

If attacker floods:
- Multiple reset emails  
- Parallel token validation  

You can create inconsistent states → takeover.

---

# Real-World Examples (Generalized)

### 1. Banking Double-Charge Refund Bug
User refunded money multiple times because:
- Refund endpoint lacked locking  
- Each request decreased merchant balance  

Severity: Critical (financial fraud)

---

### 2. Gift Card Race → Infinite Money
Redeem gift card 30 times simultaneously → all succeed.

---

### 3. Shopping Cart Price Override
Two “update cart” requests:
- One sets price = $1  
- One sets quantity = 1  

Server merges states → item becomes $1.

---

### 4. Subscription Flow Abuse
Send two “cancel” + “renew” requests → user gets premium without paying.

---

### 5. Inventory Deregulation
Reserve an item 50 times → blocks all other users.

---

# Automation Ideas

- Turbo Intruder race scripts  
- Python async requester  
- “Race Diffing” tool that compares state changes  
- Parallel request firehose (asyncio, aiohttp)  
- Multi-step workflow fuzzers  

---

# Reporting Tips
Include:
- Step-by-step reproduction  
- Screenshot or logs of multiple successes  
- Number of requests and timing details  
- Expected vs. actual behavior  
- Clear business impact:  
  - money loss  
  - privilege escalation  
  - resource exhaustion  
  - account takeover  

---

# Remediation
- Atomic DB operations (`UPDATE … WHERE balance >= amount`)  
- Server-side locking (mutex, transaction locks)  
- Rate limiting  
- Stronger workflow validation  
- Single-use tokens enforced server-side  
- Use queuing for critical operations  
- Prevent parallel execution with unique operation IDs  

---
