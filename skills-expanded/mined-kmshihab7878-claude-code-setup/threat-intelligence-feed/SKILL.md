---
name: "threat-intelligence-feed"
description: "Automated CVE and threat intelligence aggregation, prioritization, and patch tracking for the Security department. Scans vulnerability databases, threat feeds, and dependency reports. Ranks threats by exploitability × impact, tracks patch SLAs, and feeds the security self-improvement loop. Use when scanning for vulnerabilities, triaging CVEs, tracking patch compliance, or running the security UAOP pipeline."
risk: low
tags: [security, vulnerability, threat-intel, compliance]
created: 2026-03-23
updated: 2026-03-23
---

# Threat Intelligence Feed — Security Intelligence Engine

Automated vulnerability discovery, prioritization, and patch lifecycle management. UAOP Stage 1 + Stage 5 for the Security department.

## When to use

- Daily CVE scanning and triage
- After a new CVE advisory is published
- Before releases — "are we exposed?"
- Quarterly security posture review
- When a dependency update is available

## When NOT to use

- Active incident response (use `production-monitoring` + `incident-responder`)
- Code-level security review (use `security-review`)
- Penetration testing (use `offensive-security`)

## Pipeline

### Step 1: Scan Sources

Collect threat data from available sources:

```
SCAN TARGETS:
  Dependencies:
    - Python: requirements.txt, pyproject.toml → check against OSV/NVD
    - Node: package.json, package-lock.json → check against npm audit
    - Docker: base images → check against Trivy DB
    - Terraform: provider versions → check against HashiCorp advisories

  Infrastructure:
    - AWS services in use → check against AWS security bulletins
    - Container images → Trivy scan results
    - IaC configs → Checkov/Semgrep findings

  External feeds (via WebSearch):
    - NIST NVD recent CVEs for our stack (Python, FastAPI, PostgreSQL, Redis, Next.js)
    - GitHub Security Advisories for our dependencies
    - OWASP updates relevant to our attack surface
```

**Tools:** WebSearch (CVE lookups), github MCP (security advisories), filesystem (scan configs)

### Step 2: Prioritize by Risk

```
RISK SCORE = Exploitability × Impact × Exposure

  Exploitability (1-10):
    10 = Public exploit available, trivial to execute
     7 = POC exists, requires some skill
     4 = Theoretical, no public exploit
     1 = Requires physical access or highly unlikely conditions

  Impact (1-10):
    10 = RCE, data breach, full system compromise
     7 = Privilege escalation, data exposure
     4 = DoS, information disclosure (non-sensitive)
     1 = Minor information leak, cosmetic

  Exposure (1-10):
    10 = Internet-facing, no auth required
     7 = Internet-facing, behind auth
     4 = Internal only, behind VPN
     1 = Development-only, not in production
```

### Step 3: Classify and Assign SLAs

| Tier | Risk Score | SLA | Action |
|------|-----------|-----|--------|
| CRITICAL | 700-1000 | Patch within 1 hour | Page oncall, emergency patch |
| HIGH | 400-699 | Patch within 24 hours | Create urgent PR, fast-track review |
| MEDIUM | 100-399 | Patch within 7 days | Add to sprint, normal review |
| LOW | 1-99 | Patch within 30 days | Backlog, batch with other updates |

### Step 4: Produce Threat Report

```markdown
# Threat Intelligence Report — [Date]

## Scan Summary
- Sources scanned: [N]
- New vulnerabilities found: [N]
- By severity: [N] CRITICAL, [N] HIGH, [N] MEDIUM, [N] LOW
- Overdue patches: [N]

## CRITICAL Findings (Action Required NOW)
| CVE | Component | Risk Score | Exploitability | Impact | SLA | Status |
|-----|-----------|-----------|---------------|--------|-----|--------|

## HIGH Findings (Action Required Within 24h)
[same format]

## Patch Compliance Dashboard
| Tier | Total | Patched On Time | Overdue | Compliance % |
|------|-------|----------------|---------|-------------|
| CRITICAL | [N] | [N] | [N] | [X]% |

## Dependency Health
| Package | Current | Latest | CVEs | Risk | Action |
|---------|---------|--------|------|------|--------|

## Trend (Last 30 Days)
| Metric | Last Month | This Month | Delta |
|--------|-----------|------------|-------|
| Mean Time to Patch (CRITICAL) | [X]h | [Y]h | [+/-Z]h |
| Vulnerability escape rate | [X]% | [Y]% | [+/-Z]% |
| False positive rate | [X]% | [Y]% | [+/-Z]% |
```

### Step 5: Self-Improvement Loop (UAOP Stage 5)

```
MEASURE:
  - Patch SLA compliance (% patched on time per tier)
  - False positive rate (threats flagged that weren't real)
  - Escape rate (vulnerabilities that reached production undetected)
  - MTTP trend (mean time to patch over time)

REINFORCE:
  - Scanning rules that caught real threats → increase priority
  - Sources with high false positive rates → reduce weight or filter
  - Components with recurring vulnerabilities → flag for replacement

REGENERATE:
  - Update scanning scope based on new components/dependencies
  - Adjust risk scoring weights based on actual exploit attempts
  - Feed findings into security/rules.md for policy updates
```

## Cadence

```
DAILY:   Automated dependency scan (Trivy, npm audit)
WEEKLY:  Full threat report with CVE triage
MONTHLY: Security posture review + trend analysis
QUARTERLY: Comprehensive audit + policy review
```

## Agents

| Agent | Role |
|-------|------|
| security-engineer (L2) | Owns threat triage, sets patch priorities |
| security-auditor (L3) | Executes scans, analyzes findings |
| compliance-officer (L3) | Tracks SLA compliance, generates evidence |
| legal-compliance-checker (L5) | Validates regulatory alignment |

## Tools

| Tool | Purpose |
|------|---------|
| WebSearch | CVE database lookups, threat feed scanning |
| github MCP | Security advisory monitoring, dependency alerts |
| filesystem MCP | Read dependency files, scan configs |
| sequential MCP | Multi-step risk analysis and prioritization |
| memory MCP | Store threat patterns, track historical data |
