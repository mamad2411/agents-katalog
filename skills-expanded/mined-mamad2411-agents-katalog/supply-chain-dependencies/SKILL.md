---
name: supply-chain-dependencies
description: Dependency risk and vulnerability review from local package manifests, lockfiles, and advisory databases — identifies known-vulnerable packages, abandoned or unmaintained dependencies, license conflicts, dependency confusion candidates, and unpinned version ranges. Operates exclusively on user-supplied manifest/lockfile data and approved advisory sources. Does not install, update, or modify dependencies. Every finding includes CVE/ GHSA references, fixed version, exploitability assessment, and upgrade/remediation path.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat, forensic]
authorization-required: conditional
evidence-outputs: [command-log, redacted-evidence, finding-draft, dependency-risk-matrix, vulnerability-register]
---

# Dependency risk review — known vulnerabilities, supply-chain integrity, and hygiene

Use this skill to review application dependencies for security risks. Analysis covers: known vulnerabilities (CVEs, GHSAs), end-of-life or unmaintained packages, unpinned version ranges that enable dependency confusion, and license compliance conflicts. All analysis is local and passive — read manifest and lockfile data, cross-reference against advisory databases, produce findings. Never install packages, modify dependency versions, upload manifests to external services, or trigger dependency resolution during this review.

## Required inputs

- Package manifests: `package.json`, `requirements.txt`, `Pipfile`/`Pipfile.lock`, `Gemfile`/`Gemfile.lock`, `Cargo.toml`/`Cargo.lock`, `go.mod`/`go.sum`, `pom.xml` (Maven), `build.gradle`/`build.gradle.kts` (Gradle), `composer.json`/`composer.lock`, `pubspec.yaml`, `*.csproj` (NuGet).
- Lockfiles: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Gemfile.lock`, `Cargo.lock`, `go.sum`, `poetry.lock`, `composer.lock`, `packages.lock.json`.
- SBOM (Software Bill of Materials) if available: CycloneDX or SPDX format.
- Written scope confirming which dependency ecosystems are in scope and whether the review extends to transitive (indirect) dependencies.
- Confirmation that no dependencies will be installed, updated, or modified.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` to verify dependency review policy.
2. `pentest_agent_parse_scope` to confirm the repo/project is in scope.
3. `pentest_agent_check_authorization` if external advisory lookup requires API calls.
4. `pentest_agent_build_command` for any dry-run command preview.
5. `pentest_agent_append_evidence` for redacted findings.

## Workflow

### Phase 1 — dependency inventory

Build a complete, versioned list of every direct and transitive dependency.

1. **Extract direct dependencies**:
   - Node.js: `jq '.dependencies, .devDependencies' package.json` (name and version range).
   - Python: `cat requirements.txt` (parse name and version constraint; handle `==`, `>=`, `~=`, `!=`).
   - Python/Poetry: `jq '.tool.poetry.dependencies, .tool.poetry.dev-dependencies' pyproject.toml`.
   - Ruby: `grep "^gem" Gemfile`.
   - Rust: parse `[dependencies]`, `[dev-dependencies]`, `[build-dependencies]` in Cargo.toml.
   - Go: parse `require (...)` block in go.mod.
   - Java/Maven: parse `<dependencies>` in pom.xml; parse `dependencies` block in build.gradle.
   - PHP: `jq '.require, .require-dev' composer.json`.
2. **Resolve transitive dependencies** from lockfiles:
   - Node.js: `jq '.packages | to_entries[] | select(.value.resolved != null)' package-lock.json` → name, version, resolved URL.
   - Python/Poetry: `jq '.package[] | {name: .name, version: .version}' poetry.lock`.
   - Rust: `grep "^name = \|^version =" Cargo.lock`.
   - Go: `go.sum` lists hashes but not names. Use `go mod graph` if the Go toolchain is available (read-only — does not modify anything).
   - Note: transitive dependencies are often the source of vulnerabilities. Do not skip this step.
3. **Version constraint analysis**: for each direct dependency, classify:
   - **Pinned** (`==`, exact version in lockfile): safe from dependency confusion; vulnerable only to compromise of the specific version.
   - **Floating** (`^`, `~`, `>=`, `*`, `latest`): version can change without the developer's explicit action. Risk: dependency confusion, malicious version adoption.
   - **Unpinned** (no constraint): highest risk. Any version can be resolved.

### Phase 2 — vulnerability identification

Cross-reference the dependency inventory against known vulnerability databases.

1. **Advisory sources** (prioritize official sources):
   - **GitHub Advisory Database (GHSA)**: covers npm, PyPI, RubyGems, Maven, Go, NuGet, Rust, Composer, pub.
   - **National Vulnerability Database (NVD/CVE)**: broad coverage.
   - **OSV (Open Source Vulnerabilities)**: ecosystem-specific databases (RUSTSEC, GSD, etc.).
   - **Snyk vulnerability database**: commercial, may require API key.
   - **Sonatype OSS Index**: free for limited use.
2. **Vulnerability lookup per dependency**:
   - For each dependency name and version, query: "Is there a known CVE or GHSA for this package at this version or earlier?"
   - Use local advisory database mirrors when available (reduce external calls).
   - Record: CVE/GHSA ID, CVSS score (v3 or v4), affected version range, fixed version, vulnerability type (RCE, DoS, info disclosure, privilege escalation, etc.), publication date.
3. **Exploitability assessment** (for each vulnerability):
   - **Active exploitation known?** (KEV catalog, CISA known exploited vulnerabilities).
   - **Exploit publicly available?** (Metasploit module, Exploit-DB, PoC on GitHub).
   - **Exploitation context**: does the vulnerable function/API get called in this application? Is the vulnerable feature enabled by default? Is authentication or special configuration required?
   - **Attack vector**: Network (remotely exploitable), Local (requires local access), Adjacent (same network segment).
   - Classify: **CRITICAL** (actively exploited, network-vector, no auth), **HIGH** (public exploit, network-vector), **MEDIUM** (public exploit, local-vector, or high-complexity), **LOW** (theoretical, no known exploit).

### Phase 3 — dependency hygiene and maintenance assessment

Beyond known CVEs, assess whether dependencies are well-maintained and trustworthy.

1. **Maintenance status**:
   - **Last release date**: more than 12 months ago → flag as potentially unmaintained.
   - **Repository activity**: last commit date, open issues vs closed issues ratio.
   - **Maintainer count**: single-maintainer packages are higher risk (bus factor = 1).
   - **Download count vs maintainer count**: widely-used single-maintainer packages are critical supply-chain nodes (e.g., left-pad incident).
2. **End-of-life frameworks and runtimes**:
   - Is the dependency a framework/runtime that has reached EOL? (e.g., AngularJS EOL, Python 2 EOL, .NET Core 2.1 EOL, Node.js 12 EOL).
   - EOL means no security patches. Every new CVE is unfixable without migration.
3. **Unpinned or suspicious registry sources**:
   - Does the project pull dependencies from non-standard registries? (private npm registry, internal PyPI mirror, Git URLs instead of versioned packages).
   - Check: `grep -E "(github\.com|gitlab\.com|bitbucket\.org)" package.json` (npm Git dependencies).
   - Check: `grep -E "(--index-url|--extra-index-url)" requirements.txt` (custom PyPI index).
   - Risk: custom registries can serve compromised packages if compromised themselves.
4. **Dependency confusion candidates**:
   - Internal/private package names: look for package names that appear to be internal (org-specific prefixes, non-standard names).
   - For each internal package name: check whether a package with that name exists on the public registry. If it does, anyone could have published it. If it doesn't, a dependency confusion attack could register it.
   - Note: do NOT register packages on public registries as a test — this constitutes an active supply-chain attack. Only check existence.

### Phase 4 — license and compliance review

Document license risks that may affect the organization.

1. **License inventory per dependency**: extract license field from manifest/lockfile metadata.
2. **Copyleft detection**: identify GPL, AGPL, LGPL, MPL, EUPL licenses that may impose distribution obligations.
3. **Incompatible licenses**: flag dependencies whose licenses conflict with the project license or organizational policy.
4. **Missing or unclear licenses**: flag packages without a license field. These are "all rights reserved" by default in many jurisdictions — potentially unlicensed use.

### Phase 5 — remediation planning

Produce actionable guidance for each finding.

1. **Per-vulnerability remediation**:
   - **Patch available**: upgrade to version X.Y.Z or later. Provide exact upgrade command (`npm install package@X.Y.Z`).
   - **No patch available**: recommend mitigation (WAF rule, configuration change, disable vulnerable feature, switch to alternative package). Document the residual risk.
   - **EOL package with unfixable vulnerability**: recommend migration to a supported alternative. Provide migration path if a replacement exists.
2. **Prioritization**: sort by severity, exploitability, and reachability. The dependency with a critical CVE that is called on every request path goes first. The dependency with a medium CVE in an unused transitive dep goes last.
3. **Automated enforcement**: recommend tools to prevent regression:
   - `npm audit` + `npm audit fix` (or better: `npm audit --production`).
   - Dependabot / Renovate for automated PRs.
   - Snyk / Socket / Phylum for supply-chain posture monitoring.
   - SBOM generation (CycloneDX or SPDX) in CI to maintain continuous dependency visibility.

## Decision points

- **Vulnerable dependency is a transitive dependency many layers deep**: check if the application actually imports the vulnerable code path. If the vulnerable function is in an unused module, document as "low reachability." Still recommend upgrade — defense in depth.
- **Vulnerable dependency has no fixed version**: recommend mitigation or package replacement. Flag as "active risk — no patch available." Monitor for patch release.
- **Dependency uses a Git commit hash instead of a version**: this is a supply-chain risk — the hash could be force-pushed. Recommend migrating to a versioned release from a trusted registry.
- **Multiple vulnerabilities in the same package**: consolidate into one finding with a single upgrade recommendation (to the latest version that fixes all).
- **License conflict is flagged but the organization has no license policy**: document as informational. Recommend the organization establish a license policy.

## Prohibited behavior

- Installing, updating, or modifying any dependency.
- Publishing packages to any registry (npm, PyPI, RubyGems, etc.) as part of dependency confusion testing.
- Running the application build process or dependency resolution.
- Uploading manifest/lockfile data to external services without explicit user approval per service.
- Providing drop-in exploit code for identified vulnerabilities.

## Stop conditions

- Checking dependency confusion would require registering a package on a public registry → stop. Document the package name as a candidate and recommend the organization register it defensively (or configure scoped registries).
- Vulnerability database requires a paid API key not provided by the user → document limitation. Use freely available sources (NVD, OSV, GitHub Advisory) for partial coverage.
- Manifest or lockfile is incomplete or unparseable → document and request updated files.

## Evidence

For each finding, record: package ecosystem, package name, installed version, fixed version, CVE/GHSA ID, CVSS score, vulnerability type, exploitability assessment, reachability notes, and remediation command. Evidence template:

```text
Dependency risk review for: [PROJECT_NAME]
Ecosystems reviewed: [npm / PyPI / RubyGems / Maven / Go / Cargo / Composer / NuGet]
Manifests analyzed: [list files]
Direct dependencies: [N], Transitive dependencies: [N]

Vulnerability summary:
  CRITICAL (actively exploited, network-vector): [N]
  HIGH (public exploit, network-vector): [N]
  MEDIUM (limited exploitability): [N]
  LOW (theoretical): [N]

Key findings:
  [CRITICAL] [package]@[version]  → CVE-YYYY-NNNNN (CVSS 9.8, RCE)
    Affected: all versions < [X.Y.Z]. Fixed in: [X.Y.Z].
    Exploitability: [active exploitation / public PoC / theoretical].
    Remediation: [upgrade command].
  ...

Hygiene findings:
  Unmaintained (>12 months): [N] packages
  EOL framework/runtime: [N]
  Unpinned version ranges: [N] direct dependencies
  Dependency confusion candidates: [N] package names
  Non-standard registry sources: [N]

License risks:
  Copyleft (GPL/AGPL): [N] packages
  No license specified: [N] packages
  Policy-incompatible: [N] packages

Redaction notes:
  - No packages were installed or modified.
  - No manifests were uploaded to external services.
  - Vulnerability data sourced from [GitHub Advisory / NVD / OSV].
  - Dependency confusion candidates listed by name; no registration attempt was made.
```

## Report handoff

1. `pentest_agent_record_finding` for each vulnerability or hygiene finding, with: ecosystem, package name/version, advisory ID, CVSS score, exploitability, fixed version, and remediation command.
2. Provide a prioritized remediation list: CRITICALs first with immediate upgrade commands, HIGHs second, MEDIUMs and LOWs for backlog.
3. If requested, generate an SBOM in CycloneDX JSON format from the collected inventory.
4. Explicitly note: no dependencies were installed, updated, or modified. No packages were published to any registry. All vulnerabilities were identified through static analysis of manifest and lockfile data cross-referenced with advisory databases.
