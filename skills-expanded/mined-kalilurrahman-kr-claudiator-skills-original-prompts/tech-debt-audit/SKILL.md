---
name: tech-debt-audit
description: Analyze a codebase or component to identify technical debt, assess impact, and prioritize remediation. Outputs categorized debt items with ROI estimates.
argument-hint: [codebase area or component to audit]
allowed-tools: Read, Write, Bash
---

# Technical Debt Audit

Systematically identify, categorize, and prioritize technical debt in a codebase. Not a vague "code needs refactoring" — specific debt items with measurable impact and estimated remediation effort.

## Process

1. **Scope the audit.** Identify the component, service, or module being assessed.
2. **Scan for debt signals.** Long functions, high cyclomatic complexity, duplicated code, missing tests, deprecated dependencies.
3. **Use static analysis.** Run linters, complexity analyzers, security scanners (SonarQube, ESLint, Bandit).
4. **Categorize debt.** Code quality, performance, security, maintainability, scalability.
5. **Assess impact.** How does this debt slow development? Cause bugs? Increase risk?
6. **Estimate remediation.** Engineering days to fix, not story points.
7. **Calculate ROI.** Time saved (dev velocity) vs time invested.
8. **Prioritize.** High impact, low effort first. Critical security issues always top priority.

## Output Format

### Technical Debt Audit: [Component Name]

**Audited On:** [Date]  
**Scope:** [Specific files, modules, or services]  
**Total Debt Items:** 27  
**Estimated Remediation:** 38 engineering days  

---

## Executive Summary

**Critical Issues:** 3 (security vulnerabilities requiring immediate action)  
**High Impact Debt:** 8 items (blocking new features, causing production incidents)  
**Quick Wins:** 6 items (< 1 day each, high velocity improvement)  
**Recommended Priority:** Fix 3 critical security issues, then tackle 6 quick wins (7 days total).

---

## Debt Categories

### 1. Security Vulnerabilities (Critical)

#### [S1] SQL Injection in User Search
- **Location:** `api/search.py:45-62`
- **Issue:** Raw SQL query with string interpolation `f"SELECT * FROM users WHERE name = '{query}'"`
- **Impact:** Attackers can extract entire database, create admin accounts
- **Remediation:** Use parameterized queries `cursor.execute("SELECT * FROM users WHERE name = %s", [query])`
- **Effort:** 1 day (includes testing)
- **Priority:** P0 (Fix immediately)

#### [S2] Hardcoded AWS Credentials
- **Location:** `config/aws.py:12`
- **Issue:** `AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"` committed to repo
- **Impact:** Anyone with repo access can compromise AWS account
- **Remediation:** Move to environment variables, rotate keys, enable AWS Secrets Manager
- **Effort:** 0.5 days
- **Priority:** P0 (Fix immediately)

#### [S3] Missing Authentication on Admin Endpoints
- **Location:** `api/admin.py:78-120`
- **Issue:** `/admin/delete-user` endpoint has no auth decorator
- **Impact:** Anyone can delete user accounts
- **Remediation:** Add `@require_admin_auth` decorator
- **Effort:** 0.5 days
- **Priority:** P0 (Fix immediately)

---

### 2. Performance Issues (High Impact)

#### [P1] N+1 Query in Order List
- **Location:** `views/orders.py:34`
- **Issue:** Fetching related user for each order in loop (100+ queries for 100 orders)
- **Impact:** Order page takes 8s to load, times out under load
- **Remediation:** Use `select_related('user')` in initial query
- **Effort:** 0.5 days
- **ROI:** Page load drops from 8s to 0.3s, reduces DB load 99%
- **Priority:** P1

#### [P2] Missing Index on orders.user_id
- **Location:** Database schema
- **Issue:** `WHERE user_id = ?` queries do full table scan
- **Impact:** User order history query takes 2.5s (will worsen as data grows)
- **Remediation:** `CREATE INDEX idx_orders_user_id ON orders(user_id)`
- **Effort:** 0.25 days (includes testing on staging)
- **ROI:** Query drops from 2.5s to 0.05s
- **Priority:** P1

#### [P3] Uncompressed Images Served
- **Location:** Frontend build
- **Issue:** 5MB product images served without compression
- **Impact:** Page load on mobile takes 15s, 60% bounce rate
- **Remediation:** Add image optimization pipeline (WebP, responsive sizes)
- **Effort:** 2 days
- **ROI:** Page load drops to 3s, estimated 20% bounce rate reduction
- **Priority:** P1

---

### 3. Code Quality (Maintainability)

#### [C1] 800-Line God Function
- **Location:** `services/order_processor.py:process_order()`
- **Issue:** Single function handles validation, payment, inventory, email, logging
- **Impact:** Cannot test individual steps, bug fixes break unrelated features
- **Remediation:** Extract to 6 smaller functions (validate, charge, reserve_inventory, send_email, log, handle_errors)
- **Effort:** 3 days
- **ROI:** Reduces bug introduction rate, enables unit testing each step
- **Priority:** P2

#### [C2] Duplicated Validation Logic
- **Location:** `api/users.py`, `api/auth.py`, `api/profile.py` (3 files)
- **Issue:** Email validation regex copied across 3 files with slight differences
- **Impact:** Bug fixes require changing 3 places, inconsistent validation
- **Remediation:** Extract to `validators.py:validate_email()`
- **Effort:** 0.5 days
- **ROI:** Single source of truth, consistent behavior
- **Priority:** P2 (Quick Win)

#### [C3] No Unit Tests for Payment Logic
- **Location:** `services/payment.py`
- **Issue:** 0% test coverage on payment processing (300 lines)
- **Impact:** Cannot safely refactor, production bugs caught by customers
- **Remediation:** Add unit tests for charge, refund, webhook handling
- **Effort:** 4 days
- **ROI:** Prevents production payment bugs (cost: customer trust, refund overhead)
- **Priority:** P1

---

### 4. Dependency Debt

#### [D1] Django 2.2 (EOL)
- **Location:** `requirements.txt`
- **Issue:** Django 2.2 end-of-life April 2022, no security patches
- **Impact:** Known CVEs (CVE-2023-XXXX), cannot use new features
- **Remediation:** Upgrade to Django 4.2 LTS
- **Effort:** 8 days (includes compatibility testing)
- **Priority:** P1

#### [D2] 14 Outdated NPM Packages
- **Location:** `package.json`
- **Issue:** React 16 (current: 18), Webpack 4 (current: 5), etc.
- **Impact:** Missing performance improvements, security patches
- **Remediation:** Upgrade packages incrementally, test after each
- **Effort:** 5 days
- **Priority:** P2

---

### 5. Scalability Issues

#### [SC1] Session Data in Database
- **Location:** `auth/sessions.py`
- **Issue:** Session tokens stored in PostgreSQL, queried on every request
- **Impact:** Database bottleneck at 1000+ concurrent users
- **Remediation:** Move to Redis for session storage
- **Effort:** 3 days
- **ROI:** Reduces DB load 30%, supports 10x more concurrent users
- **Priority:** P2 (defer until traffic grows)

---

## Prioritization Matrix

| ID | Issue | Impact | Effort | ROI | Priority |
|----|-------|--------|--------|-----|----------|
| S1 | SQL Injection | Critical | 1d | ∞ | P0 |
| S2 | Hardcoded Keys | Critical | 0.5d | ∞ | P0 |
| S3 | Missing Auth | Critical | 0.5d | ∞ | P0 |
| P1 | N+1 Query | High | 0.5d | Very High | P1 |
| P2 | Missing Index | High | 0.25d | Very High | P1 |
| C2 | Duplicated Validation | Medium | 0.5d | Medium | P2 (Quick Win) |
| D1 | Django EOL | High | 8d | High | P1 |
| C3 | No Payment Tests | High | 4d | High | P1 |

**Total P0:** 2 days  
**Total P1:** 14.75 days  
**Quick Wins (< 1 day, high ROI):** 1.75 days  

---

## Recommended Remediation Plan

### Sprint 1 (Week 1): Critical Security
- Fix S1, S2, S3 (2 days)
- Add monitoring for admin endpoint access

### Sprint 2 (Week 2): Quick Wins + High Impact
- P1, P2 (0.75 days) — Performance fixes
- C2 (0.5 days) — Deduplicate validation
- Start C3 (payment tests) — 4 days

### Sprint 3 (Week 3-4): Framework Upgrade
- D1 (Django upgrade) — 8 days
- Regression testing

## Rules

- Every debt item must have a specific file location, not just "authentication system."
- Impact must be measurable: page load time, error rate, dev velocity, security risk.
- Effort must be in engineering days, not vague "small/medium/large."
- Security vulnerabilities are always P0 regardless of effort.
- ROI = (time saved per month × 12) / remediation effort. If ROI > 2, prioritize higher.
- Quick wins are < 1 day effort with measurable improvement — do these first to build momentum.
- If audit scope is large (entire codebase), focus on highest-traffic or highest-risk areas first.
- Use automated tools (linters, complexity analyzers) to find debt, then manually verify and categorize.
- Include at least one "defer" item — not all debt needs fixing now.
