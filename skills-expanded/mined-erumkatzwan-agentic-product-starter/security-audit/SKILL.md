---
name: security-audit
description: Use when setting up a new product from this starter, before a release, when the weekly Security workflow or a Dependabot alert is red, or when asked for a vulnerability overview. Produces one report of known vulnerabilities across every app and fixes them by upgrading to the lowest safe stable version.
---

# Security audit

One overview of known vulnerabilities in the dependencies of every app, and a safe way to fix them.

## 1. Get the overview

Run both and merge the results into one table:

```bash
node scripts/security-audit.mjs --out security-report.md          # all apps against osv.dev
gh api "repos/{owner}/{repo}/dependabot/alerts?state=open&per_page=100" \
  --jq '.[] | [.security_advisory.severity, .dependency.manifest_path, .dependency.package.name, .security_vulnerability.first_patched_version.identifier, .html_url] | @tsv'
```

* The script covers the web app, back office and website (npm), the backend (NuGet, after `dotnet restore`), Android (Gradle, needs Java) and iOS (Swift packages, when added). It says what it could not scan.
* Dependabot alerts cover the same ecosystems from GitHub's side, including Android through automatic dependency submission.
* Also check **Security → Code scanning** (CodeQL) and **Secret scanning** in the repository. A leaked secret is always critical: rotate it first, then remove it.

Show the user one table: severity, app, package, current version, fixed version, runtime or dev, advisory link. Lead with the counts per severity.

The latest weekly result is also on the website's **Security** page (`apps/website/security/`) and the README badge, both published by the Security workflow to the `security` branch. After fixing, run the **Security** workflow on `main` (Actions → Security → Run workflow) so the dashboard updates. For a private product, the `SECURITY_DASHBOARD` repository variable set to `off` stops publishing.

## 2. Triage

| Severity | Fix within | Notes |
|---|---|---|
| Critical | 2 days | Stop other work. Runtime code first |
| High | 7 days | The weekly report fails until fixed |
| Moderate | 30 days | Batch with the next dependency update |
| Low | Next dependency update | |

Lower the priority one step when the package is **dev** only (build or test tools never shipped to users), unless the advisory affects the build itself (supply chain, code execution during install).

Create one GitHub issue per app, labelled `security` and the app's `area:` label, listing its findings. Use the `triage` skill's labels for readiness.

## 3. Fix

Always move to the **lowest fixed version that is on the latest stable line**: prefer a patch or minor upgrade; a major upgrade follows the `update-dependencies` skill.

| Ecosystem | Direct dependency | Transitive (pulled in by another package) |
|---|---|---|
| npm (web app, back office, website) | `npm install <pkg>@<version>` | Upgrade the parent first; otherwise add `"overrides": { "<pkg>": "<version>" }` in `package.json`, then `npm install` |
| NuGet (backend) | Change `Version` in the `.csproj` `PackageReference` | Add a direct `PackageReference` to the fixed version (it wins over the transitive one) |
| Gradle (Android) | Change the version in `gradle/libs.versions.toml` | Add a `constraints { implementation("<group>:<artifact>:<version>") }` block in `app/build.gradle.kts` with a comment linking the advisory |
| Swift Package Manager (iOS) | Raise the minimum version in `project.yml` packages | Update the parent package |
| GitHub Actions | Bump the tag in `.github/workflows/*.yml` | – |
| Toolchains (.NET SDK, JDK, Node, Xcode) | Raise the version in the workflow and the app's README | – |

Rules:

* Stable releases only: no alpha, beta, RC or snapshot versions.
* No fix available yet: record it in the issue with the advisory link, check whether the vulnerable code path is used, and add a mitigation if it is. Re-check weekly.
* Never silence a finding (no ignore lists, no lowered thresholds) without an ADR that explains why.
* One pull request per app, titled `fix(security): <app> <package> <old> → <new>`.

## 4. Verify

1. Re-run `node scripts/security-audit.mjs` and confirm the findings are gone.
2. Run the app's checks: `make ci` (iOS, Android), `npm run lint && npm test` (web apps), `dotnet test` (backend).
3. Open the pull request. **Dependency review** must pass, plus every other required check.

## When to run it

* Right after creating a new product from this starter (and after the `rename-product` step).
* Before every release.
* When the weekly **Security** workflow fails, or a Dependabot alert arrives.
* On request: "run a security audit".
