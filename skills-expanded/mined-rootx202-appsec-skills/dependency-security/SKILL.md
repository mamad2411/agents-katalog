---
name: dependency-security
description: Dependency and supply-chain vulnerability scanner for npm, pip, composer, gradle, cargo, and other package ecosystems. Use whenever the user wants to check for known CVEs, outdated packages, or supply-chain risk in package.json, requirements.txt, composer.json, build.gradle, Cargo.toml, or similar manifest/lockfiles, for any project.
---

# Dependency Security — Supply-Chain Vulnerability Scanner

A skill for auditing third-party libraries and dependencies for known vulnerabilities (CVEs) and outdated versions.

## When to use this
- Request to scan `package.json`, `requirements.txt`, `composer.json`, `build.gradle`, `Cargo.toml`, or a lockfile
- Before deployment, to confirm no dependency carries a known-critical vulnerability

## Methodology
1. Read the manifest and, if present, the lockfile (more accurate for exact resolved versions).
2. For each package, check (using available tools such as running an audit command, or web search when appropriate) whether that specific version has known CVEs.
3. Compare current version against the latest stable release.
4. Rate severity based on the actual vulnerability's real-world exploitability, not simply "the version is old."

## Suggested Tools by Ecosystem
- **npm**: `npm audit` — run it for real if the environment allows, and read its actual output rather than guessing.
- **pip**: `pip-audit`, or manual comparison against the OSV database.
- **composer**: `composer audit`
- **cargo**: `cargo audit`
- If the tool or network isn't available, say so explicitly and provide analysis based on well-documented, widely known vulnerabilities for those libraries, while noting that a real audit tool run is still recommended for certainty.

## Report Format Per Affected Package
```
Package: [name]
Current Version: [x.y.z]
CVE: [CVE ID if applicable]
Risk: Critical/High/Medium/Low
Affected Function: [where this library is actually used in the project]
Upgrade: [recommended safe version]
Breaking Changes: [does the upgrade require code changes?]
```

## Additional Considerations
- **Transitive dependencies**: indirect dependencies (dependencies of dependencies) can carry vulnerabilities too — don't stop at the top level.
- **Typosquatting**: check for packages with names suspiciously similar to popular ones that may have been added by mistake (supply-chain risk).
- **Unused packages**: flag any installed dependency that isn't actually used in the code — removing it reduces attack surface.
- After upgrading, remind the user to run the test suite to confirm nothing broke.

## Rules
- Never claim a vulnerability exists without grounding it in a real source (an actual audit tool result or a documented CVE) — if unsure, say so rather than asserting it.
- Stay focused on third-party dependencies; issues in the user's own code belong to `code-audit`.
