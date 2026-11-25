# Security Audit — Proactive Vulnerability Scanning

## When to Use
- Before deploying to production
- After integrating AI-generated code (Claude can introduce subtle vulnerabilities)
- Periodic security reviews (quarterly minimum)
- When integrating third-party dependencies
- After any authentication or authorization changes

## Core Principle
Proactively scan for threats using structured checklists. Use Claude for deep code analysis, but confirm findings with tools and manual review. Prevention over reaction.

## Process
1. **Scope the audit** — Define boundaries (full app or specific modules). Have Claude generate a customized vulnerability checklist.
2. **Static analysis** — Run SAST tools (Snyk, Bandit, ESLint security plugins). Have Claude review and prioritize findings by severity.
3. **Dependency check** — Audit all dependencies for known CVEs. Use Claude to assess risk of each.
4. **Manual review** — Deep-dive into high-risk areas: auth, crypto, input handling, API endpoints. Use Claude for code walkthroughs.
5. **Remediate and verify** — Apply fixes, re-run tools, confirm issues are resolved.
6. **Document findings** — Create a vulnerability report with risk scores and remediation status.

## Output Format
- Vulnerability report (issue, severity, fix, status)
- Remediation plan with code snippets
- Risk score (overall rating)
- Preventive measures added

## Rules
- Follow OWASP Top 10 as minimum baseline.
- Audit dependencies as rigorously as custom code.
- Claude analyzes, tools and humans confirm.
- Schedule recurring audits — vulnerabilities evolve.
- Never skip auth/crypto review, even if "nothing changed."

## Anti-Patterns
- Treating audits as one-time events
- Dismissing low-severity issues (they chain into exploits)
- Over-relying on automated tools without manual context review
- Auditing in isolation without team input
- Trusting AI-generated code is "probably secure"
