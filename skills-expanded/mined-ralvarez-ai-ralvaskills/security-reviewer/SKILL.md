---
name: security-reviewer
version: 1.1.1
description: Cross-language security review - injection, auth/authz, secrets, insecure defaults, deserialization, CSRF/SSRF/IDOR, dep vulns. Emits a Critical/High/Medium/Low report with file:line + fixes. Use when auditing a PR or pre-release.
---

# Security Reviewer

Reviews code for security issues before they reach production. This skill catches the issues that architect skills already encode rules against; it's the safety net. Findings table, severity rubric, and tooling reference in [RECIPES.md](RECIPES.md).

## 1. When to invoke

- User asks "review this for security", "audit", "is this safe", "any security issues".
- Pre-release review of a service touching auth, payments, PII, or external integration.
- After dependency updates that include security advisories.
- New endpoint, new auth flow, new SQL query - anything where the failure mode is "data leaks" or "user gets owned".

## 2. Output format

Structured findings report - one row per finding with severity, rule, location, evidence, and fix. Layout + severity rubric + closing summary in [RECIPES § 1-2](RECIPES.md#1-findings-report-format).

## 3. Review approach

Two passes:

1. **Tool pass** - run static analyzers, then read their output. They catch low-hanging fruit fast.
2. **Read pass** - read the actual diff (or files in scope), checking the categories in §4. Tools miss intent; the read pass finds most real issues.

## 4. What to check - by category

### Injection

- **SQL injection.** Per [sql-architect §4](../../databases/sql-architect/SKILL.md#4-query-patterns) and [§8](../../databases/sql-architect/SKILL.md#8-security): every query uses parameter binding. Grep for f-strings, format-strings, concatenation in SQL. `WHERE id = '${userId}'` is a fail; `WHERE id = $1` is a pass.
- **Command injection.** Any `subprocess.run(..., shell=True)`, `os.system`, `exec.Command("sh", "-c", userInput)`. Use list-form args.
- **Template injection.** `Jinja2(autoescape=False)` or `html/template` bypassed via `template.HTML(userInput)`.
- **LDAP / NoSQL / regex injection.** Anything that builds a query from user input without escaping is a candidate.

### Auth & authz

- **Per [rest-api-architect §11](../../protocols/rest-api-architect/SKILL.md#11-authentication-patterns)** - Pattern A (in-house JWT) or B (external IdP). Verify implementation matches.
- **Argon2id** for password hashing (not bcrypt, never MD5/SHA1).
- **JWT signing algorithm pinned** (`jwt.WithValidMethods([]string{"HS256"})` Go / `algorithms=["HS256"]` Python) - never `algorithms=["HS256", "none"]`, never accept the alg the token claims.
- **`aud` and `iss` verified** for external IdP tokens.
- **Tokens not in URLs**, only in `Authorization: Bearer` headers.
- **401 vs 403** distinction maintained.
- **No tenant-id from request body**; derive from authenticated context. `customer_id` in a JSON payload is a take-over vector.
- **Authorization checked per endpoint**, not assumed by middleware. Per [fastapi-architect §6](../../frameworks/fastapi-architect/SKILL.md#6-authentication--authorization) / [gin-architect §7](../../frameworks/gin-architect/SKILL.md#7-authentication--authorization) / [nethttp-architect §8](../../frameworks/nethttp-architect/SKILL.md#8-authentication--authorization): scopes/roles enforced per-route.

### Secrets

- **No secrets in code.** Run `gitleaks` over the diff + the whole history.
- **No secrets in env files committed to git.** Only `.env.local` (gitignored) holds secrets.
- **No secrets in Dockerfile layers.** Per [docker-architect §4](../../infra/docker-architect/SKILL.md#4-image-security): build-time secrets via `--mount=type=secret`; runtime via orchestrator.
- **No secrets in logs.** Per [observability-architect §7](../../infra/observability-architect/SKILL.md#7-what-not-to-emit): redaction filters configured.
- **Rotation.** If a secret was ever committed, rotate it - even if "we removed it later". Git history is forever.

### Insecure defaults

- **CORS:** never `Access-Control-Allow-Origin: *` for authenticated endpoints. Explicit allow-list.
- **HTTPS only.** Reject plaintext at the load balancer / `Strict-Transport-Security` header set.
- **Security headers** present: `X-Content-Type-Options: nosniff`, `Content-Security-Policy` (for HTML), `Referrer-Policy: no-referrer`.
- **Cookies:** `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict` where compatible).
- **Default-deny in IAM.** Roles grant specific permissions; nothing is "allow all" except the operator break-glass account.
- **Container runs as non-root** (per [docker-architect §1](../../infra/docker-architect/SKILL.md#1-dockerfile-fundamentals)).

### Deserialization and parsing

- **No `pickle.loads` on untrusted data.** Python's `pickle` is RCE-by-design.
- **No `yaml.load(s)` - use `yaml.safe_load(s)`.**
- **JSON: strict** - `json.NewDecoder(r.Body).DisallowUnknownFields()` (Go), `model_config = ConfigDict(extra="forbid")` (Pydantic).
- **XML: disable external entities** (XXE) - `defusedxml` (Python) or `xml.disable_external_entities` style config.

### CSRF, SSRF, IDOR

- **CSRF:** for cookie-authenticated browser endpoints, double-submit token or SameSite=Strict cookies. Bearer-token APIs don't need CSRF protection.
- **SSRF:** outbound HTTP from server-side code that takes a user-supplied URL must validate - block private IP ranges (`10.0.0.0/8`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.169.254` AWS metadata), enforce HTTPS, restrict to an allow-list.
- **IDOR (insecure direct object reference):** every resource lookup checks ownership. `GET /v1/orders/{id}` returns 404 if the order isn't the caller's, *not* 403 (don't leak existence).

### Rate limiting and abuse

- **Rate limit at the edge** (gateway / CDN / WAF) plus per-endpoint critical-path limits.
- **Per-caller**, not per-IP - IPs are unreliable identity.
- **Login endpoints rate-limited aggressively** to prevent credential stuffing. Lock the account after N failures within a window.
- **Account enumeration:** signup/login error messages don't disclose whether a user exists. "Invalid credentials" - not "user not found".

### Dependency hygiene

- **`trivy image` + `trivy fs`** in CI per [docker-architect §10](../../infra/docker-architect/SKILL.md#10-vulnerability-scanning--trivy). Fail on HIGH/CRITICAL.
- **Renovate-managed updates** per [repo-tooling-architect §7](../../tooling/repo-tooling-architect/SKILL.md#7-dependency-updates--renovate-default-dependabot-acceptable). Security updates land immediately.
- **Lockfiles committed.** `go.sum`, `uv.lock`, `package-lock.json` - never edit by hand.
- **No `:latest` tags** in Dockerfiles. Digest-pin in production.

## 5. Tooling

`gitleaks`, `semgrep`, `gosec`, `bandit`, `trivy`, `npm audit` / `pip-audit` - full reference + when each catches what + where to wire them in [RECIPES § 3](RECIPES.md#3-tooling-reference).

## 6. What this skill does NOT do

- **Penetration testing.** Black-box attack simulation against a running service is a different skill set and requires explicit authorization.
- **Threat modeling.** Architecture-level "what attacker types can affect this system" lives in [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md) territory or a dedicated workshop.
- **Compliance audit.** SOC 2 / HIPAA / PCI-DSS specifics need a compliance specialist.

This skill stops at code- and configuration-level findings. Findings that imply deeper work flag that explicitly: *"recommendation: full threat-model session with the team that owns Payments."*

## 7. Cross-skill ties

- [rest-api-architect §10-11](../../protocols/rest-api-architect/SKILL.md#10-auth--security-headers) - REST security conventions reviewers verify against.
- [sql-architect §4 & §8](../../databases/sql-architect/SKILL.md#4-query-patterns) - parameter binding, RLS for multi-tenancy.
- [docker-architect §4 & §10](../../infra/docker-architect/SKILL.md#4-image-security) - image security baseline + Trivy scanning.
- [observability-architect §7](../../infra/observability-architect/SKILL.md#7-what-not-to-emit) - PII / secret redaction in signals.
- [repo-tooling-architect §5 & §7](../../tooling/repo-tooling-architect/SKILL.md#5-pre-commit-hooks--minimal-opt-in) - gitleaks in pre-commit, Renovate for security updates.
- [commit-author](../../workflows/commit-author/SKILL.md) - security fix commits use `fix(scope): ...` with `BREAKING CHANGE` footer if API behavior changes.
