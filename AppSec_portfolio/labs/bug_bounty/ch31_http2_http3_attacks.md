# Chapter 31 – HTTP/2 & HTTP/3 Attacks  
Advanced Flow Control Abuse • Stream Layer Exploits • Rapid Reset • Cross-Stream Injection

---

# Why HTTP/2 & HTTP/3 Matter
Most large platforms now use:
- Cloudflare
- Google Frontend (GFE)
- AWS ALB
- Fastly
- Akamai

These automatically upgrade traffic to **HTTP/2** or **HTTP/3 (QUIC)**.

This introduces **new attack surfaces** that do NOT exist in HTTP/1.1:
- Stream multiplexing
- Header compression (HPACK/QPACK)
- Flow control mechanisms
- Rapid reset behavior
- Frame-based parsing
- Cross-stream confusion

HTTP/2 bugs have caused **multi-million-dollar bounty payouts**.

---

# Core Concepts

## HTTP/2: Stream Multiplexing
One TCP connection carries multiple “streams”:
Stream 1 → Login request
Stream 3 → JS file
Stream 5 → API request


Vulnerabilities come from **how servers interpret streams**.

---

## HTTP/3 (QUIC): UDP-Based
HTTP/3 replaces TCP with QUIC:
- Faster
- More forgiving of packet loss
- New frame types
- Even more parsing complexity

More parsing = more bugs.

---

# Attack Class 1 — HTTP/2 Rapid Reset (CVSS 10.0)

Famous global outage (2023):
- Attackers sent **hundreds of thousands of RST_STREAM frames**
- Servers were forced to process EACH ONE
- Caused global DoS for Google, Cloudflare, Amazon, Meta

### Simplified attack behavior:
1. Open a single HTTP/2 connection  
2. Send a request on a new stream  
3. Immediately cancel it with `RST_STREAM`  
4. Repeat at scale

Servers did massive work handling resets → meltdown.

### Bug bounty angle:
You look for:
- Excessive CPU usage per RST_STREAM  
- Infinite loops in stream teardown  
- Failure to enforce limits  

---

# Attack Class 2 — Request Smuggling Over HTTP/2

Even though HTTP/2 is frame-based, many servers downgrade internally to HTTP/1.1 **incorrectly**.

This leads to:

## HTTP/2 → HTTP/1 Smuggling
Examples:
- Extra CONTINUATION frames  
- Mixing header ordering  
- Conflicting pseudo-headers  
- Abusing `content-length` logic  
- Fragmentation mismatches

### Payload example (conceptual):
Send multiple `:path` headers:


:method: POST
:path: /endpoint
:path: /smuggled


Some backend servers interpret the second one.

This enables:
- Cache poisoning  
- Admin bypass  
- Credential theft  
- WAF bypass  
- Phantom requests injected to backend  

---

# Attack Class 3 — HPACK / QPACK Side-Channel Leaks

HPACK = Header compression for HTTP/2  
QPACK = Header compression for HTTP/3

Compression-based side channels leak:
- Tokens  
- Cookies  
- API keys  
- Internal headers  
- CSRF tokens  

### Example:
Change a single byte and observe:
- Size delta  
- Timing delta  
→ Allows guessing secrets character by character.

This is similar to CRIME/BREACH but **more powerful**.

---

# Attack Class 4 — Flow Control Abuse

Servers use flow control windows:


INITIAL_WINDOW_SIZE
MAX_FRAME_SIZE
MAX_CONCURRENT_STREAMS


If incorrectly enforced, attackers can:
- Consume all memory  
- Prevent streams from closing  
- Cause persistent deadlocks  
- Block legitimate users

### Example flow-control exploitation:
1. Open stream  
2. Advertise tiny window (1 byte)  
3. Server holds entire response waiting  
4. Repeat with thousands of streams  
→ Exhaust server threads and memory

Complete DoS on HTTP/2 endpoints.

---

# Attack Class 5 — Priority Tree Abuse

HTTP/2 allows clients to send a “priority tree” describing:
- Weight  
- Parent streams  
- Dependencies  

Servers often mis-implement prioritization:
- Infinite loops  
- Recursion bugs  
- Memory blowups  
- Wrong stream scheduling

This leads to DoS or request starvation.

---

# Attack Class 6 — Cross-Stream Confusion Attacks

Server mixes metadata between streams:
- Mixes cookies  
- Mixes authorization  
- Mixes CSRF tokens  
- Mixes response fragments  

This results in:
- User A getting User B’s data  
- Token leakage  
- Full account takeover

This category produces **critical-level vulnerabilities**.

---

# Practical Testing Checklist

## 1. Test Rapid Reset Behavior
Send 1,000–50,000 RST_STREAM frames:
- Check CPU usage
- Check error logs
- Detect rate limits

## 2. Test Stream Multiplexing Edge Cases
Send:
- Duplicate pseudo-headers  
- Missing :path  
- Extra framing  
- Interleaved HEADERS/DATA frames  

Observe backend behavior.

## 3. Test HTTP/2 → HTTP/1 Downgrade
Force downgrade by disconnecting streams:
- Some servers reveal backend smuggling bugs.

## 4. Test Flow Control Deadlocks
Advertise small window sizes:
- 1 or 0  
- Open 100+ streams  
- Observe blocking

## 5. Test HPACK / QPACK Compression Oracle
Change header lengths:
- Compare response sizes  
- Look for compression side channels  

## 6. Test Cross-Stream Data Mixups
Send parallel requests:


Stream 1: authenticated request
Stream 3: unauthenticated request

Look for:
- Cookie bleed  
- Header bleed  
- Token bleeding  

---

# Tools for HTTP/2/3 Bug Hunting

## Essential:
- h2csmuggler  
- h2spec  
- nghttp  
- curl --http2  
- curl --http3  
- hyper  
- burp suite (with HTTP/2 extension)

## Elite tools:
- lsquic  
- ngtcp2  
- quiche  
- Request Baskets with HTTP/2 support  
- Custom frame fuzzer  

---

# High-Value Targets

These companies are highly vulnerable historically:
- Google  
- Cloudflare  
- Amazon AWS  
- Meta  
- Fastly  
- Akamai  
- Any site behind Cloudflare “free tier”  

Why?  
Because they all support:
- Stream multiplexing  
- HPACK/QPACK  
- Frame parsing  
- Massive backend fan-out  

Complexity = bugs.

---

# Reporting Tips

Include:
- Exact frame sequence  
- Stream numbers  
- Headers used  
- Backend behavior  
- Impact estimation (CPU, memory, confusion, credentials)  
- Tools used  
- Reproduction steps  

HTTP/2 bugs get high rewards:
- $10,000 – $50,000 (common)
- $100,000+ for major vendors  

---

# Remediation
- Enforce RST_STREAM rate limits  
- Validate all pseudo-headers  
- Strong request normalization  
- Disable HTTP/2 downgrades  
- Strict HPACK/QPACK bounds  
- Enforce flow control limits  
- Add stream concurrency caps  
- Patch priority tree recursion bugs  
- Maintain separate state per stream  

---

# Summary
HTTP/2/3 attacks represent the **future** of high-impact bug bounty work.  
Mastering:
- Frame injection  
- Rapid reset  
- Stream parsing  
- Compression side channels  
- Downgrade vulnerabilities  

puts you in the **top 1% of hunters globally**.
