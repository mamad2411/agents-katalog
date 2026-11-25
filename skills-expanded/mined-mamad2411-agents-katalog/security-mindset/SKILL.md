---
name: security-mindset
description: Security mindset - think like an attacker
---

# /security-mindset — Security Mindset

Think like an attacker. Question trust assumptions. Validate all input.

## Core Philosophy

"Security is a process, not a product."

The security mindset means:
1. **Think like an attacker** — How would I break this?
2. **Assume breach** — What happens when (not if) security fails?
3. **Defense in depth** — Multiple layers, no single point of failure
4. **Trust minimization** — Give minimum required privileges

## Key Principles

### 1. Threat Modeling

Before writing code, ask:
- What are we protecting? (Assets)
- From whom? (Threat actors)
- What can go wrong? (Attack vectors)
- What's the impact? (Risk assessment)

### 2. Attack Surface Reduction

```
// Bad: Large attack surface
app.use(express.json({ limit: '50mb' }));
app.use('*', handleEverything);

// Good: Minimal surface
app.use(express.json({ limit: '100kb' }));
app.use('/api/v1', rateLimiter, validateInput, apiRoutes);
```

### 3. Fail Securely

```csharp
// Bad: Fails open
try {
    if (user.HasPermission(resource)) return Allow();
} catch { }
return Allow(); // WRONG - fails open

// Good: Fails closed
try {
    if (user.HasPermission(resource)) return Allow();
} catch (Exception ex) {
    Log.Error(ex);
}
return Deny(); // Default deny
```

### 4. Trust Nothing from Outside

- All user input is malicious until validated
- All external APIs may be compromised
- All network traffic may be intercepted
- All client-side controls may be bypassed

## Security Questions (Ask Every Review)

1. **Authentication**: How do we know who this is?
2. **Authorization**: Should they be allowed to do this?
3. **Input validation**: What happens with malformed input?
4. **Error handling**: Do errors leak information?
5. **Logging**: Would we detect an attack?
6. **Data protection**: Is sensitive data encrypted?

## Common Vulnerabilities to Check

- Injection (SQL, command, LDAP)
- Broken authentication
- Sensitive data exposure
- XXE (XML External Entities)
- Broken access control
- Security misconfiguration
- XSS (Cross-Site Scripting)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging/monitoring

## Anti-Patterns (Always Reject)

- Security through obscurity
- Rolling your own crypto
- Trusting client-side validation
- Storing passwords in plaintext or reversible encryption
- Overly permissive CORS
- Hardcoded secrets
- Verbose error messages to users

## When to Invoke /security-mindset

- Designing authentication/authorization
- Handling sensitive data
- Processing user input
- Implementing API endpoints
- Code reviews for security
- After any security incident
