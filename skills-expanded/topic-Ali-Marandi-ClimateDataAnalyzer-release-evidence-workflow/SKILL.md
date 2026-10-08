---
name: release-evidence-workflow
description: Build an auditable release-evidence workflow for a desktop or packaged application. Use when implementing or reviewing authoritative-data features, local and live smoke validation, guarded GitHub Actions Windows packaging/signing, controlled commit/push, release-readiness reporting, or technical/executive presentation materials.
---

# Release Evidence Workflow

Use this workflow to turn an implemented desktop product into evidence that is reviewable without overstating scientific, security, or release claims.

## Guardrails

- Separate **branch CI artifacts** from **signed public releases**. Never call an unsigned branch installer a stable signed release.
- Require fresh, explicit approval before a remote push, tag, public release, secret mutation, payment, or installer execution.
- Never request, print, stage, commit, or pass a PFX password, PAT, signing certificate, or Base64 certificate in a command argument.
- Treat external-source responses as time-bounded evidence. Record the exact input, source label, timestamp, result, and failure collection; do not claim availability, accuracy, or latency guarantees from one smoke run.
- Preserve the product’s scientific boundary. Published scenario summaries are not a new physical model, deterministic forecast, local-impact conclusion, or operational recommendation.

## Workflow

### 1. Establish the release boundary

Inspect repository state before modifying it:

```bash
git status -sb
git log --oneline -5
git remote -v
git config user.name && git config user.email
```

Record the current version in package metadata and runtime metadata. State whether the target operation is only a branch push, a version tag, or a public release. If the user has not explicitly authorized the relevant external action, stop after local preparation.

### 2. Define data and geography semantics

When the product consumes authoritative external data, document the source, parameter contract, uncertainty fields, and known scope. For country-level scenario summaries, label spatial exports as country summaries. Do not invent a high-resolution raster from a country aggregate. Preserve CRS, transform, data type, source and limitation metadata in GIS outputs.

### 3. Generate evidence, not assertions

Run the full local suite in a reproducible headless mode where appropriate. Persist a verbose log with test names and slowest durations:

```bash
mkdir -p docs/validation_logs
set -o pipefail
QT_QPA_PLATFORM=offscreen pytest -vv --durations=10 2>&1 \
  | tee docs/validation_logs/local_pytest_YYYY-MM-DD.log
```

Run at most a bounded, user-relevant live smoke request. Save the output and elapsed observation. Clearly distinguish a test failure from a missing local measurement utility or other environment failure.

Report total collected/passed/failed/skipped/xfailed, duration, major test families, slowest tests, live request inputs, source label, returned fields, failure collection, and measurement limitations.

### 4. Design GitHub Actions with a signed-release gate

Use two distinct paths.

| Path | Trigger | Minimum evidence | Publication rule |
|---|---|---|---|
| Branch CI | push / pull request | tests, package build, installer build, silent install-uninstall test, unsigned artifact | Never publish stable release |
| Stable release | protected `vX.Y.Z` tag | environment approval, PFX secret checks, Authenticode signing and verification, signed installer silent test | Publish only signed artifacts |

Audit each invoked JavaScript action before publishing workflow changes. Inspect its tagged `action.yml` and upgrade to a Node.js 24-compatible major for checkout, language setup, artifact upload/download, and third-party release actions. Add a static contract test that rejects known Node.js 20 majors, then use the next CI run to prove the warning is gone.

Use a protected environment such as `production` for signing. Require expected secret names but never create fake secret values. A PFX pattern normally needs `CODESIGN_PFX_BASE64`, `CODESIGN_PFX_PASSWORD`, and a trusted timestamp URL configured as a variable or controlled input. Decode certificates only into the runner temp directory, use SHA-256 plus an RFC 3161 timestamp, run `signtool verify /pa /all` on both EXE and installer, and delete the temporary PFX afterward.

Do not claim code signing until a CI run has actually signed and verified artifacts with the real certificate.

### 5. Commit and push in controlled stages

Use explicit paths rather than `git add .`. Before committing, inspect staged content:

```bash
git diff --check
git add <explicit-paths>
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Scan staged material for accidental credentials. The scan supplements, but does not replace, human review. Commit only after reviewing the staged diff. Before push, fetch and compare refs. Push only with fresh user authorization:

```bash
git fetch --prune origin
git log --oneline origin/<branch>..HEAD
git push origin <branch>
```

After push, verify branch alignment and inspect the CI run. Do not create a tag or release unless it was separately authorized.

### 6. Write a decision-ready evidence summary

Create a concise technical report with: current commit/ref, exact test result, performance caveat, live-source result, CI state, signing state, release state, and next gates. Use status words precisely:

- **Passed:** a named command or CI job completed successfully.
- **In progress:** a remote job has started but has no final conclusion.
- **Not executed:** a gated step, such as signing, was intentionally not run.
- **Not created:** no tag, release, or secret exists.

### 7. Prepare presentations without changing evidence

Create separate content and speaker-script files before creating slides. Use a concise executive deck and, when requested, an internal technical deck. Include the scientific boundary, uncertainty, evidence artifacts, validation outcome, release state, and decisions required. Preserve current status rather than projecting future success.

## Definition of Done

Deliver a readable evidence package with validation log(s), local/live metrics summary, CI link or status, signing/release state, and presentation materials. Attach this `SKILL.md` when delivering the skill so it can be installed or downloaded.
