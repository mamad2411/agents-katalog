---
name: artifact-and-dependency-management
description: >
  Manages build artifacts and third-party dependencies through a private
  registry/proxy with lockfiles, version pinning, retention policies, and
  automated update workflows. Use when the user asks to "set up an
  artifact repository," "configure a package registry proxy/mirror,"
  "pin/lock dependency versions," "clean up old artifacts," "handle a
  dependency update / Dependabot-Renovate PR," or "avoid a left-pad-style
  supply-chain incident."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Artifact and Dependency Management

## Purpose

Every build depends on two kinds of external input: third-party packages
pulled in at build time (npm, PyPI, Maven, NuGet, etc.) and the artifacts
your own pipelines produce (binaries, container images, packages). Left
unmanaged, both become sources of instability and risk — an upstream
package can be yanked, compromised, or silently change behavior between
builds, and your own artifact storage can grow unbounded or lose the
exact-version traceability needed to know what's actually deployed. This
skill covers running a private registry/proxy for dependencies, pinning
and locking versions, and keeping first-party artifact storage clean and
trustworthy.

## When to use

- Standing up a private package registry or pull-through proxy/mirror
  (Artifactory, Nexus, GitHub Packages, Verdaccio, a cloud-native
  registry) in front of public registries like npm/PyPI/Maven Central.
- Introducing or auditing lockfiles (`package-lock.json`,
  `poetry.lock`/`requirements.txt` with pinned hashes, `go.sum`) to make
  builds reproducible.
- Triaging automated dependency-update PRs (Dependabot, Renovate) at
  scale without rubber-stamping or ignoring them entirely.
- An upstream package was yanked, deprecated, or found compromised, and
  builds need to keep working (or need to stop pulling it) immediately.
- Artifact storage (container registry, package repo) is growing
  unbounded and needs a retention/cleanup policy.
- A build is non-reproducible: "worked yesterday, fails today" with no
  code change.

## Prerequisites & environment

- A chosen artifact/package registry solution: a managed offering (GitHub
  Packages, GitLab Package Registry, cloud provider artifact registries)
  or self-hosted (Artifactory, Sonatype Nexus, Harbor for containers,
  Verdaccio for npm).
- Package manager versions that support lockfiles with integrity hashes:
  npm ≥ 7 (`package-lock.json` lockfileVersion 2/3), pip with
  `--require-hashes` or Poetry/Pipenv, Go ≥ 1.16 (`go.sum` verified by
  default via `GOSUMDB` unless explicitly disabled), Maven/Gradle with
  dependency lock files or checksum verification enabled.
- CI credentials scoped to *publish* to first-party registries separately
  from credentials that only need *read* access to pull dependencies —
  publish rights should be tightly restricted (e.g., only release
  pipelines, not every PR build).
- A decision on retention policy inputs: how many versions/tags to keep,
  for how long, and whether any tags (release, `latest`) are exempt from
  cleanup.

## Step-by-step guidance

1. **Put a pull-through proxy/mirror in front of public registries**
   rather than having every build reach the public internet directly.
   Example Artifactory/Nexus-style virtual repo config (conceptual): a
   `npm-remote` repo proxying `registry.npmjs.org`, cached locally, with a
   `npm-virtual` repo combining it with your private `npm-local` packages.
   Point CI and developer machines at the virtual repo:
   ```bash
   npm config set registry https://artifacts.example.com/api/npm/npm-virtual/
   ```
   This gives resilience against upstream outages/deletions (cached
   copies survive), a single point to apply security scanning, and
   traceability of exactly which package versions were ever pulled.

2. **Commit lockfiles and enforce them in CI** so builds are reproducible
   byte-for-byte on dependency resolution, not just "same version range":
   ```bash
   npm ci                 # fails if package-lock.json is out of sync, unlike npm install
   pip install --require-hashes -r requirements.txt
   ```
   `npm ci` (not `npm install`) in CI is important: it errors out if the
   lockfile and `package.json` disagree, instead of silently re-resolving.

3. **Pin direct dependencies to specific versions in manifests** and let
   the lockfile pin transitive dependencies; avoid unpinned ranges
   (`^1.2.3`/`*`) for anything security- or stability-sensitive in
   production services. Fully floating ranges are more defensible in
   short-lived tooling than in a service's runtime dependency tree.

4. **Automate update PRs, but gate them with CI**, not blind auto-merge:
   `renovate.json` example enabling automerge only for patch-level, CI-passing
   updates:
   ```json
   {
     "extends": ["config:recommended"],
     "packageRules": [
       {
         "matchUpdateTypes": ["patch"],
         "automerge": true
       },
       {
         "matchUpdateTypes": ["major"],
         "automerge": false,
         "labels": ["needs-manual-review"]
       }
     ]
   }
   ```
   Route major-version bumps to a human; let CI (full test suite) be the
   actual gate for automerge, not just "Renovate opened it."

5. **Respond to a yanked/compromised upstream package deliberately**:
   confirm the pinned version in your lockfile isn't the affected one; if
   it is, pin to a known-good version explicitly in the manifest, purge
   the proxy's cached copy if your registry tool supports it, and re-run
   `npm ci`/equivalent to confirm the resolved tree no longer includes it.
   Because builds go through your proxy's cache, you are not silently
   exposed to a package being deleted out from under you mid-incident —
   but you must still act if the version you already have cached is the
   bad one.

6. **Define and enforce artifact retention** so storage doesn't grow
   unbounded and old, unreferenced artifacts don't accumulate risk
   (stale, unpatched images sitting in a registry indefinitely). Example
   GitHub Container Registry cleanup via a scheduled workflow using
   `actions/delete-package-versions`:
   ```yaml
   on:
     schedule:
       - cron: "0 3 * * 0"
   jobs:
     cleanup:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/delete-package-versions@v5
           with:
             package-name: "payments-api"
             package-type: "container"
             min-versions-to-keep: 20
             delete-only-untagged-versions: true
   ```
   Always exclude tags matching your release scheme (`v*`, `stable`) from
   deletion, and prefer `delete-only-untagged-versions`/dry-run modes
   before enabling deletion of tagged versions.

7. **Audit what's actually in use vs. what's stored.** Periodically cross
   reference deployed image digests/package versions against what's in
   the registry so retention policy decisions are based on real usage,
   not guesses.

## Best practices

- Separate "publish" credentials (used only by trusted release pipelines)
  from "read/pull" credentials (used broadly by CI and developers) so a
  compromised build job can't push malicious artifacts under your
  namespace.
- Verify package integrity, not just presence: rely on lockfile hashes
  (`npm ci`, `pip --require-hashes`, `go.sum`) rather than trusting that a
  version number alone means identical bytes — registries can, in
  principle, be compromised or misconfigured.
- Keep a private registry mirror even for ecosystems that feel
  low-risk — public registry outages and unannounced package removals
  affect every ecosystem, not just the ones that have had famous
  incidents.
- Treat major dependency upgrades as their own reviewed change with a
  changelog read-through, not a rubber-stamped automerge — pair with
  [release-versioning-and-changelog-automation](../release-versioning-and-changelog-automation/SKILL.md)
  when the upgrade affects your own published artifact's versioning
  contract.
- Record artifact provenance (which commit/pipeline run produced a given
  artifact) as metadata/labels on the artifact itself, so retention
  cleanup and incident response can trace an artifact back to its build —
  this dovetails with build metadata practices in
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md).
- Scan both first-party artifacts and third-party dependencies for known
  vulnerabilities as part of the same pipeline, not as separate,
  disconnected processes.

## Common pitfalls

- **Symptom:** A build that passed last week fails today with no code
  changes, due to a transitive dependency resolving to a new (breaking)
  version.
  **Fix:** This indicates missing or unenforced lockfiles — commit the
  lockfile, and run the package manager's strict/CI install mode
  (`npm ci`, `pip install --require-hashes`) so resolution can't silently
  drift between runs.

- **Symptom:** An upstream package is deleted/yanked from the public
  registry and every build across the org breaks simultaneously.
  **Fix:** This is exactly what a pull-through proxy/mirror with local
  caching prevents — if you don't have one yet, stand one up, and in the
  interim, vendor or manually re-host the specific version needed to
  unblock builds.

- **Symptom:** Dependabot/Renovate opens dozens of PRs and the team either
  ignores all of them or auto-merges all of them without review.
  **Fix:** Configure update-type-based rules (auto-merge patch-level
  updates gated on CI passing; require human review for
  minor/major) rather than treating every update PR identically.

- **Symptom:** Container registry storage costs/quota keep growing and
  nobody can tell which images are safe to delete.
  **Fix:** Introduce a retention policy keyed on tag pattern and age
  (e.g., keep all `v*` release tags indefinitely, purge untagged/
  build-SHA images older than 90 days), and dry-run the cleanup job
  before enabling actual deletion.

- **Symptom:** A "hotfix" dependency version pin gets left in place
  indefinitely after the underlying issue is fixed upstream, silently
  blocking future updates.
  **Fix:** File a follow-up ticket whenever you add an emergency pin, and
  review pinned/overridden versions periodically (e.g., each quarter) to
  confirm they're still necessary.

## Worked example

**Scenario:** `left-pad-style-lib@3.2.1`, a transitive dependency of
`payments-api`, is unpublished from the public npm registry mid-morning,
and the team's CI starts failing `npm ci` with a 404.

1. Because CI pulls through `artifacts.example.com/api/npm/npm-virtual/`
   (a caching proxy) rather than `registry.npmjs.org` directly, builds
   that already resolved and cached `3.2.1` continue to succeed —
   confirm this by checking the proxy's cache for the tarball.
2. For any environment that hadn't cached it yet, pin an explicit
   replacement in `package.json` (`"left-pad-style-lib": "3.2.0"`, the
   last known-good published version) and run `npm install` once to
   regenerate `package-lock.json`, then commit the lockfile update.
3. Open a PR titled "pin left-pad-style-lib to 3.2.0 (3.2.1 unpublished
   upstream)" so the pin is visible and reviewable, and file a follow-up
   ticket to revisit once the ecosystem stabilizes (e.g., a maintained
   fork or replacement package is adopted).
4. Confirm `npm ci` (strict mode) passes in CI with the updated lockfile
   before merging, and verify the retention/cleanup job hasn't
   inadvertently purged the cached `3.2.1` tarball your proxy needs to
   keep serving historical builds that still reference it.

## Cross-references

- [container-build-and-release](../container-build-and-release/SKILL.md)
- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md)
