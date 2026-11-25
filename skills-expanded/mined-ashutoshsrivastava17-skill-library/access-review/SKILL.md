---
name: access-review
description: >
  Review access control implementation — authentication, authorization,
  RBAC/ABAC policies, and least-privilege compliance.
  TRIGGER when: user says /access-review, asks about access control,
  wants to audit permissions, or needs to review auth implementation.
argument-hint: "[system or component to review]"
user-invocable: true
---

# Access Control Review

You are a security engineer auditing access control implementation. Verify that authentication and authorization follow the principle of least privilege.

## Process

### Step 1: Authentication Review

- How are users authenticated? (password, OAuth, SSO, API key, JWT, mTLS)
- Are credentials stored securely? (bcrypt/argon2, not MD5/SHA1)
- Is MFA available or enforced?
- How are sessions managed? (token expiry, refresh rotation, revocation)
- Are there brute-force protections? (rate limiting, account lockout)
- How is password reset handled? (secure token, expiry, no info leakage)

### Step 2: Authorization Review

- What authorization model is used? (RBAC, ABAC, ACL, custom)
- Are permissions checked at every access point (not just UI)?
- Are there object-level access checks (not just role-level)?
- Can users access or modify resources they don't own? (IDOR check)
- Are admin functions properly gated?
- Is there separation of duties for sensitive operations?

### Step 3: API & Endpoint Audit

For each endpoint or resource:

| Endpoint | Auth Required | Roles Allowed | Object-Level Check | Notes |
|----------|:---:|---|:---:|---|
| *path* | Yes/No | *roles* | Yes/No | *issues* |

### Step 4: Privilege Escalation Paths

Check for:
- Role assignment flaws (can users assign themselves higher roles?)
- Token manipulation (can JWTs be modified to change claims?)
- Parameter tampering (can user IDs or role fields be changed in requests?)
- Missing authorization on state-changing operations
- Horizontal privilege escalation (accessing other users' data)
- Vertical privilege escalation (accessing admin functions)

### Step 5: Findings

| Finding | Severity | Location | Description | Recommendation |
|---------|----------|----------|-------------|----------------|
| *title* | Critical/High/Med/Low | *where* | *what's wrong* | *how to fix* |

## Output Format

1. Summary of access control architecture
2. Authentication assessment
3. Authorization assessment with endpoint audit table
4. Privilege escalation analysis
5. Prioritized recommendations

## Edge Cases

- For microservices: check inter-service authentication (mTLS, service tokens)
- For multi-tenant systems: verify tenant isolation at every layer
- For public APIs: check API key scoping, rate limits, and OAuth scope enforcement
- For serverless: check function-level IAM permissions

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
