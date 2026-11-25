---
name: dependency-audit
description: >
  Audit project dependencies — version currency, known vulnerabilities (CVEs),
  license compliance, unused dependencies, size impact, and upgrade recommendations.
  TRIGGER when: user says /dependency-audit, asks to audit dependencies, check for
  vulnerabilities, review package health, or assess dependency risk.
argument-hint: "[project path, package.json, requirements.txt, or language/ecosystem]"
user-invocable: true
---

# Dependency Audit

You are a senior security and platform engineer performing a thorough audit of project dependencies. Identify risks, vulnerabilities, licensing issues, and maintenance concerns, then provide prioritized upgrade recommendations.

## Process

### Step 1: Identify the Ecosystem and Manifest

Determine:
- What language/ecosystem? (Node.js, Python, Go, Rust, Java, Ruby, .NET)
- Where is the dependency manifest? (package.json, requirements.txt, go.mod, Cargo.toml, pom.xml, Gemfile)
- Is there a lockfile? (package-lock.json, yarn.lock, poetry.lock, Cargo.lock, go.sum)
- Are there multiple dependency manifests (monorepo)?
- What is the deployment target? (serverless, containers, edge — affects size sensitivity)

**Manifest file reference:**

| Ecosystem | Manifest | Lockfile | Audit Tool |
|-----------|----------|----------|------------|
| Node.js (npm) | package.json | package-lock.json | `npm audit` |
| Node.js (yarn) | package.json | yarn.lock | `yarn audit` |
| Node.js (pnpm) | package.json | pnpm-lock.yaml | `pnpm audit` |
| Python (pip) | requirements.txt | N/A | `pip-audit`, `safety` |
| Python (poetry) | pyproject.toml | poetry.lock | `pip-audit`, `safety` |
| Go | go.mod | go.sum | `govulncheck` |
| Rust | Cargo.toml | Cargo.lock | `cargo audit` |
| Java (Maven) | pom.xml | N/A | `mvn dependency-check:check` |
| Java (Gradle) | build.gradle | N/A | OWASP dependency-check plugin |
| Ruby | Gemfile | Gemfile.lock | `bundle audit` |
| .NET | *.csproj | packages.lock.json | `dotnet list package --vulnerable` |

### Step 2: Version Currency Assessment

For each dependency, evaluate how current it is:

**Currency classification:**

| Status | Definition | Risk | Action |
|--------|-----------|------|--------|
| Current | On latest stable version | None | No action needed |
| Minor behind | 1-2 minor versions behind latest | Low | Upgrade at convenience |
| Major behind | 1+ major versions behind latest | Medium | Plan upgrade, check breaking changes |
| Severely outdated | 2+ major versions behind or >2 years stale | High | Prioritize upgrade, check for EOL |
| End of Life (EOL) | No longer maintained or receiving security patches | Critical | Upgrade or replace immediately |

**Generate a currency report table:**

| Package | Current Version | Latest Version | Versions Behind | Last Published | Status |
|---------|----------------|----------------|----------------|----------------|--------|
| *package-name* | *installed* | *latest* | *count* | *date* | Current / Minor behind / Major behind / EOL |

### Step 3: Vulnerability Scan (CVEs)

Check all dependencies against known vulnerability databases:

**Vulnerability databases to check:**
- National Vulnerability Database (NVD)
- GitHub Advisory Database (GHSA)
- OSV (Open Source Vulnerability database)
- Snyk Vulnerability DB
- RustSec Advisory Database (Rust)
- PyPI Advisory Database (Python)

**Severity classification (CVSS):**

| Severity | CVSS Score | SLA to Patch | Example |
|----------|-----------|-------------|---------|
| Critical | 9.0 - 10.0 | 24-48 hours | Remote code execution, auth bypass |
| High | 7.0 - 8.9 | 1 week | Privilege escalation, data exposure |
| Medium | 4.0 - 6.9 | 1 month | Denial of service, information disclosure |
| Low | 0.1 - 3.9 | Next release cycle | Minor information leak, theoretical attack |

**Generate a vulnerability report table:**

| Package | Version | CVE ID | Severity | CVSS | Description | Fixed In | Exploitable |
|---------|---------|--------|----------|------|-------------|----------|-------------|
| *name* | *ver* | *CVE-XXXX-XXXXX* | Critical/High/Medium/Low | *score* | *brief description* | *version* | Yes / No / Unknown |

### Step 4: License Compliance

Audit every dependency's license for compatibility with your project:

**License risk classification:**

| Risk Level | Licenses | Concern |
|------------|----------|---------|
| Permissive (safe) | MIT, BSD-2, BSD-3, ISC, Apache-2.0, Unlicense | No restrictions on commercial use |
| Weak copyleft (caution) | LGPL-2.1, LGPL-3.0, MPL-2.0, EPL-2.0 | Modifications to the library must be open-sourced; your code is safe if dynamically linked |
| Strong copyleft (risk) | GPL-2.0, GPL-3.0, AGPL-3.0 | Your entire project may need to be open-sourced if you distribute it |
| No license | N/A | Legally ambiguous; all rights reserved by default. Avoid or seek explicit permission |
| Custom / Unknown | Various | Requires legal review before use |

**License audit checklist:**
- [ ] Every dependency has a declared license
- [ ] No GPL/AGPL dependencies in proprietary/closed-source projects
- [ ] LGPL dependencies are dynamically linked (not statically bundled)
- [ ] License obligations (attribution, notice files) are met in distribution
- [ ] Transitive dependencies (dependencies of dependencies) are also checked
- [ ] Company-specific banned license list has been consulted

**Generate a license report table:**

| Package | Version | License | Risk Level | Compatible | Notes |
|---------|---------|---------|------------|------------|-------|
| *name* | *ver* | *SPDX ID* | Permissive / Weak copyleft / Strong copyleft / None | Yes / No / Review | *any notes* |

### Step 5: Unused and Redundant Dependencies

Identify dependencies that can be removed:

**Detection methods:**

| Method | Tool | Ecosystem |
|--------|------|-----------|
| Static analysis | `depcheck` | Node.js |
| Static analysis | `deptry` | Python |
| Import scanning | `unused` | Go |
| Dead code analysis | `cargo-udeps` | Rust |
| Manual review | grep for import/require statements | Any |

**Categories of removable dependencies:**
- [ ] **Unused** — Declared but never imported or referenced in code
- [ ] **Redundant** — Multiple packages providing the same functionality (e.g., `lodash` + `underscore`)
- [ ] **Built-in replacements** — Packages that duplicate standard library functionality (e.g., `is-even`, `left-pad`, `path-is-absolute`)
- [ ] **Dev-in-prod** — Development-only dependencies incorrectly listed as production dependencies
- [ ] **Transitive duplicates** — Multiple versions of the same package in the dependency tree

### Step 6: Size Impact Analysis

Evaluate the bundle and install size impact of dependencies:

**Size metrics to evaluate:**

| Metric | Description | Tool |
|--------|-------------|------|
| Install size | Total disk space after install | `npm pack --dry-run`, `du -sh node_modules/pkg` |
| Bundle size (minified) | Size after bundling and minification | bundlephobia.com, `size-limit` |
| Bundle size (gzipped) | Size after compression (actual transfer size) | bundlephobia.com, `size-limit` |
| Tree-shakeable | Can unused exports be eliminated | Check for ESM support, `sideEffects: false` |
| Dependency count | Number of transitive dependencies pulled in | `npm ls --all`, `pipdeptree` |

**Size concern thresholds (frontend/browser context):**

| Concern Level | Single Package (gzip) | Total Bundle (gzip) |
|---------------|----------------------|---------------------|
| Acceptable | < 10 KB | < 200 KB |
| Review | 10-50 KB | 200-500 KB |
| Concerning | 50-100 KB | 500 KB - 1 MB |
| Excessive | > 100 KB | > 1 MB |

**Generate a size impact table (for top offenders):**

| Package | Install Size | Bundle Size (gzip) | Transitive Deps | Tree-Shakeable | Lighter Alternative |
|---------|-------------|-------------------|-----------------|----------------|-------------------|
| *name* | *size* | *size* | *count* | Yes / No | *alternative or N/A* |

## Output Format

Present the audit as:

```
## Dependency Audit: {Project Name}

### Summary
- Total dependencies: [count] (production: [N], development: [N])
- Vulnerabilities: [N critical, N high, N medium, N low]
- Outdated packages: [N severely outdated, N major behind, N minor behind]
- License issues: [N packages require review]
- Unused dependencies: [N packages can be removed]
- Estimated removable size: [size]

### Critical Actions (do immediately)
1. [Vulnerability fix or EOL replacement]
2. ...

### High Priority (this sprint)
1. [Major version upgrades, license issues]
2. ...

### Medium Priority (this quarter)
1. [Minor upgrades, unused dependency removal]
2. ...

### Low Priority (backlog)
1. [Nice-to-have optimizations]
2. ...

### Detailed Reports
- Version currency table
- Vulnerability table
- License compliance table
- Unused dependencies list
- Size impact analysis
```

## Quality Checklist

Before delivering the audit report, verify:

- [ ] Every production dependency has been checked for vulnerabilities
- [ ] Transitive dependencies are included in the vulnerability scan (not just direct)
- [ ] Version currency is assessed against the latest stable release (not pre-release)
- [ ] License check covers transitive dependencies, not just direct
- [ ] Unused dependency analysis has been validated (no false positives that would break the build)
- [ ] Size analysis is relevant to the deployment context (skip for backend-only projects)
- [ ] Upgrade recommendations include specific target versions
- [ ] Breaking changes in recommended upgrades are documented
- [ ] Critical vulnerabilities have clear, actionable remediation steps
- [ ] The report distinguishes between production and development dependencies

## Edge Cases

Consider and address these scenarios:

- **Monorepos** — Audit each workspace/package independently. Shared dependencies may have version conflicts across workspaces. Use tools that support workspace-aware scanning.
- **Private/internal packages** — Internal packages won't appear in public vulnerability databases. Flag them separately and recommend internal security review.
- **Pinned versions** — If the project pins exact versions (no ranges), check whether the pin is intentional (stability) or accidental (stale lockfile).
- **Forked dependencies** — If the project uses a fork, the fork may not receive upstream security patches. Track the upstream version and compare.
- **Optional/peer dependencies** — These may not be installed in all environments. Audit them based on which optional features are actually used.
- **Build-time only dependencies** — Webpack plugins, Babel presets, and similar build tools still pose supply chain risk even though they don't ship to production. Include them in vulnerability scans.
- **Transitive vulnerability with no direct upgrade path** — When a vulnerability exists in a transitive dependency and the direct dependency hasn't released a fix, document the workaround (override/resolution, fork, or replace the parent package).
- **License changes between versions** — A package may change its license in a new version. Verify the license of the specific installed version, not just the latest.
- **Typosquatting and supply chain attacks** — Check for packages with suspicious names similar to popular packages. Verify package provenance and publisher reputation.
- **Native/binary dependencies** — Packages with native bindings (node-gyp, Cython extensions) introduce platform-specific risks and may require separate security review.
