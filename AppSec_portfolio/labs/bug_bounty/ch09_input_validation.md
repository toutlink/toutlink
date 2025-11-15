# Chapter 9 — Input Validation & Injection (Elite Notes)

Injection flaws appear when user-controlled input is sent to an interpreter without proper validation or escaping.

## Types of Injection
- SQL Injection
- Command Injection
- NoSQL Injection
- Server-Side Template Injection (SSTI)
- File path traversal
- Email header injection

## General Testing Approach

1. **Map all inputs**
   - URL parameters
   - Form fields
   - JSON bodies
   - Headers and cookies
   - File names and metadata

2. **Probe with safe payloads**
   - Look for:
     - Error messages
     - Stack traces
     - Different response lengths
     - Timing differences

3. **Infer backend technology**
   - SQL engine (MySQL, Postgres, MSSQL, etc.)
   - Template engine (Jinja2, Twig, etc.)
   - File system behavior

4. **Escalate to proof-of-concept**
   - Login bypass
   - Reading sensitive files
   - Server-side code execution (where allowed by scope)

## Example Payload Concepts (original, generic)

### SQL Injection (authentication testing)
```text
' OR '1'='1


### Server-Side Template Injection (Jinja2-style)

{{7*7}}

### Path Traversal

../../etc/passwd

### High-Value Targets
- Login and search forms
- Export and reporting features
- Admin panels with filters
- File upload and processing endpoints

### Automation Ideas
- Parameter fuzzer that injects payloads into every parameter  
- Error pattern detector  
- Timing-based tester to detect blind injection  

### Reporting Tips
- Provide exact payload and endpoint  
- Show controlled but convincing impact  
- Recommend parameterization and proper escaping  
