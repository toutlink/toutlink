# Chapter 8 — Access Control (IDOR & Authorization) (Elite Notes)

Access control bugs are some of the most valuable in bug bounty.

## Types of Access Control
- **Vertical**: normal user → admin features
- **Horizontal**: user A can access user B’s data
- **Context-based**: user allowed action in the wrong state or workflow

## Elite Testing Strategy

### 1. Identify “objects”
Look for identifiers:
- User IDs
- Order IDs
- Invoice IDs
- Document IDs
- Ticket / case numbers

### 2. Change the identifiers
- Increment / decrement integers
- Swap UUIDs
- Use IDs from another account
- Use deleted or old IDs

### 3. Test with another user
Use:
- Two browser profiles
- Two Burp sessions
- Two sets of cookies

Send the same request but with different:
- Cookies
- Tokens
- Headers

### 4. Remove or alter auth context
- Remove `Authorization` header
- Remove cookies
- Replace token with another user’s token

### 5. Check for hidden admin or staff features
- Look in JavaScript, HTML, and API responses for:
  - `is_admin`
  - `role`
  - `/admin/`
  - Debug or staff-only endpoints

## Common Weaknesses
- Relying only on client-side checks (e.g., hiding buttons)
- Missing permission checks in APIs
- Validating that user is logged in, but not that they own the object
- “Admin by parameter” (e.g., `role=admin` in request)

## Automation Ideas
- Script to replay requests with different tokens and IDs
- IDOR testing tool that iterates ID ranges
- Diff tool that compares responses between user A and user B

## Reporting Tips
- Show how user A can view/modify data of user B
- Include screenshots and full HTTP requests
- Explain business impact clearly (privacy, financial, compliance)
