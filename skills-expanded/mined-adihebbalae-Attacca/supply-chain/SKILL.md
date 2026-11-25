---
name: supply-chain
description: "4-gate supply chain security checklist. Prevents malicious packages, typosquatting, and abandoned projects. Use before adding any dependency to production. Can run standalone."
---

<!-- Delete when: native Claude Code package provenance verification with automated typosquatting detection is available -->

# Supply Chain Security Skill

4-gate defense against malicious packages, typosquats, and supply chain attacks. Use before adding ANY dependency to production.

---

## The 4 Gates

### Gate 1: Verify Package Exists on Official Registry

```bash
# Node.js
npm view [package-name] versions --json | tail -5

# Python
pip index versions [package-name]

# Go
go list -m [module-path]@latest

# Ruby
gem list -r [gem-name]
```

**Reject if:**
- Package doesn't exist on registry
- Name has extra chars vs. well-known name (e.g., `Requests` vs `requests`)

---

### Gate 2: 30-Day Age Minimum

**REJECT packages published less than 30 days ago** unless it's a Z-version security patch.

Why: supply chain attacks exploit the window before security scanners catch malicious code.

```bash
# Node.js — check publication date
npm view [package-name] time.created

# Python — check first release date
curl -s https://pypi.org/pypi/[package-name]/json | jq '.releases | keys'
```

**Exception**: Security patches (X.Y.Z → X.Y.Z+1) can be approved immediately IF:
- Previous version has confirmed CVE
- Patch version fixes only that vulnerability
- All tests pass after upgrade

---

### Gate 3: Anti-Typosquatting Check

Compare name against well-known packages:

```bash
# Common typosquatting patterns:
#   lodash → 1odash (1 instead of L)
#   express → expres, expresss
#   react → raect, reeact
#   requests → reqeusts

npx package-name-check [package-name]  # Node.js
```

**Verify by checking:**
1. GitHub stars / open issues (active = legitimate)
2. Weekly download count (established = millions)
3. Maintainer: verified account, other projects, followers

---

### Gate 4: Maintainer Trust & CVE Check

```bash
# Check maintainer activity
npm view [package-name] maintainers
pip show [package-name]

# Check GitHub repo
# Red flags: account created recently, no activity, no followers, recent ownership transfer

# Check CVE database
# Go to: https://osv.dev and search [package-name]
```

**Ask:**
- Is maintainer account active?
- Any recent ownership transfers (high risk)?
- Do repo commits match published versions?
- Any HIGH/CRITICAL CVEs in current version?

---

## Gate 2 Decision Template

```markdown
## Dependency Review: [package-name]@[version]

- [ ] Registry: Found on official registry
- [ ] Age: Published ≥30 days ago (exception: security patch)
- [ ] Typosquatting: Name matches well-known package
- [ ] Maintainer: Active, verified account, recent commits
- [ ] CVE: No HIGH/CRITICAL vulnerabilities
- [ ] Alternative: No lower-risk option

VERDICT: ✅ APPROVE / ⚠️ WARN / ❌ REJECT
```

---

## Gate 3: Dependency Audit

Run before every push with dependency changes:

```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit

# Go
govulncheck ./...

# Ruby
bundle audit check --update
```

**Requirements:**
- Zero HIGH/CRITICAL vulnerabilities
- Lock file present and committed
- No packages added since Gate 2 approval

---

## Gate 4: SBOM + Lock File Integrity

If any dependency file changed (package.json, requirements.txt, go.mod, Gemfile):

### 4A: Generate SBOM

```bash
mkdir -p .attacca/sbom
syft . -o cyclonedx-json=.attacca/sbom/latest.json
```

### 4B: Review SBOM for Anomalies

```bash
# Check for unexpected packages
cat .attacca/sbom/latest.json | grep '"name"' | wc -l  # Total count

# Any packages you didn't approve? Reject.
# Any suspicious registries? Reject.
```

### 4C: Verify Lock File

```bash
# Node.js
npm ci --dry-run

# Python
pip install --require-hashes -r requirements.txt --dry-run

# Go
go mod verify

# Ruby
bundle install --frozen
```

**Lock file rules:**
- ✅ MUST be committed
- ✅ MUST match package manifest exactly
- ❌ Never in .gitignore
- ❌ Any tampering = FAIL review

---

## Gate 4 Report

```markdown
## Supply Chain Review

SBOM Generated: ✅ .attacca/sbom/latest.json (n packages)
Lock File Verified: ✅
Unexpected Packages: ✅ None
CVE Scan: ✅ Clean
Private Registries: ✅ Official registries only

VERDICT: ✅ SAFE TO PUSH / ❌ DO NOT PUSH
```

---

## Age Policy Reference

| Version bump | Age required | Example |
|--------------|--------------|---------|
| Major | ≥30 days | 1.0.0 → 2.0.0 |
| Minor | ≥30 days | 1.0.0 → 1.1.0 |
| Patch | ≥30 days | 1.0.0 → 1.0.1 |
| Security patch | Immediate | 1.0.4 → 1.0.5 (CVE fix) |

---

## Quick Gate Summary

| Gate | When | What | Stops |
|------|------|------|-------|
| 1 | Always | Verify on registry | Fake packages |
| 2 | Always | Age + typosquatting + maintainer | New packages, typosquats |
| 3 | Pre-push | Audit for CVEs | Vulnerable transitive deps |
| 4 | If deps changed | SBOM + lock file | Tampering, supply chain drift |

---

## Run Before Production Pushes

Include all 4 gates in your pre-push verification for any production deployment.
