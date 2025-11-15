# Chapter 17 – Business Logic & Workflow Abuse

## Mental Model
Business logic vulnerabilities occur when the application behaves *as designed*, but the design allows:
- Unintended actions  
- Abused workflows  
- Skipped steps  
- Unauthorized benefits  

This is not technical exploitation like XSS or SSRF.  
This is about *breaking rules the developers assumed users would follow*.

---

## Common Logic Flaw Categories

### 1. Bypass Required Steps
- Skipping payment
- Skipping email/phone verification
- Completing checkout without validating cart
- Approving something without required prior actions

**Tests:**
- Remove a step and jump to final endpoint  
- Replay previous “success” responses  
- Change status fields directly

---

### 2. Race Conditions / TOCTOU
Two or more requests sent at the same time break logic.

**Targets:**
- Promo codes  
- Payment processing  
- Wallet transfers  
- Reward point redemption  
- Inventory stock checks

**Testing Tools:**
- Burp Intruder (Pitchfork / Clusterbomb)  
- Turbo Intruder  
- Race-the-Web

**Example:**
Redeem a coupon multiple times before the system updates usage count.

---

### 3. Parameter Tampering
Manipulating hidden or client-side values:

Examples:
- Changing price fields  
- Modifying quantity limits  
- Flipping boolean flags like `is_admin=true`  
- Changing product IDs

**Techniques:**
- Change value from frontend  
- Intercept API call  
- Modify hidden inputs  
- Remove client-side validation and resubmit

---

### 4. Broken Workflow State Machines
Applications depend on states such as:

INIT → PENDING → APPROVED → COMPLETED

If attacker forces:

INIT → COMPLETED

They bypass rules.

**Examples:**
- Skipping contract signing  
- Skipping KYC steps  
- Marking payment as "PAID" without payment  
- Completing onboarding without required data

---

### 5. Multistep Form Abuse
Targets:
- Loans  
- Account registration wizards  
- Company onboarding flows  
- Profile completion systems  

**Weakness:**
Server assumes user is on Step X because the **client says so**.

**Test:**
Submit Step 3 directly without completing Step 1 or 2.

---

## High-Value Targets
Look for logic in:
- Carts & checkouts  
- Subscriptions & renewals  
- Wallets, credits, points  
- Approval workflows (admins, HR, finance)  
- Booking/reservation systems  
- Promotions & coupon systems  
- Loyalty / reward programs  

---

## Real Attack Examples (Generalized)
- **Refund Abuse:** Request refund but keep the product  
- **Stock Manipulation:** Repeated reservations to block inventory  
- **Price Manipulation:** Change price from $100 → $1  
- **Unauthorized Access:** Skip approval APIs by calling the final endpoint  
- **Logic-based Account Takeover:** Abuse password-reset workflow order  

---

## Automation Ideas
Logic bugs are human-intelligence heavy, but you can automate:

- Workflow diff tools  
- Race condition testing (Turbo Intruder scripts)  
- Forced sequence testing (skipping steps automatically)  
- API replay tools that reorder requests  
- State machine mappers

---

## Reporting Tips
Include:
- Intended workflow (describe normal user journey)  
- Flawed workflow (exact bypass path)  
- Requests used (before/after examples)  
- Clear business impact (money loss, misuse potential, fraud)  
- Diagram of broken flow (optional but powerful)

---

## Remediation
- Enforce server-side step validation  
- Store workflow states server-side only  
- Use atomic transactions for race-sensitive operations  
- Never trust client-side indicators like steps, roles, or prices  
- Add rate limits to critical endpoints  

---



