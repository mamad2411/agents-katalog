---
name: triaging-vulnerable-dependencies
description: Triages vulnerable and malicious dependencies with bumper — scans lockfiles for known CVEs and known-malicious packages, pulls authoritative detail from the bumper Advisor, and picks a safe version before installing. Use when adding or upgrading a dependency, editing a lockfile (package-lock.json, yarn.lock, pnpm-lock.yaml, requirements.txt, go.sum, Cargo.lock, etc.), or when a vulnerability or malware alert appears.
---

# Triaging vulnerable dependencies with bumper

bumper scans dependencies for known vulnerabilities and known-malicious packages,
using the bumper Advisor for data. It needs the `bumper` CLI on PATH
(https://github.com/gnana997/bumper). If a package is flagged malicious, do not
install it.

## Workflow

1. Scan the lockfile(s):
   ```
   bumper deps                       # auto-detect lockfiles in the current directory
   bumper deps --json path/to/lock   # machine-readable findings for one file
   ```
   Exit codes: 0 = clean, 1 = findings present, 2 = usage error.

2. For each finding, get authoritative detail. Prefer the `bumper-advisor` MCP when
   connected (use fully-qualified tool names):
   - `bumper-advisor:lookup_cve` — CVEs affecting a specific package + version
     (args: ecosystem, package, version)
   - `bumper-advisor:get_vuln` — full detail for one advisory id (CVE/GHSA)
   - `bumper-advisor:check_malware` — reputation of a package (is it malware?)
   - `bumper-advisor:search_cve` — search CVEs by keyword/ecosystem

   If the MCP is not connected, fall back to the CLI: `bumper deps --json …`.

3. Decide per finding:
   - **Malicious package** → do NOT install. Remove it; find a trusted alternative.
   - **Vulnerable, fix available** → upgrade to the lowest version that clears the
     advisory (`lookup_cve` / `get_vuln` list fixed versions).
   - **Vulnerable, no fix** → surface the risk to the user; pin and isolate, or drop
     the dependency. Do not silently proceed.

4. Apply the fix and re-scan (repeat until clean):
   a. Update the manifest/lockfile to the chosen version.
   b. `bumper deps`.
   c. If findings remain, return to (a).

## Example

Adding `lodash`:
1. `bumper deps` → **HIGH**: lodash 4.17.4 (prototype pollution).
2. `bumper-advisor:lookup_cve ecosystem=npm package=lodash version=4.17.4`
   → fixed in 4.17.12.
3. Bump to `lodash ^4.17.21`, re-run `bumper deps` → clean. Install.

## Full, version-matched procedure

For the complete steps and any checks specific to this installed bumper version:
```
bumper skills get deps-triage
```
