---
name: tpl-situacao-analise-dependencias
description: Template do pack (situacao/13-analise-dependencias.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/13-analise-dependencias.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Dependency Analysis & Vulnerability Remediation

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/13-analise-dependencias.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when auditing project dependencies — checking for security vulnerabilities, outdated packages, license compliance issues, or evaluating whether to replace a dependency. This is triggered by: a Dependabot/Renovate alert, a pre-release security audit, CVE disclosure in a package you use, or periodic quarterly dependency health checks.

## OBJECTIVES
- Identify and remediate all Critical and High severity CVEs
- Establish a systematic update strategy to prevent future accumulation
- Verify license compliance for production dependencies
- Evaluate oversized or abandoned dependencies for replacement
- Document decisions for each significant dependency change

## APPROACH RULES

1. **Triage by severity, not by count.** 100 Low severity advisories matter less than one Critical. Use CVSS score as the primary triage signal. Focus time on CVSS ≥ 7.0.

2. **Understand the vulnerability before patching.** Read the CVE/advisory. Understand the attack vector. Is your application actually vulnerable? (e.g., a server-side template injection vulnerability in a package you use for string parsing offline has zero network exposure.)

3. **Patch before minor before major.** For a dependency at v3.2.1: patch (v3.2.x) is almost always safe. Minor (v3.x.0) is usually safe with a changelog read. Major (vX.0.0) requires a migration guide and testing.

4. **Lock files are authoritative.** `package-lock.json`, `Pipfile.lock`, `go.sum`, `Cargo.lock` must be committed. They are the specification of exactly what runs in production. Never gitignore them.

5. **Never force-override a version without understanding why the constraint exists.** If upgrading packageA forces packageB to downgrade, investigate the conflict before using `--force` or `--legacy-peer-deps`.

6. **Abandoned dependencies are time bombs.** A package with zero commits in 24+ months and no stated maintenance status is a liability. Evaluate replacement or internalization.

7. **Transitive dependencies also scope production risk.** A vulnerability in a transitive dependency (a dependency of a dependency) may still affect you. Check if the vulnerable code path is actually reachable from your usage.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| CVSS ≥ 9.0 (Critical) | Fix immediately, same day. Stop other work. Create hotfix branch. |
| CVSS 7.0-8.9 (High) | Fix within current sprint. Cannot ship new releases without fixing. |
| CVSS 4.0-6.9 (Medium) | Fix within 30 days. Schedule in next sprint. |
| CVSS < 4.0 (Low/Info) | Fix in next quarterly dependency update. Do not urgently interrupt work. |
| Vulnerability in dev-only dependency | Lower priority — not in production build. Still fix, but after production vulnerabilities. |
| No patch available yet | Apply mitigations (firewall rule, input validation, feature flag). Add to monitoring. Watch for patch. |
| Major version upgrade required | Read migration guide. Create a separate migration branch. Test thoroughly. Allocate 2× normal time. |
| Package abandoned (no commits 2+ years) | Evaluate: fork + maintain, replace with alternative, internalize the functionality. |
| Conflicting peer dependency versions | Resolve the conflict — do not use `--force`. Understand why the conflict exists. |
| License changed in new version | Legal review required. GPL in a commercial product is a serious issue. Do not blindly update. |

## Audit Commands by Ecosystem

```bash
# Node.js
npm audit
npm audit --json > audit-report.json
npx better-npm-audit audit  # More readable output

# Python
pip install pip-audit
pip-audit
pip-audit --output-format json > audit-report.json

# Rust
cargo audit

# Go
govulncheck ./...

# PHP
composer audit

# Docker images
docker scout cves [image:tag]

# Multi-ecosystem (CI)
npx snyk test
```

## CVSS Score Interpretation

| Score | Severity | Response SLA | Example |
|-------|----------|-------------|---------|
| 9.0-10.0 | Critical | Same day | Remote code execution, no auth required |
| 7.0-8.9 | High | Current sprint | SQL injection with auth bypass |
| 4.0-6.9 | Medium | 30 days | SSRF requiring authenticated user |
| 0.1-3.9 | Low | Quarterly | Info disclosure of non-sensitive data |
| 0.0 | None/Info | Quarterly schedule | Version disclosure only |

## Update Strategy by Type

```
patch update (1.2.3 → 1.2.4):
  - High confidence safe to merge
  - Read changelog for anything unusual
  - Run existing tests
  - Time: 15 minutes

minor update (1.2.x → 1.3.0):
  - Generally safe but check changelog for deprecations
  - Look for new required configuration
  - Run full test suite
  - Time: 30-60 minutes

major update (1.x.x → 2.0.0):
  - Read migration guide fully before starting
  - Check for breaking API changes in your usage
  - May require code changes
  - Create dedicated branch
  - Time: 1-4 hours (or more)
```

## License Compliance

Common license compatibility rules for commercial software:

| License | Can Use in Closed Source? | Requires Attribution? | Copyleft (must open-source your code)? |
|---------|--------------------------|----------------------|---------------------------------------|
| MIT | ✅ Yes | ✅ Yes (easy) | ❌ No |
| Apache 2.0 | ✅ Yes | ✅ Yes | ❌ No |
| BSD 2/3-Clause | ✅ Yes | ✅ Yes | ❌ No |
| LGPL | ⚠️ Conditional | ✅ Yes | ⚠️ Only if modified |
| GPL v2/v3 | ❌ No | — | ✅ Yes — forces open source |
| AGPL | ❌ No | — | ✅ Yes — includes network use |
| CC BY | ⚠️ Check by version | ✅ Yes | Varies |

## DO NOT

- **DO NOT** run `npm audit fix --force` blindly — it can downgrade major versions and break things
- **DO NOT** ignore vulnerability in dev-only dependencies in public repos — they affect contributors
- **DO NOT** update all dependencies at once — changes cannot be isolated if something breaks
- **DO NOT** assume a vulnerability doesn't affect you without verifying the attack vector
- **DO NOT** merge dependency updates without running the full test suite
- **DO NOT** use `--legacy-peer-deps` or `--force` as a regular practice — it hides incompatibilities
- **DO NOT** ignore license changes when updating major versions of dependencies

## OUTPUT FORMAT

For each audit, produce a **Dependency Report**:

```markdown
## Dependency Audit Report

**Date:** 2024-01-15
**Project:** [name]
**Tool:** npm audit + Snyk

### Summary
| Severity | Count | Action Required |
|----------|-------|----------------|
| Critical | 1 | Fix immediately |
| High | 3 | Fix this sprint |
| Medium | 7 | Schedule next sprint |
| Low | 14 | Quarterly sweep |

### Critical Findings
#### [CVE-2024-XXXXX] — lodash ReDoS via template()
- Package: lodash@4.17.20
- CVSS: 9.8
- Attack: Input via template engine causes catastrophic backtracking
- Affected: Yes — we use lodash.template() in email generation
- Fix: Upgrade to lodash@4.17.21
- PR: #456

### Update Log
| Package | Old Version | New Version | Type | Notes |
|---------|-------------|-------------|------|-------|
| lodash | 4.17.20 | 4.17.21 | patch | CVE fix |
| typescript | 5.2.0 | 5.3.3 | minor | No breaking changes |
```

## QUALITY GATES

- [ ] Zero CVSS ≥ 7.0 vulnerabilities in production dependencies
- [ ] All vulnerabilities documented with CVE ID, affected code path, and fix
- [ ] Lock file updated and committed after any dependency change
- [ ] Full test suite passes after updates
- [ ] License audit: no GPL/AGPL in production dependencies (unless explicitly cleared)
- [ ] No abandoned dependencies (last commit > 24 months) with alternatives available
- [ ] Renovate/Dependabot configured to prevent future accumulation
- [ ] Audit runbook documented so next run takes < 1 hour
