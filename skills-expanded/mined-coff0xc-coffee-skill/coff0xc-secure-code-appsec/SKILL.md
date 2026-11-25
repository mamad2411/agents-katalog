---
name: coff0xc-secure-code-appsec
description: "Use when the user requests code/AppSec audit: source/sink, taint, Web/API/GraphQL/OAuth, CSP/CORS/Cookie, LLM prompt injection, access control/authorization bypass, SSRF/XSS/SQLi, backdoor/Webshell, security regression. Authorized scope only. Manual trigger: Use coff0xc-secure-code-appsec."
---

# coff0xc-secure-code-appsec

<!-- skill-id: cs-sca-3d9e7a54 -->

## Quick Rules (read this first for everyday tasks)
> **[Entry points first]** First find entry points, authentication/authorization boundaries, source/sink, trust boundaries, and dangerous functions.
> **[Evidence gate]** Every finding must have file/line number, call chain, impact, trigger conditions, and remediation recommendations.
> **[Fix loop]** Prefer minimal patches and regression tests; do not write unreproduced guesses as confirmed vulnerabilities.
> **[Hard boundary]** Confirm first for unauthorized targets, real attack chains, credential abuse, persistence, data exfiltration, and production validation.

Follow this section first for ordinary code-security audits; expand the full workflow only for large-scale variant analysis, patch validation, or launch security gates.

## Capability
Evidence-based audit capability for code and application security. It turns source code, routes, configuration, scan results, and logs into verifiable findings, remediation recommendations, and regression checks.

## What It Can Deliver
- Security finding list: location, impact, evidence, reproduction conditions
- source/sink or permission-chain explanations
- Remediation recommendations, test cases, detection/logging recommendations
- False-positive judgments and residual risk

## What Input It Can Take
- Source repos, routes/controllers/resolvers, auth middleware
- Burp projects, SARIF, scan results, logs, configuration
- Vulnerability leads, authorization-bypass symptoms, prompt-injection or backdoor suspicions

## Safe-Use Boundaries
- Handle only owned or explicitly authorized assets, local code, and defensive work
- Do not provide unauthorized exploitation, credential acquisition, persistence, detection evasion, or exfiltration steps
- Active scanning, authentication-bypass testing, and external callbacks must have their authorization scope confirmed first
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Every finding must have code/configuration/log evidence
- Distinguishes verified, high-confidence, inferred, and unknown
- Security output includes the fix, detection, and validation loop by default

## Typical Usage
```text
Use coff0xc-secure-code-appsec to audit this Web/API project's authentication and authorization-bypass risks.
Use coff0xc-secure-code-appsec to look at source/sink, SSRF, XSS, SQLi, and backdoor signs.
Use coff0xc-secure-code-appsec to triage this SARIF report and remove false positives.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
