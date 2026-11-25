---
name: api-security-testing-checklist
description: >
  Authorized API security testing checklist covering inventory, authn/z, BOLA/BFLA, mass
  assignment, injection, rate limits, SSRF, file uploads, and business logic. Use for
  structured assessments of owned or in-scope APIs after recon — not unscoped Internet scanning.
---

# API Security Testing Checklist

## Scope And Authorization

- **In scope:** APIs under written authorization / ownership.
- **Out of scope:** Testing out-of-scope hosts; destructive probes without approval.
- Use test tenants; minimize production data access.
- Redact tokens and PII in evidence.
- Start from inventory (`api-recon-and-docs`); deep dives route to specialized skills.

## When To Use

- Systematic API pentest or security QA gate.
- Regression checklist after major API release.
- Mapping coverage across OWASP API Top 10 style risks.
- Coordinating multiple testers on one engagement.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Discovery of endpoints | `api-recon-and-docs` |
| JWT-specific crypto bugs | `api-auth-and-jwt-abuse` |
| Pagination-only issues | `api-pagination-security` |
| IDOR deep methodology | `idor-broken-object-authorization` |
| Rate limit design (defensive) | `api-rate-limit-design` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — checklist map

| Area | Sample questions |
| --- | --- |
| Inventory | Undocumented? Versioned? Admin? |
| Authn | JWT/API key flaws? |
| Authz | BOLA/BFLA? Tenant isolation? |
| Input | Injection, XSS in stored fields? |
| Abuse | Rate limits, pagination bombs? |
| Config | Verbose errors, CORS, TRACE? |
| Logic | Race, coupon, price tamper? |

## Workflow

### 1. Preconditions

1. Scope, accounts (A low, B peer, C admin), tools, rate limits.
2. Inventory attached from recon.
3. Success: checklist completed or N/A justified; findings filed.

### 2. Authentication & session

- [ ] No auth → protected routes fail closed  
- [ ] Invalid/expired tokens rejected  
- [ ] JWT alg/claims tests (`api-auth-and-jwt-abuse`)  
- [ ] API key scopes enforced  
- [ ] Refresh/revoke behavior documented  

### 3. Object & function authz

- [ ] Horizontal: A cannot access B object IDs (BOLA)  
- [ ] Vertical: user cannot call admin functions (BFLA)  
- [ ] Create/update mass assignment of `role`, `tenant_id`, `price`  
- [ ] Batch endpoints don’t skip per-item authz  

```bash
curl -sS -H "Authorization: Bearer $A" "$API/users/$B_ID"
curl -sS -X PUT -H "Authorization: Bearer $A" -H 'Content-Type: application/json' \
  "$API/users/me" -d '{"role":"admin"}'
```

### 4. Input & injection

- [ ] JSON/SQL/NoSQL injection on filters  
- [ ] Command/path/SSRF on URL fields  
- [ ] Upload type/size limits  
- [ ] GraphQL depth/cost if applicable  

Route hits to `injection-checking` / specific skills.

### 5. Pagination, export, rate limit

- [ ] Max page size (`api-pagination-security`)  
- [ ] Export authz  
- [ ] 429 behavior exists on abuse-prone routes  

### 6. Misconfig & data leak

- [ ] Stack traces / debug in prod  
- [ ] Excessive data exposure in list DTOs  
- [ ] CORS overly permissive with credentials  
- [ ] HTTP verb tampering  

### 7. Business logic

- [ ] Negative quantities / price override  
- [ ] Race on redeem/fulfill  
- [ ] Workflow skip (ship before pay)  

### 8. Report

1. Map findings to severity and API Top 10 categories as useful.
2. Include minimal repro; redact secrets.
3. Retest plan.

## Coverage Matrix (track progress)

| Endpoint | Authn | BOLA | Mass assign | Injection | Notes |
| --- | --- | --- | --- | --- | --- |
| GET /items/{id} | | | n/a | | |
| POST /items | | | | | |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Coverage | Matrix signed off | Random tool dump only |
| Accounts | Multi-role proofs | Single admin token testing |
| Impact | Business-aware | “Returns 200” without data class |
| Scope | Written | Tool defaults to huge wordlists on prod |

## Output Checklist

- [ ] Inventory complete
- [ ] Authn section done
- [ ] Authz BOLA/BFLA done
- [ ] Mass assignment checked
- [ ] Injection/SSRF/upload sampled
- [ ] Pagination/rate limit sampled
- [ ] Misconfig/CORS/errors checked
- [ ] Logic abuses considered
- [ ] Findings + residual risk documented
- [ ] Specialist skills used where needed

## Rules

- Authorized APIs only.
- Checklist ensures coverage — not a substitute for deep skills.
- Prefer non-destructive tests in production scopes.
- Multi-account evidence for authz issues.
- Redact all credentials in artifacts.
