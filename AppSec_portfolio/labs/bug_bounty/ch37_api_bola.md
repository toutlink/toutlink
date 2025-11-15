# Chapter 37 – API Abuse & Broken Object Level Authorization (BOLA)
IDOR • Mass Assignment • Privilege Escalation via APIs • Mobile API Abuse • Hidden Admin Endpoints

APIs power most modern apps. They often expose internal objects directly:
- `/users/{id}`
- `/orders/{order_id}`
- `/accounts/{acct_number}`
- `/messages/{msg_id}`

If the server **does not check ownership on every request**, you get full account takeover.

BOLA is consistently in the **Top 3 highest-paid** vulnerabilities in programs like:
- Shopify
- Coinbase
- Uber
- TikTok
- GitHub

---

# 1. What BOLA Really Means

A user can access or modify another user’s object:

Examples:
- Get another user’s profile  
- Cancel someone else’s order  
- View private messages  
- Download private invoices  
- Modify subscription tiers  

This is NOT authentication failure.  
This is **authorization** failure.

---

# 2. BOLA Testing Checklist (Elite Level)

## 2.1 Replace object identifiers
Try replacing:
- `user_id`  
- `account_id`  
- `order_id`  
- `invoice_id`  
- `message_id`  

with:
- another user’s ID  
- sequential numbers  
- predictable patterns  
- recently created IDs

**If the API returns data → BOLA confirmed.**

---

## 2.2 Try deleting/updating other users’ objects
Examples:
DELETE /api/orders/112
PUT /api/orders/112 {"status":"cancelled"}

yaml
Copy code

If allowed → **Impact is huge**.

---

## 2.3 Hidden fields in mobile apps
Mobile apps often contain:
- admin-only fields  
- hidden features  
- undocumented API endpoints

Use:
- jadx (Android)
- objection / frida
- ipa extraction  
- mitmproxy / burp mobile config  

Look inside the app for:
- `/admin/*`
- `/internal/*`
- `/v3/private/*`

---

## 2.4 Check GraphQL (super common BOLA source)
Send:
query getUser($id:Int){ user(id:$id){ email, role, balance } }

yaml
Copy code

GraphQL usually:
- exposes too many fields  
- does not apply authorization on every resolver  

---

## 2.5 Mass Assignment Abuse
Dangerous if API accepts bulk updates:

PATCH /api/user/123
{
"email": "attacker@evil.com",
"is_admin": true
}

yaml
Copy code

If server does not whitelist safe fields:
→ **Privilege escalation**.

---

# 3. High-Value BOLA Targets

- Order systems  
- E-commerce carts  
- Banking transactions  
- Subscription upgrades  
- Payment methods  
- Saved credit cards  
- Invoices and receipts  
- Health records  
- Admin user management  
- Internal company dashboards  

---

# 4. Attack Techniques (Professional)

## 4.1 Numeric Substitution
/users/21 → /users/22

makefile
Copy code

## 4.2 UUID Cycling
Try:
00000000-0000-0000-0000-000000000001
00000000-0000-0000-0000-000000000002

yaml
Copy code

Some APIs do sequential UUIDs.

---

## 4.3 Parameter Pollution
/api/user/profile?user_id=123&user_id=999

yaml
Copy code

Some frameworks take the last ID.

---

## 4.4 Force Browsing
Try:
/api/admin/users
/api/admin/reports
/api/admin/invoices

yaml
Copy code

If no admin check → full system dump.

---

## 4.5 Guessing private resource names
Common patterns:
/exports/invoice-2024-01-004.pdf
/backups/db-01-03-2024.gz

yaml
Copy code

If accessible → serious data leak.

---

# 5. Automation Ideas

### Burp Intruder
Enumerate IDs quickly:
1–5000

shell
Copy code

### Custom Python Script
for id in range(1,10000):
GET /api/users/{id}

yaml
Copy code

### Use your mobile device
Apps reveal endpoints via:
- network logs  
- HAR export  
- certificate pinning bypass  

---

# 6. Real-World Bug Bounty Examples (Generalized)

### Example 1 — Unlimited account access
A fintech app exposed:
GET /api/transactions/{id}

yaml
Copy code
Changing the ID → full financial history of others.

Payout: **$12,500**

---

### Example 2 — Cancel any user’s order
DELETE /api/orders/{order_id}

yaml
Copy code

Impact:
- attacker cancels purchases  
- affects merchant business  

Payout: **$7,500**

---

### Example 3 — Upgrade yourself to admin
API allowed:
PATCH /api/users/12 {"role": "admin"}

yaml
Copy code

Payout: **$20,000**

---

### Example 4 — Download private documents
/api/invoices/2023-0041.pdf

yaml
Copy code

Predictable IDs, no auth.

Payout: **$5,000–$15,000**

---

# 7. Reporting Template (Professional)

Include:

### 1. Endpoint tested  
`GET /api/orders/{order_id}`

### 2. Normal behavior  
User should only access their own order.

### 3. Vulnerability  
Attacker can replace `order_id` and access any order.

### 4. Proof of Exploit  
- request  
- response containing another user’s data  

### 5. Impact  
- PII leak  
- financial data exposure  
- account takeover  
- business logic compromise  

### 6. Remediation  
- Enforce per-object authorization  
- Validate ownership on every request  
- Do not rely on client-side checks  
- Use indirect identifiers (non-sequential IDs)

---

# 8. Remediation Summary

- Apply authorization at the **controller** level  
- Use **access control middleware**  
- Replace numeric IDs with:
  - UUIDv4  
  - hashed IDs  
  - opaque IDs  

- Prevent over-posting:
  - whitelist allowed fields  

- Add rate limits to resource-heavy APIs  

---

# Summary

API BOLA is responsible for the majority of high-severity bug bounty payouts today.

Mastering API authorization flaws gives you:
- personal data disclosure  
- financial manipulation  
- account takeover  
- privilege escalation  
- massive impact  

This is core skill for any elite AppSec engineer or top-tier bounty hunter.
