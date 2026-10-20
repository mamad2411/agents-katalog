---
name: dast-authenticated-scans
description: >
  Run authenticated dynamic application security scans on owned apps: session
  acquisition, auth scripts, crawl behind login, role matrix, safe scan policies,
  and result triage. Use with ZAP, Burp Enterprise, or similar DAST against
  staging/prod-authorized targets — not unauthenticated-only defaults when the
  risk is in logged-in features.
---

# DAST Authenticated Scans

## Scope And Authorization

- **In scope:** Applications named in authorization with agreed environments and roles.
- **Out of scope:** Credential stuffing real users; scanning third-party SaaS outside contract; destructive active scans on prod without approval.
- Prefer staging full policy; production smoke/authenticated crawl with limited attack strength.
- Protect scanner credentials; rotate after engagement.
- Pair with `recon-and-methodology`, class-specific vulns skills, and `code-quality-standards` for fixes.

## When To Use

- Pre-release or periodic DAST on apps where most functionality requires login.
- Multi-role apps (user/admin) needing separate authenticated contexts.
- CI DAST gates with test users.
- Coverage gaps after unauthenticated-only scans.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Unauthenticated recon only | recon / unauthenticated DAST basics |
| Manual deep XSS/SQLi | class-specific skills |
| CVE on dependencies | `cve-triage-workflow` |
| Full engagement planning | `recon-and-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Authn patterns for scanners

| Pattern | Approach |
| --- | --- |
| Form login | Auth script / recorded login + session verification URL |
| SSO/OIDC | Test IdP user; script code exchange or browser automation |
| JWT header | Token mint for test user; refresh strategy |
| MFA | Lab bypass account or TOTP seed in vault for scanner only |
| API keys | Scoped non-prod keys |

## Workflow

### 1. Confirm RoE and roles

1. Environments, rate limits, excluded paths (`/logout`, payment capture, delete-all).
2. Roles: `user`, `admin`, `tenant-A` vs `tenant-B` for IDOR-oriented crawls.
3. Success: authenticated crawl coverage metrics; actionable findings with repro; no prod Sev-1 from scanner.

### 2. Provision scanner identities

1. Dedicated users; no shared human passwords in clear chat.
2. Least privilege still covering target features.
3. Vault storage for secrets; CI OIDC if possible.

### 3. Session acquisition (ZAP example concepts)

```text
1. Open context → authentication → form-based / script
2. Login URL + username/password params
3. Verification URL regex logged-in indicator
4. Forced user mode for spider/ascan
```

```bash
# Headless tooling examples vary; conceptual:
# zap-cli or Automation Framework yaml with env-injected secrets
```

Burp: recorded login macro + session handling rules; re-login on idle.

### 4. Crawl then scan

1. **Spider/crawl** authenticated first; review site tree for missed mounts.
2. Exclude logout and token revocation endpoints.
3. Active scan policy: start passive+safe; enable injection plugins where RoE allows.
4. Multi-context: repeat for each role; compare admin-only surfaces.

### 5. Multi-tenant checks

1. Crawl as tenant A; attempt object IDs from tenant B in scanner or manual follow-up.
2. DAST alone may miss logic IDOR — schedule manual/API tests.

### 6. Triage

| Finding | Action |
| --- | --- |
| Missing auth on URL | Verify with curl without cookie |
| XSS/SQLi alerts | Manual confirm; reduce duplicates |
| CSRF | Confirm cookie auth + missing token |
| Low info banners | Batch or accept |

Export reports redacting session tokens.

### 7. CI integration

```yaml
# Conceptual job
- name: dast-auth
  env:
    DAST_USER: ${{ secrets.DAST_USER }}
    DAST_PASS: ${{ secrets.DAST_PASS }}
  run: ./scripts/run-zap-auth.sh
```

1. Run on ephemeral review apps.
2. Fail gate on high confidence medium+ after allowlist of known issues.
3. Refresh auth when login UX changes (treat auth script as code).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | Verified logged-in crawl | Scanner thinks it is authed but sees login page |
| Prod | Limited policy + window | Full aggressive ascan on prod Friday |
| Secrets | Vault / CI secrets | Password in repo script |
| Roles | Separate contexts | Single admin scan only |
| Coverage | Review site map | Trust “100% complete” blindly |

## Output Checklist

- [ ] RoE/exclusions documented
- [ ] Scanner users provisioned
- [ ] Auth verification URL works
- [ ] Logout excluded
- [ ] Crawl coverage reviewed per role
- [ ] Scan policy matches environment
- [ ] Findings triaged with repro
- [ ] Tokens redacted in exports
- [ ] Auth scripts versioned
- [ ] Residual unauthenticated surface noted

## Rules

- Authenticated DAST multiplies impact of misconfiguration — stay in scope.
- Confirm session liveness throughout the run.
- Focus on **authenticated DAST setup and triage**.
