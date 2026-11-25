---
name: software-composition-analysis-sca
description: >
  Guides scanning third-party and transitive dependencies for known
  vulnerabilities and license issues using tools such as Grype, Trivy,
  OWASP Dependency-Check, npm audit/pip-audit, or GitHub
  Dependabot/Snyk, and building a remediation workflow around the
  results. Use when the user asks to "scan dependencies for
  vulnerabilities", "add SCA to the pipeline", "check for known CVEs in
  our packages", "set up Dependabot/Renovate", "fix a vulnerable
  transitive dependency", or "generate a vulnerability report for our
  open-source components". Distinct from SAST (own source code) and DAST
  (runtime behavior).
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Software Composition Analysis (SCA)

## Purpose

Modern applications are assembled mostly from third-party and open-source
code — direct dependencies plus their own transitive dependencies, often
outnumbering an application's own source code by an order of magnitude or
more. Software Composition Analysis (SCA) identifies every component in
that dependency tree, matches it against vulnerability databases (the
National Vulnerability Database/NVD, GitHub Advisory Database, OSV.dev,
vendor advisories) and license databases, and flags known-vulnerable or
license-incompatible components before they ship. Unlike SAST (which
analyzes code you wrote) or DAST (which probes running behavior), SCA is
concerned entirely with *what you depend on* — and it is often the single
highest-leverage scan a team can add, since a large share of real-world
breaches trace back to a known, patchable vulnerability in a dependency
that was never updated.

## When to use

- The user asks to "scan dependencies for vulnerabilities", "add SCA to
  the pipeline", or "check for known CVEs" in a project's packages.
- A new CVE is publicly disclosed for a widely-used library and the user
  needs to determine if/where it's used across a codebase or fleet of
  services.
- The user wants automated dependency-update PRs (Dependabot, Renovate)
  configured, or wants help triaging the resulting PR backlog.
- The user needs a Software Bill of Materials (SBOM) as an input — SCA
  tools frequently consume or produce SBOMs; for SBOM *generation* and
  supply-chain provenance specifically, see
  [supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md).
- The user wants to enforce a license-compliance policy (e.g. block
  GPL-licensed dependencies in a proprietary product).
- The user needs to distinguish a container image's OS-package
  vulnerabilities from its application-dependency vulnerabilities.

## Prerequisites & environment

- A resolvable dependency manifest/lockfile per ecosystem: `package-lock.json`
  or `yarn.lock`/`pnpm-lock.yaml` (npm/yarn/pnpm), `requirements.txt`/
  `poetry.lock`/`Pipfile.lock` (Python), `go.sum` (Go), `pom.xml`/
  `gradle.lockfile` (Java), `Gemfile.lock` (Ruby), `Cargo.lock` (Rust).
  SCA tools generally need the lockfile, not just the top-level manifest,
  to see transitive dependencies accurately.
- Tool options:
  - **Trivy** (`aquasecurity/trivy`, current `0.5x` line) — scans
    filesystems, container images, and IaC in one tool; good default for
    a "just scan everything" first pass.
  - **Grype** (`anchore/grype`) — pairs naturally with Syft-generated
    SBOMs (see the supply-chain skill); fast, container- and
    filesystem-aware.
  - **OWASP Dependency-Check** — mature, Java/`.NET`-centric roots but
    supports other ecosystems; NVD-based.
  - Ecosystem-native: `npm audit`, `pip-audit`, `bundler-audit`, `govulncheck`
    (Go) — good lightweight first line, but each only understands its own
    ecosystem, so a polyglot repo needs multiple tools or a
    multi-ecosystem scanner (Trivy/Grype) as well.
  - **Dependabot** (native to GitHub) or **Renovate** (self-hosted or
    Mend-hosted, more configurable) — for automated update PRs rather
    than point-in-time scanning.
- Network egress from CI to the relevant vulnerability database/registry
  (NVD, OSV.dev, GitHub Advisory API, or a mirrored internal feed for
  air-gapped environments).
- A defined severity threshold and remediation SLA (e.g. "critical:
  patch within 48h, high: 2 weeks") — without one, SCA produces a large
  backlog nobody is accountable for.

## Step-by-step guidance

1. **Run a baseline scan** to see current exposure before gating
   anything:
   ```bash
   trivy fs --scanners vuln --severity HIGH,CRITICAL .
   ```

2. **Add a CI step** that fails on new critical/high findings in
   direct dependencies, while tracking (not blocking on) transitive
   findings that require an upstream fix you don't control directly:
   ```yaml
   name: sca
   on: [pull_request]
   jobs:
     trivy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Trivy filesystem scan
           uses: aquasecurity/trivy-action@0.24.0
           with:
             scan-type: 'fs'
             scan-ref: '.'
             severity: 'CRITICAL,HIGH'
             exit-code: '1'
             ignore-unfixed: true
   ```
   `ignore-unfixed: true` avoids blocking on CVEs with no available patch
   yet — track those separately with a re-scan schedule instead of
   failing every build indefinitely.

3. **Scan container images** separately from source, since OS packages
   (from the base image) and application dependencies have different
   patch paths:
   ```bash
   trivy image --severity CRITICAL,HIGH myorg/myapp:1.4.2
   ```

4. **Configure automated dependency updates** so fixes land as PRs
   instead of manual triage. Dependabot example:
   ```yaml
   # .github/dependabot.yml
   version: 2
   updates:
     - package-ecosystem: "npm"
       directory: "/"
       schedule:
         interval: "weekly"
       open-pull-requests-limit: 10
       groups:
         minor-and-patch:
           update-types: ["minor", "patch"]
   ```
   Grouping minor/patch updates keeps the PR count manageable; leave
   major-version bumps ungrouped since they usually need manual review.

5. **Suppress with justification and an expiry**, never a silent ignore:
   ```yaml
   # .trivyignore
   # CVE-2023-XXXXX: no fix available upstream yet, low exploitability in our usage
   # (library used only in build tooling, not shipped to production). Re-review 2026-09-01.
   CVE-2023-XXXXX
   ```

6. **Add a license-compliance check** if the product has licensing
   constraints:
   ```bash
   trivy fs --scanners license --license-full .
   ```

7. **Feed results into the same triage/ticketing pipeline as SAST/DAST**
   findings (see [secure-cicd-gates](../secure-cicd-gates/SKILL.md)) so
   dependency vulnerabilities aren't managed in a separate, disconnected
   process from other security findings.

## Best practices

- Scan lockfiles, not just top-level manifests — transitive dependencies
  are where most unnoticed vulnerable code actually lives.
- Distinguish "fixed" from "unfixed" findings and gate primarily on the
  former; track the latter with a re-scan cadence instead of perpetually
  failing builds for issues with no available patch.
- Scan both source/filesystem and built container images — a
  vulnerability can enter via either the application's own dependency
  tree or the base image's OS packages, and they're patched differently
  (dependency bump vs. base-image bump).
- Automate updates (Dependabot/Renovate) for the bulk of low-risk
  minor/patch bumps so humans only review major-version or
  security-critical updates.
- Set and honor a remediation SLA by severity, and report on SLA
  adherence, not just raw finding count — an unbounded backlog with no
  deadline effectively means "never fix."
- Treat a clean SCA report as necessary, not sufficient — it only knows
  about *publicly disclosed* vulnerabilities in *known* components; pair
  it with [sast-integration](../sast-integration/SKILL.md) for code you
  wrote yourself and
  [supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md)
  for provenance/tampering risks a vulnerability scan doesn't address.
- Regenerate scans on a schedule (not just on dependency change) — new
  CVEs are disclosed against *already-installed* versions constantly, so
  yesterday's clean scan can be wrong today with no code change at all.

## Common pitfalls

- **Symptom:** SCA scan reports a critical CVE in a transitive dependency
  three levels deep that the team has no direct control over, and the
  build is blocked indefinitely with no clear owner.
  **Fix:** Check whether a newer version of the *direct* dependency pulls
  in a patched transitive version first (`npm ls <pkg>`, `mvn dependency:tree`);
  if no upstream fix exists yet, suppress with an expiry date and
  re-review cadence rather than blocking indefinitely, and track it on a
  dependency-risk register.

- **Symptom:** Dependabot/Renovate opens 30+ PRs overnight and the team
  stops reviewing them entirely.
  **Fix:** Group minor/patch updates into batched PRs, cap
  `open-pull-requests-limit`, and set up auto-merge for
  patch-level updates that pass CI, reserving manual review for
  major-version bumps and security-labeled PRs.

- **Symptom:** The same CVE is reported by three different tools with
  three different severity scores, confusing prioritization.
  **Fix:** Pick one primary source of truth for severity (e.g. the
  vendor/GitHub Advisory Database CVSS score) for gating decisions, and
  treat other tools' scores as supplementary context, not competing gates.

- **Symptom:** A container image scan reports dozens of CRITICAL findings
  that all trace back to the base OS image, none of which the
  application team can directly patch.
  **Fix:** Bump the base image tag (e.g. move to a newer `-slim`/distroless
  variant or the next patch release) rather than trying to patch
  individual OS packages by hand; see
  [container-image-hardening](../container-image-hardening/SKILL.md) for
  a broader base-image strategy.

- **Symptom:** A scan that passed yesterday fails today with no code
  changes.
  **Fix:** This is expected — a new CVE was disclosed against an
  already-installed version. Confirm via the CVE ID, then patch or
  suppress-with-justification; it is not a scanner bug.

## Worked example

A Node.js service adds Trivy filesystem scanning to CI, Dependabot for
automated updates, and a documented suppression for one unfixed
low-exploitability CVE.

`.github/workflows/sca.yml`:
```yaml
name: sca
on: [pull_request]
jobs:
  trivy-fs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@0.24.0
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
          ignore-unfixed: true
```

`.trivyignore`:
```
# CVE-2024-XXXXX: fix requires upgrading to a major version with breaking
# API changes; library is used only in an internal CLI tool, not exposed
# to untrusted input. Re-review by 2026-10-01. Tracked in JIRA-4821.
CVE-2024-XXXXX
```

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 8
    groups:
      minor-and-patch:
        update-types: ["minor", "patch"]
```

Sample Trivy finding that blocks a PR:
```
myapp/package-lock.json (npm)
==============================
Total: 1 (HIGH: 1)

┌─────────┬────────────────┬──────────┬──────────┬───────────────┬───────────────┐
│ Library │ Vulnerability  │ Severity │ Status   │ Installed Ver │ Fixed Ver     │
├─────────┼────────────────┼──────────┼──────────┼───────────────┼───────────────┤
│ ejs     │ CVE-2024-YYYYY │ HIGH     │ fixed    │ 3.1.6         │ 3.1.10        │
└─────────┴────────────────┴──────────┴──────────┴───────────────┴───────────────┘
```
Remediation: bump `ejs` to `>=3.1.10` (`npm install ejs@3.1.10`), commit
the updated lockfile, and re-run the scan to confirm it clears.

## Cross-references

- [supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md) —
  SBOM generation and provenance attestation, which SCA tools often
  consume as input or produce as a byproduct.
- [sast-integration](../sast-integration/SKILL.md) — analyzes your own
  source code rather than third-party dependencies; the two are
  complementary, not overlapping.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — how to combine SCA
  with SAST/DAST into one coherent set of pipeline gates and a single
  triage workflow.
