# Chapter 29 – WebSockets Security & Realtime Application Attacks

## Why WebSockets Matter
Modern applications use WebSockets for:
- Chat systems
- Notifications
- Dashboards
- Trading platforms
- Multiplayer games
- Admin monitoring systems
- Realtime analytics

Because the connection stays open and messages bypass traditional HTTP, **security controls are often weaker**. Many bounties ($5k–$25k) come from WebSocket logic issues.

---

# Core Concepts

## WebSocket Handshake
Starts as HTTP:
GET /ws/chat HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: xxxxx
Sec-WebSocket-Version: 13


If server accepts, it switches to a persistent bidirectional channel.

**Common weakness:**  
The handshake is protected, but **messages after handshake often lack authentication or authorization checks.**

---

## Message Types
Two main formats:
- JSON
- Binary (protobuf, custom formats)

Both can carry:
- Privilege escalation payloads
- Sensitive data
- Server commands
- Actions not exposed via HTTP

---

# High-Risk Vulnerability Types

## 1. Broken Authentication in WebSockets
Server trusts the initial handshake only.

Attack:
1. Log in as user A  
2. Intercept WebSocket messages  
3. Replace user identifiers with user B  
4. Send message  
5. Server performs action as user B

You get:
- Account takeover  
- Messaging impersonation  
- Unauthorized admin actions  

### Example Attack Message
```json
{
  "action": "update_profile",
  "user_id": 42,
  "email": "attacker@hacked.com"
}


If server doesn’t check current user → full privilege escalation.

2. Lack of Authorization (most common)

WebSocket handlers often skip:

Role checks

Ownership checks

Resource-level validation

Example:
A WebSocket endpoint:

/ws/admin_panel


Client simply sends:

{"action":"ban_user","id":5}


If server doesn’t enforce admin privileges → attacker can control admin features.

3. Message Manipulation / Hidden Actions

Developers frequently:

Hide admin commands in the frontend

Add debug actions

Expose non-HTTP features through WebSockets

Attackers can:

Enumerate actions

Trigger hidden functionality

Discover undocumented APIs

Try sending:

{"action":"help"}
{"action":"admin.debug"}
{"action":"system.status"}

4. Privilege Escalation Through IDOR in WebSockets

Typical pattern:

{"action":"get_wallet","wallet_id":19}


If server accepts:

Financial theft

Data exposure

Account takeover

5. Injection Attacks (XSS, SQLi, Template Injection)

If WebSocket messages get inserted into:

Templates

Logs

Database queries

Chat systems

Then attacker can cause:

Stored XSS

SQL injection

Server template injection

Log poisoning → RCE

Payload example:

{"message":"<img src=x onerror=alert(1)>"}

6. WebSocket CSRF

Some systems allow:

Anonymous WebSocket connections

No origin checks

No CSRF tokens

Attacker builds a webpage:

var ws = new WebSocket("wss://victim.com/ws");
ws.onopen = () => ws.send('{"action":"steal_funds"}');


If the browser auto-sends cookies → the attack works.

7. Binary Protocol Reverse Engineering

Binary protocol = security through obscurity.

Steps:

Capture WebSocket frames

Identify repeating patterns

Decompile client code

Reverse engineer message format

Recreate payloads manually

This often reveals hidden commands worth big bounties.

8. Rate-Limit Bypass & Brute Forcing Over WebSockets

Many apps forget to apply rate limits.

Use WebSockets to:

Bruteforce OTP codes

Password spraying

Spam actions

Flood high-value endpoints

High-Value Targets

Look for WebSockets in:

Chat apps (messages contain raw HTML)

Trading / stock / crypto exchanges (balance manipulation)

Games (score manipulation)

Monitoring panels (RCE through debug commands)

Payment dashboards

IoT device control apps

Multi-user collaboration tools

These systems are often rushed and fragile.

Exploitation Workflow
Step 1 — Identify the WebSocket endpoint

In Burp:

Proxy → WS history

Look at messages + actions

Step 2 — Discover all actions

Send:

{"action":"help"}
{"action":"commands"}
{"cmd":"*"}

Step 3 — Bruteforce hidden/ undocumented actions

Try patterns:

admin.*
debug.*
system.*
user.*
config.*
internal.*

Step 4 — Check IDOR

Modify all IDs:

{"user_id":1}
{"target_id":2}
{"wallet":4}
{"account":7}

Step 5 — Replace user identifiers

Remove authentication fields entirely:

{"action":"delete_user","user_id":999}

Step 6 — Inject payloads

XSS payloads

SQLi payloads

SSTI payloads

Step 7 — Test CSRF

Create HTML page that connects to WebSocket.

Automation Ideas

Build a message repeater similar to Burp Repeater

Auto-enumerate all numeric parameters

Write a WebSocket fuzzer script

Use Turbo Intruder for high-speed brute force

Build a JSON mutation engine

Reporting Tips

Provide:

WebSocket endpoint URL

Original message

Modified malicious message

Impact and severity

How attacker abuses it reliably

Recommended server-side fix

Screenshots help a lot.

Remediation

Enforce authentication on every message

Add authorization per action

Validate schemas strictly

Block unknown/undocumented commands

Apply rate limits

Sanitize all message content

Implement CSRF protections

Sign messages with HMAC (advanced)
