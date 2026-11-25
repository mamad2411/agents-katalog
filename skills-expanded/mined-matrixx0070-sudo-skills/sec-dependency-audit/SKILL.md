---
name: sec-dependency-audit
version: 1.0.0
description: Audit direct and transitive dependencies for known CVEs and produce a prioritized, reachability-aware remediation plan.
author: matrixx0070
tags: [security, dependencies, cve, sca, supply-chain, defensive]
capabilities: []
---

## When to use

Use this before a release, during supply-chain reviews, or on a recurring schedule to catch vulnerable and abandoned packages. You identify and remediate known weaknesses in third-party code.

**Not for:** writing exploits against a vulnerable package; auditing your own application logic (use `sec-code-audit`); or fabricating advisory data. Cite real auditor output — never estimate CVE counts.

## Method

1. **Inventory dependencies.** Collect direct and transitive packages from lockfiles (`package-lock`, `pnpm-lock`, `poetry.lock`, `go.sum`). Note versions and whether each is direct or transitive.
2. **Run the ecosystem auditor.** Use the native tool (`npm audit`, `pnpm audit`, `pip-audit`, `osv-scanner`) and read the raw output. Cite counts by severity directly from it.
3. **Map CVEs.** For each advisory record the CVE/GHSA id, affected package, vulnerable range, fixed version, and CVSS severity.
4. **Assess exploitability.** *Decision point:* is the vulnerable code path actually reachable from your app? A Critical CVE in an unused transitive branch may rank below a reachable High. Note maintenance status too.
5. **Plan remediation.** For each: upgrade to the fixed version, apply an override/resolution for transitive pins, or document a compensating control if no fix exists. *Decision point:* if no patch exists and the path is reachable, escalate for a design decision rather than silently deferring.
6. **Prevent drift.** Recommend automated dependency updates and CI audit gating.

## Example

`npm audit` reports GHSA-xxxx in `lodash@4.17.15`, fixed in `4.17.21`, severity High, pulled in transitively by `some-lib`. Reachability: your code uses the affected `_.template`. Action: add a resolution pinning `lodash@4.17.21`, or upgrade `some-lib` to a version that requires the patched range; re-run the auditor to confirm the advisory clears.

## Pitfalls

- **Estimating instead of citing.** "About a dozen highs" is not a finding. Quote the auditor's exact counts.
- **Upgrading blindly.** A major-version bump can break your build; check the changelog and test before pinning.
- **Ignoring transitive depth.** The vulnerable package is often three levels down; overrides/resolutions, not a direct install, are the fix.
- **Treating unreachable and reachable CVEs identically.** Reachability should reorder your remediation queue, not just CVSS.

## Output format

```
## Scan summary
Tool: <npm audit / osv-scanner / ...>. Advisories by severity (from output): C:_ H:_ M:_ L:_

## CVE table
| CVE/GHSA | Package | Current | Fixed | Severity | Direct/Transitive | Reachable? | Action |
|----------|---------|---------|-------|----------|-------------------|------------|--------|

## Remediation plan
Ordered by severity then effort.

## Residual / no-fix items
- <item> — compensating control
```
