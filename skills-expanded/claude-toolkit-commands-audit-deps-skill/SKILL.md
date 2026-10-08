---
name: audit-deps
description: Scan project dependencies for outdated packages, known security vulnerabilities, and license issues. Trigger when the user asks to audit dependencies, check for vulnerabilities, review outdated packages, or says things like "are my deps up to date", "check for CVEs", "audit my packages", "/audit-deps", "scan for vulnerabilities", "should I update anything", or "dependency health check". Also trigger when the user mentions upgrading or updating dependencies and wants guidance on what to prioritize.
---

# Audit Dependencies

Scan `package.json`, `pyproject.toml`, `requirements.txt`, and lock files for outdated packages, known CVEs, and license concerns. Produces a prioritized upgrade plan with risk assessment and estimated effort.

## Trigger Examples

- "/audit-deps"
- "Are my dependencies up to date?"
- "Check for security vulnerabilities in my project"
- "Audit my packages"
- "What should I upgrade first?"
- "Dependency health check"

## Inputs

- **Project path** (optional, default: current working directory) — path to the project root
- **Scope** (optional, default: `all`) — one of:
  - `all` — Check everything: outdated, security, licenses
  - `security` — CVEs and known vulnerabilities only
  - `outdated` — Version freshness only
  - `licenses` — License compatibility only
- **Strictness** (optional, default: `standard`) — one of:
  - `relaxed` — Only flag critical CVEs and major version lags
  - `standard` — Flag high/critical CVEs, packages >1 major version behind, copyleft licenses
  - `strict` — Flag all CVEs, any outdated package, any non-permissive license

---

## Workflow

### Step 1: Discover Dependency Files

Scan the project root for dependency manifests:

```bash
# Find all dependency files
find . -maxdepth 3 \( \
  -name "package.json" \
  -o -name "package-lock.json" \
  -o -name "yarn.lock" \
  -o -name "pyproject.toml" \
  -o -name "requirements.txt" \
  -o -name "requirements*.txt" \
  -o -name "Pipfile" \
  -o -name "uv.lock" \
  -o -name "poetry.lock" \
\) -not -path "*/node_modules/*"
```

Report what was found and note any missing lock files (a finding in itself).

### Step 2: Check for Outdated Packages

#### JavaScript/TypeScript

```bash
# Check outdated packages
npm outdated --json 2>/dev/null || true

# Or if yarn
yarn outdated --json 2>/dev/null || true
```

#### Python

```bash
# Using pip
pip list --outdated --format=json 2>/dev/null || true

# Or parse pyproject.toml and check PyPI API
# For each dependency, fetch https://pypi.org/pypi/{package}/json
```

For each outdated package, determine:
- **Current version** installed
- **Latest version** available
- **Version delta** — patch, minor, or major behind
- **Changelog highlights** — what changed between current and latest (search web if needed)
- **Breaking change risk** — does the upgrade cross a major version boundary?

### Step 3: Security Vulnerability Scan

#### JavaScript

```bash
# npm audit
npm audit --json 2>/dev/null || true

# Check against GitHub Advisory Database via web search
```

#### Python

```bash
# pip-audit if available
pip-audit --format=json 2>/dev/null || true

# Or search web for CVEs against each dependency
```

For each vulnerability found:
- **CVE ID** and description
- **Severity** (Critical / High / Medium / Low)
- **Affected versions** vs installed version
- **Fixed in version** — is a patch available?
- **Exploitability** — is this reachable in the project's usage pattern?
- **CVSS score** if available

### Step 4: License Analysis

Parse each dependency and its transitive dependencies for license information:

```bash
# JavaScript
npx license-checker --json 2>/dev/null || true

# Python - check PyPI metadata
```

Flag licenses based on strictness level:

| License | Relaxed | Standard | Strict |
|---------|---------|----------|--------|
| MIT, BSD, ISC, Apache 2.0 | ✅ | ✅ | ✅ |
| MPL 2.0 | ✅ | 🟡 | 🟡 |
| LGPL | ✅ | 🟡 | 🔴 |
| GPL v2/v3 | 🟡 | 🔴 | 🔴 |
| AGPL | 🔴 | 🔴 | 🔴 |
| SSPL, BSL, Elastic | 🟡 | 🔴 | 🔴 |
| Unknown / No License | 🔴 | 🔴 | 🔴 |
| Custom / Proprietary | 🔴 | 🔴 | 🔴 |

### Step 5: Generate Report

```markdown
# Dependency Audit Report

**Project:** [name]
**Scanned:** [date]
**Files analyzed:** [list of dependency files found]

## Summary Dashboard

| Category | Status | Count |
|----------|--------|-------|
| 🔴 Critical vulnerabilities | [count] | [packages] |
| 🟠 High vulnerabilities | [count] | [packages] |
| 📦 Major version behind | [count] | [packages] |
| 📦 Minor version behind | [count] | [packages] |
| ⚖️ License concerns | [count] | [packages] |
| ✅ Up to date & clean | [count] | [packages] |

**Overall health:** [🟢 Healthy / 🟡 Needs Attention / 🔴 Action Required]

---

## 🔒 Security Vulnerabilities

### 🔴 Critical

#### [package-name]@[version] — [CVE-ID]
- **Severity:** Critical (CVSS [score])
- **Description:** [What the vulnerability enables]
- **Fix:** Upgrade to [version]
- **Breaking changes in fix:** [Yes/No — details]
- **Effort:** [Quick patch / Minor migration / Significant work]

---

### 🟠 High

[Same format]

---

## 📦 Outdated Packages

### Major Version Behind (Breaking Changes Likely)

| Package | Current | Latest | Behind | Risk |
|---------|---------|--------|--------|------|
| [name] | [ver] | [ver] | [N major] | [notes] |

### Minor/Patch Behind (Usually Safe)

| Package | Current | Latest | Behind |
|---------|---------|--------|--------|
| [name] | [ver] | [ver] | [N minor] |

---

## ⚖️ License Concerns

| Package | License | Concern |
|---------|---------|---------|
| [name] | [license] | [why this is flagged] |

---

## 📋 Prioritized Upgrade Plan

Ordered by impact and safety. Each step should be a separate commit/PR.

### Phase 1: Security Patches (Do Immediately)
1. `[package]` [current] → [target] — fixes [CVE]. Patch-level, safe to upgrade.
2. `[package]` [current] → [target] — fixes [CVE]. Minor version bump, review changelog.

### Phase 2: Safe Upgrades (Low Risk)
3. `[package]` [current] → [target] — [N] minor versions behind. Non-breaking.
4. `[package]` [current] → [target] — patch update. Bug fixes only.

### Phase 3: Major Upgrades (Schedule Time)
5. `[package]` [current] → [target] — major version. Key changes: [summary].
   - Estimated effort: [time]
   - Migration guide: [link if available]

### Phase 4: Evaluate (Optional)
6. `[package]` — consider replacing with [alternative]. [Reasoning].

---

## Recommendations

- **Lock file hygiene:** [observations about lock file state]
- **Pinning strategy:** [observations about version pinning — too loose, too strict]
- **Unused dependencies:** [any detected unused packages]
- **Duplicate dependencies:** [any detected duplicates at different versions]
```

### Step 6: Deliver

- Write the full report to `/mnt/user-data/outputs/dependency-audit-[date].md`
- Display the summary dashboard and Phase 1 action items in chat
- If critical CVEs are found, emphasize urgency

---

## Notes for Claude

- **Prioritization is the value.** Anyone can run `npm audit`. The skill is in ranking what matters, assessing real risk, and creating a phased plan that doesn't break things.
- **Context-aware risk.** A CVE in a dev-only dependency is less urgent than one in a production runtime dependency. Note the difference.
- **Don't create panic.** Many CVEs are theoretical or don't apply to the project's usage. Assess exploitability honestly.
- **Transitive dependencies matter.** Flag when a vulnerability is in a transitive dep that the user doesn't directly control.
- **Be specific about effort.** "Upgrade X" isn't helpful. "Upgrade X from 4.x to 5.x — requires updating import syntax per migration guide [link]" is.
- **Missing lock files are a finding.** If there's a `package.json` but no lock file, that's a reproducibility concern worth flagging.
- **Check both ecosystems.** Many full-stack projects have both Python and JS dependencies. Scan both.
