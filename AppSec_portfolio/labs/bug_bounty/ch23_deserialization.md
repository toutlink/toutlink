# Chapter 23 – Insecure Deserialization, Gadget Chains & Remote Code Execution

## Mental Model
Deserialization = taking **untrusted data** and turning it back into an object.

If attackers can modify serialized objects before the server loads them →  
they can **execute code**, escalate privileges, bypass authentication, or corrupt logic.

Modern apps deserialize:
- JSON Web Tokens (JWT but rarely vulnerable)
- Session cookies  
- API tokens  
- Message queues  
- Cache objects  
- Background job data  
- Framework-specific object formats (Java, PHP, Python, Ruby)

The attack goal:  
**Make the server load attacker-controlled data that triggers dangerous behavior.**

---

# Where Deserialization Happens

## 1. Session Tokens
Some frameworks store session state in:
- Cookies (Flask signed cookies)
- Redis / Memcache blobs
- Server-side session objects

If signature/secret = weak → attacker can forge session data.

---

## 2. API Objects
APIs often deserialize:
```json
{
  "user": {
    "role": "admin"
  }
}
If server trusts roles directly → privilege escalation.
3. Message Queues

Processing pipelines that use:

RabbitMQ

Kafka

Celery

RQ

Sidekiq

Workers load arbitrary task data → RCE if format is unsafe.

4. File-Based Serialized Objects

Examples:

Java .ser

Python pickle

Ruby Marshal

PHP serialized strings:

O:8:"stdClass":1:{s:5:"admin";b:1;}


Any of these formats → high risk.

Language-Specific Danger Zones
Python (pickle)

Most famous vulnerability:

pickle.loads(attacker_controlled_data)


This equals instant RCE, because pickle executes code during loading.

PHP

PHP’s unserialize() allows "gadget chains" in common libraries.

Example payload:

O:4:"User":1:{s:5:"admin";b:1;}


If the class has a __wakeup() or __destruct() method → attacker triggers internal actions.

Java (Big Target)

Java serialization historically produced catastrophic bugs (Apache Commons Collection gadget chains).

Payloads delivered via:

Cookies

API parameters

Multipart forms

RMI/JMX endpoints

Impact can be full RCE.

Ruby

Ruby’s Marshal.load() behaves like Python’s pickle → highly dangerous if used on untrusted data.

Testing Methods
1. Look for Serialized Patterns

Indicators:

O:, a:, s: → PHP serialized

gggg.... → Python pickle base64

rO0AB → Java serialization magic header

Strange base64 blobs

Very long cookie values ending with ==

JSON fields that hold objects instead of primitives

2. Tamper and Re-Send

Modify fields:

Change roles or permissions

Add unwanted fields

Change object type

Insert path traversal strings

Insert command execution strings (language dependent)

If server:

Errors

Accepts modified data

Behaves weirdly

Shows stack traces

→ You found an entry point.

3. Use ysoserial (Java / PHP)

Most powerful tool for deserialization exploits.

Java:

java -jar ysoserial.jar CommonsCollections6 "touch /tmp/pwned" | base64


PHP:

phpggc Monolog/RCE1 system id


Frameworks with known gadgets:

PHP: Monolog, Laravel, Symfony

Java: CommonsCollections, Spring, WebLogic

Ruby: YAML / Marshal

4. Fuzzing

Send corrupted serialized data:

Add/delete object fields

Break format partially

Replace numbers with strings

Use invalid encodings

Servers often reveal:

Class names

Gadget candidates

Internal structure

High-Impact Real-World Examples (Generalized)
1. RCE on Enterprise App

Attacker sends crafted Java serialized object → server deserializes → executes attacker’s command.
Impact: Full server takeover.

2. Privilege Escalation via Session Cookie

Serialized session cookie includes:

role=“user”


Attacker modifies to:

role=“admin”


Server trusts cookie and upgrades privileges.

3. Payment Manipulation

Serialized shopping cart:

O:5:"Cart":2:{s:5:"item";s:8:"Laptop";s:5:"price";i:0;}


Attacker changes price → purchases for free.

4. API Queue RCE

Worker receives:

task={"op": "resize_image", "file": "/tmp/aaa"}


Attacker changes format → loader interprets it as Python object → code execution inside worker container.

High-Value Targets

Focus on:

Legacy Java/PHP apps

Monolithic enterprise SaaS

Background job systems

Upload-to-process features

Anything using Redis with insecure serialization

Microservices exchanging messages

Automation Ideas

Build base64 decoder + serialization fingerprint tool

Gadget chain scanner (integrate ysoserial/phpggc)

Payload generator library

Worker queue protocol mapper

Cookie decoding bot

Reporting Tips

Include:

Endpoint / cookie / header where exploit happens

Format detected (Java, PHP, pickle, Ruby)

Exact payload used

Proof of arbitrary modification or RCE

Steps to reproduce

Business impact (RCE is highest severity possible)

Remediation

Never use unsafe serialization formats

Input validation + strict schema

Replace pickle / PHP serialize / Java native serialization

Enforce signing + encryption

Use safe encoders (JWT, Pydantic, protobuf)

Implement object whitelisting

Harden job queues
