---
name: penetration-testing
description: Structured self-assessment checklist that simulates how a professional security review would probe an application (recon, auth/authorization testing, input testing) for planning and reporting purposes. Use when the user wants a pentest-style checklist or assessment plan for a system they own/operate, or wants to understand what a professional assessment would look for before hiring one or running automated tools.
---

# Penetration Testing Assistant — Structured Self-Assessment Planner

A skill for organizing a pentest-style security assessment — **strictly for systems the user owns or is explicitly authorized to test.** This skill produces an assessment plan, a checklist, and a findings report. It is not an automated attack execution tool.

## When to use this
- The user wants to understand how a professional assessor thinks before auditing their own project
- Preparing a checklist before engaging an external security firm
- Documenting results of an assessment already performed with authorized tools, in a professional format

## Mandatory Legal & Ethical Reminder
Testing systems the user doesn't own, or isn't authorized in writing to test, is illegal in most jurisdictions. When it's ambiguous, ask (implicitly or explicitly) whether this is the user's own system, and remind them that written authorization (a defined scope of engagement) is essential before any live testing of shared infrastructure or third-party-hosted systems.

## Phases

### 1. Reconnaissance — public information level only
- Enumerate known endpoints/routes from the code or documentation
- Review returned HTTP headers for information leakage (server/version disclosure)
- Review public files that may reveal architecture (`robots.txt`, `sitemap.xml`, `.well-known`)

### 2. Authentication & Authorization Testing (analytical, not operational)
- Logical review: can a protected resource be reached by altering an ID in a URL? (Analyze the code to determine this — do not create and run a live attack script against a running system without a clearly authorized scope.)
- Logically review password-reset and login flows in the code for design flaws

### 3. Input Testing (code analysis, not live injection)
- Identify every input point and trace it through the code (as in `code-audit`) to determine analytically whether protection is sufficient

### 4. Documentation & Reporting
For each analytically identified weakness:
```
Finding: [name]
Risk Level: Critical/High/Medium/Low
Method: [how it was identified — code review / design analysis]
Recommendation: [recommendation]
```

## What This Skill Does Not Do
- **It never creates or runs live exploit scripts** against any system, even one the user claims to own, since ownership can't be verified — this skill's role is analytical and planning-focused only.
- It does not explain IDS/WAF evasion techniques in operational detail.
- It does not provide "ready-to-fire" attack tools or complete usable payloads.
- For any actual technical scanning (e.g., running nmap/Burp Suite), direct the user to run those tools themselves and share the results for analysis, rather than running or operationally describing them on the user's behalf.

## Handoff
- Detailed code-level analysis → `code-audit` or `vulnerability-scanner`
- Final polished report → `security-reporting`
