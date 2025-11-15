# Chapter 40 – Source Code Analysis (SAST for Bug Bounty + AppSec)

Source code analysis lets you discover vulnerabilities **before they appear in the UI or API**, and often reveals entire classes of bugs no scanner or proxy will ever see.

This chapter focuses on:
- Manual source auditing for bug bounty  
- Common insecure patterns  
- Framework-specific pitfalls  
- High-impact findings in codebases  
- Practical techniques used by elite AppSec engineers  

---

# 1. Why Source Code Analysis Is OP (Overpowered)

Benefits:
- Reveals hidden endpoints  
- Shows authentication logic  
- Exposes insecure authorization  
- Finds hardcoded secrets  
- Identifies missed validations  
- Finds vulnerabilities impossible to detect externally  
- Lets you confirm exploitability with precision  

What hunters normally miss → **You catch via source code**.

---

# 2. What You Look For First (The Fast Money)

## 2.1. Hardcoded Secrets  
Search for patterns:

API_KEY
SECRET
PASSWORD
TOKEN
PRIVATE_KEY
AKIA
AIza

yaml
Copy code

High-impact examples:
- AWS keys  
- Stripe keys  
- GitHub personal access tokens  
- Firebase database URLs  
- SMTP credentials  

Immediate payload: takeover systems, read/write cloud data, impersonation, etc.

---

## 2.2. Authentication Logic  
Look for:
- Token generation  
- Password reset flows  
- Signature verification  
- Cookie creation  
- OAuth client secrets  

Weaknesses:
- Predictable tokens  
- Missing expiration  
- Hardcoded signing keys  
- No rate limiting  
- Password reset without verification  

---

## 2.3. Authorization Logic (Most critical)

Authorization breaks when code does:

```python
if user.is_admin:
    allow()
instead of:

python
Copy code
if request.user.id == object.owner_id:
Things to check:

Access checks missing

Access checks done only in frontend

Access checks in the wrong controller

Mixed admin/user logic

Role strings easily spoofed

This reveals high-impact BOLA, privilege escalation, and account takeover without brute force.

2.4. User Input Handling
Look for:

bash
Copy code
eval()
exec()
subprocess()
os.system()
raw SQL
jinja / twig / ejs templates
Dangerous patterns:

String concatenation

Rendering user-controlled content

Taking user input into templates

Building file paths from user input

This leads to:

SQL injection

Template injection

Command injection

Path traversal

RCE

3. High-Value Folders to Explore
Always inspect:

bash
Copy code
/auth
/controllers
/routes
/api
/internal
/services
/utils
/models
/middleware
Then search for "dangerous" files:

pgsql
Copy code
payment*
admin*
debug*
testing*
backup*
beta*
internal*
These often contain:

hidden API endpoints

admin bypasses

debug-only logic accidentally left exposed

4. Framework-Specific Attack Vectors
4.1. Django
Common issues:

Missing @login_required

Insecure ModelViewSet without permission_classes

Trusting request.data['role']

Using eval() in templates

Unsafe custom file upload handlers

Search:

ini
Copy code
permission_classes = []
→ Critical.

4.2. Node.js / Express
Weak points:

eval()

child_process.exec()

jsonwebtoken with ignoreExpiration: true

JWT tokens signed with "secret"

Insecure regex in input validation

Business logic in middleware

Search:

bash
Copy code
router.post('/admin/...')
Often unprotected.

4.3. PHP / Laravel / WordPress
Weak points:

SQL concat strings

file operations

unserialize()

preg_replace with exploitable patterns

plugins exposing internal APIs

Search:

bash
Copy code
$_GET
$_POST
$_REQUEST
These often lead to injection.

4.4. Java (Spring Boot)
Weak points:

SpEL injection

Unsafe data binding

Incorrect use of @PreAuthorize

Missing CSRF protection

Exposed actuator endpoints

Search:

nginx
Copy code
RestController
Actuator
ExecutionContext
5. Hidden Endpoints + Internal APIs
Source code reveals things that recon never will:

Examples:

swift
Copy code
/api/internal/reports
/api/v3/admin/export
/api/v2/debug/enable
/api/beta/users
These endpoints normally:

bypass auth

reveal database dumps

export internal data

support admin-only actions

include unfinished or disabled features

Testing them leads to:

full privilege escalation

data exfiltration

system compromise

6. Code Paths That Commonly Introduce Logic Flaws
Look for:

Multi-step flows handled on client

Missing server-side enforcement

Conditional security behavior

Role-based logic done incorrectly

Payment logic handled by frontend

Example:

nginx
Copy code
if (request.body.price < product.price) {
    finalPrice = request.body.price;
}
Price manipulation. Many real-world exploits started like this.

7. Source Code Guided Injection Attacks
Find injection points manually by searching:

less
Copy code
query(
execute(
cursor.execute(
template.render(
render_string(
subprocess(
Once found:

Try controlled input

Try template injection payloads

Try command injection payloads

Try SQLi payloads

Validate with Burp

This methodology catches blind conditions scanners miss.

8. How to Audit Large Codebases Fast (Elite Method)
Step 1 — Identify main request entry points
Controllers, routes, or views.

Step 2 — Trace inputs
Follow parameters from request → service → model.

Step 3 — Note where validation SHOULD happen
Check if it actually does.

Step 4 — Look for dangerous sinks (eval, DB, file ops).
Step 5 — Map privilege checks
If missing → you likely found a BOLA.

Step 6 — Build a list of hidden endpoints discovered
Test them in Burp.

Step 7 — Try to exploit + validate impact.
This method reduces thousands of files into actionable attack paths.

9. Automation Tools (Optional but powerful)
semgrep

bandit

gitleaks

trufflehog

grep.app

codeql

Semgrep rules for hunting:

makefile
Copy code
repo:company
rule: eval
rule: jwt-secret
rule: weak-auth
rule: insufficient-authz
rule: dangerous-file-op
Elite hunters write custom semgrep rules to scan entire companies.

10. Reporting Template (Professional)
Include:

vulnerable file + line numbers

vulnerable function

proof of concept request

root cause summary

business impact

secure coding recommendation

suggested patch

Source-based reports usually get top-tier payouts.

Summary
Source code analysis gives you:

deeper visibility

faster bug identification

high-severity findings

business logic understanding

internal API discovery

This skill separates average hunters from elite AppSec engineers.

If you can read code and think like an attacker → you win.
