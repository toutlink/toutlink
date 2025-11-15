# Chapter 10 — Cross-Site Scripting (XSS) (Elite Notes)

XSS allows an attacker to run JavaScript in a victim’s browser in the context of a vulnerable site.

## Main Types
- Reflected XSS
- Stored XSS
- DOM-based XSS
- Hybrid flows (DOM + server)

## XSS Hunting Workflow

1. **Find all input points**
   - Query parameters
   - Form fields
   - JSON data
   - Headers (User-Agent, Referer, X-Forwarded-For)
   - File names and comments

2. **See where input is reflected**
   - In HTML body
   - In HTML attributes
   - Inside JavaScript blocks
   - Inside URLs

3. **Send harmless probes**
   - Examples:
     - `">DEBUG`
     - `'/>DEBUG`
     - `</script>DEBUG`

4. **Identify context and test payloads**

### Example Payload Concepts (for demonstration)

**HTML context:**
```text
"><img src=x onerror=alert(1)>
### JavaScript context:
';alert(1);// 
### Attribute context:
" onmouseover="alert(1)
### Common XSS Locations

Search results

Error messages

Chat and comment systems

Profile pages

Admin dashboards and logs

### Automation Ideas

Script that injects probes into all parameters and searches for reflection

DOM scanner for dangerous sinks (innerHTML, document.write, etc.)

### Reporting Tips

Provide a simple payload that leads to a visible alert or clear JS execution

Explain possible impact (session theft, CSRF via XSS, data exfiltration)

Include steps that a triager can easily reproduce
