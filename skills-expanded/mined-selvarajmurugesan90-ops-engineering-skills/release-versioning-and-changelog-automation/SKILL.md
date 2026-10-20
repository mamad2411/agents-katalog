---
name: release-versioning-and-changelog-automation
description: >
  Establishes a version numbering scheme (SemVer or CalVer) and automates
  changelog generation and release tagging from commit history, typically
  via Conventional Commits and tools like semantic-release or
  release-please. Use when the user asks to "set up semantic versioning,"
  "auto-generate a changelog," "automate release tagging," "decide on a
  versioning scheme," "cut a release," or "figure out what changed between
  two versions."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Release Versioning and Changelog Automation

## Purpose

A version number is a promise: consumers of a library, API, or service use
it to decide whether an upgrade is safe. When versioning is inconsistent
(manually chosen, disconnected from what actually changed) or changelogs
are stale/hand-written-after-the-fact, that promise breaks — consumers
either upgrade blindly into a breaking change or avoid upgrading at all
out of distrust. This skill covers deriving version numbers and changelogs
automatically and consistently from commit history, so every release
carries an accurate, machine-verifiable account of what changed and how
risky the upgrade is.

## When to use

- Establishing a versioning scheme for a new library, service, or API
  (SemVer vs. CalVer, and why).
- Automating changelog generation from commit messages instead of
  hand-writing release notes after the fact (or not at all).
- Setting up automatic release tagging/publishing triggered by merges to
  the main branch.
- A consumer asks "what changed between v1.3.0 and v1.4.0" and there's no
  reliable answer beyond reading the full commit log.
- Enforcing Conventional Commits (or another structured commit format) so
  automation has something reliable to parse.
- Coordinating version bumps across a monorepo with multiple
  independently-versioned packages.

## Prerequisites & environment

- A commit message convention the team will actually follow —
  Conventional Commits (`feat:`, `fix:`, `feat!:`/`BREAKING CHANGE:`,
  `chore:`, etc.) is the most common because tooling (semantic-release,
  release-please, commitlint) is built around it, but any structured
  format works if it distinguishes breaking/feature/fix changes.
- Node.js ≥ 18 if using `semantic-release` (npm package, but works for
  any language's release artifact, not just JS); or `release-please` (Go
  binary/GitHub Action, language-agnostic) as an alternative with a
  slightly different model (it opens a standing "Release PR" that
  accumulates changes, rather than releasing on every merge).
- Git tag push permission for the CI identity, and, if publishing to a
  package registry as part of the release, registry publish credentials
  scoped to the release job only (see
  [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md)).
- A decision on SemVer vs. CalVer before automating: SemVer
  (`MAJOR.MINOR.PATCH`) suits libraries/APIs where consumers reason about
  compatibility; CalVer (`YYYY.MM.PATCH` or similar) suits products/
  services released on a cadence where "compatibility" is less the point
  than "when was this built."
- `commitlint` (or equivalent) wired into CI/pre-commit if you want
  malformed commit messages caught before they break automated version
  inference, rather than discovered at release time.

## Step-by-step guidance

1. **Adopt Conventional Commits** as the structured input automation will
   parse:
   ```
   feat(auth): add OAuth2 device code flow
   fix(billing): correct rounding in tax calculation
   feat(api)!: remove deprecated /v1/users endpoint

   BREAKING CHANGE: /v1/users is removed; use /v2/users instead.
   ```
   `feat` → minor bump, `fix` → patch bump, `!`/`BREAKING CHANGE:` footer
   → major bump. Enforce format with `commitlint` in a commit-msg hook or
   CI check so bad commits are caught at PR time, not discovered when a
   release computes the wrong version.

2. **Configure semantic-release** for "release on every merge to main"
   model:
   ```json
   {
     "branches": ["main"],
     "plugins": [
       "@semantic-release/commit-analyzer",
       "@semantic-release/release-notes-generator",
       "@semantic-release/changelog",
       ["@semantic-release/npm", { "npmPublish": true }],
       "@semantic-release/github",
       ["@semantic-release/git", {
         "assets": ["CHANGELOG.md", "package.json"],
         "message": "chore(release): ${nextRelease.version} [skip ci]"
       }]
     ]
   }
   ```
   Run it as a dedicated CI job after tests pass on `main`:
   ```yaml
   release:
     needs: [verify]
     if: github.ref == 'refs/heads/main'
     runs-on: ubuntu-latest
     permissions: { contents: write, issues: write, pull-requests: write }
     steps:
       - uses: actions/checkout@v4
         with: { fetch-depth: 0 }
       - uses: actions/setup-node@v4
         with: { node-version: "20" }
       - run: npx semantic-release
         env:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
   ```
   `fetch-depth: 0` is required — semantic-release needs full commit
   history to compute the next version, not a shallow clone.

3. **Or configure release-please** for a "standing release PR" model,
   which is often easier to review before anything ships (the PR itself
   *is* the changelog preview):
   ```yaml
   - uses: googleapis/release-please-action@v4
     with:
       release-type: node
       target-branch: main
   ```
   Every merge to `main` updates a long-lived "chore(main): release
   1.5.0" PR with the accumulated changelog; merging that PR is what
   actually cuts the tag/release. This suits teams wanting a deliberate
   "yes, ship this batch" moment rather than releasing on every merge.

4. **For a monorepo with multiple independently-versioned packages**, use
   a tool that understands package boundaries — `semantic-release` with
   `semantic-release-monorepo` extensions, `release-please`'s manifest
   mode, or Changesets (common in JS monorepos: contributors add a small
   `.changeset/*.md` describing the change and bump type per affected
   package, and a bot batches them into per-package releases).

5. **Publish the changelog and artifact together, atomically.** The
   release job should tag Git, generate/commit `CHANGELOG.md`, publish
   the package/image (pinned to that exact version — see
   [container-build-and-release](../container-build-and-release/SKILL.md)),
   and create the GitHub/GitLab release entry as one coordinated job —
   not as separate manual steps that can drift out of sync (e.g., a tag
   exists but the changelog wasn't updated, or vice versa).

6. **Surface breaking changes prominently**, not buried mid-changelog.
   Most changelog generators already group by type (Features, Bug Fixes,
   BREAKING CHANGES) — verify the `BREAKING CHANGES` section renders
   first/most visibly in the generated notes, since that's the section
   consumers most need before upgrading.

## Best practices

- Never hand-edit a version number that automation also manages — pick
  one source of truth (the tool) or you get drift between what's tagged
  in Git and what's declared in the manifest (`package.json`, `pyproject.toml`).
- Treat the commit message, not the PR title alone, as the thing
  automation parses (unless your tool is explicitly configured to use
  squash-merge PR titles) — decide which and be consistent, since a team
  that writes good PR titles but sloppy commit messages (or vice versa)
  will get inconsistent changelogs depending on which one the tool reads.
- Reserve manual/human-chosen version numbers for pre-1.0 or experimental
  packages where SemVer's compatibility promise doesn't yet apply
  (`0.x.y` releases are conventionally allowed to break on minor bumps) —
  document that explicitly so consumers aren't misled.
- Keep the changelog itself in the repo (`CHANGELOG.md`), not only in a
  release platform's UI, so it's versioned alongside the code and
  diffable across releases.
- Gate a release job behind the same passing test suite used for regular
  CI (per
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md)) — release
  automation should never bypass quality gates just because it's a
  separate job.
- For CalVer schemes, still record a monotonically increasing patch/build
  component (`2026.07.3`) so two releases in the same period remain
  orderable, and still generate a changelog — CalVer solves "when," not
  "what changed."

## Common pitfalls

- **Symptom:** semantic-release computes a version bump that doesn't
  match what the team expected (e.g., a release that should have been
  major only bumps minor).
  **Fix:** Check the actual commit messages since the last release for
  the `!`/`BREAKING CHANGE:` marker — a breaking change described only in
  prose without the structured marker will not be detected as breaking by
  the commit-analyzer plugin, regardless of how the PR description reads.

- **Symptom:** The changelog and the published package version disagree
  (changelog says 1.5.0, but the published package is still 1.4.2).
  **Fix:** The release steps ran out of order or partially failed — make
  tagging, changelog commit, and publish part of one atomic job/plugin
  chain (as semantic-release's plugin pipeline does) rather than separate
  jobs that can fail independently and leave things half-updated.

- **Symptom:** A squash-merged PR's commit message on `main` is just the
  PR title, losing the granular Conventional Commit messages from
  individual commits within the PR.
  **Fix:** Decide deliberately whether squash-merge is compatible with
  your setup — if squashing, enforce that the *PR title itself* follows
  Conventional Commits format (many teams add a `commitlint`/PR-title-lint
  check specifically for this), since that becomes the only commit
  message automation ever sees.

- **Symptom:** `semantic-release` runs but produces no release at all,
  with no clear error.
  **Fix:** Confirm the checkout step used `fetch-depth: 0` (full history)
  — a shallow clone frequently causes the commit-analyzer to see no
  releasable commits since it can't walk back to the last tag.

- **Symptom:** Consumers of a library keep getting broken by "minor"
  version bumps.
  **Fix:** Audit recent releases for commits marked `feat` that actually
  removed or changed existing behavior without a `!`/`BREAKING CHANGE:`
  marker — this is a commit-discipline problem, not a tooling problem;
  retrain contributors (and consider a PR template reminder) on when a
  change is actually breaking under SemVer.

## Worked example

**Scenario:** `payments-api` uses semantic-release on every merge to
`main`. Three PRs merge in sequence:

1. `fix(billing): correct rounding in tax calculation` → merges, triggers
   release: `1.4.1` → `1.4.2`. Changelog gets a new "Bug Fixes" entry.
2. `feat(webhooks): add support for retry-after header` → merges,
   triggers release: `1.4.2` → `1.5.0`. Changelog gets a "Features" entry.
3. `feat(api)!: remove deprecated /v1/users endpoint` with a
   `BREAKING CHANGE: /v1/users removed; use /v2/users.` footer → merges,
   triggers release: `1.5.0` → `2.0.0`. The generated `CHANGELOG.md`
   places a `BREAKING CHANGES` section at the top of the `2.0.0` entry.

Resulting `CHANGELOG.md` excerpt:
```markdown
## [2.0.0](.../compare/v1.5.0...v2.0.0) (2026-07-28)

### ⚠ BREAKING CHANGES
* **api:** /v1/users is removed; use /v2/users instead.

### Features
* **api:** remove deprecated /v1/users endpoint

## [1.5.0](.../compare/v1.4.2...v1.5.0) (2026-07-20)

### Features
* **webhooks:** add support for retry-after header

## [1.4.2](.../compare/v1.4.1...v1.4.2) (2026-07-18)

### Bug Fixes
* **billing:** correct rounding in tax calculation
```
Each release is tagged in Git (`v2.0.0`, etc.), the container image is
built and pushed with the matching immutable tag (see
[container-build-and-release](../container-build-and-release/SKILL.md)),
and consumers evaluating the upgrade from `1.5.0` to `2.0.0` can see
immediately, from the changelog alone, that a breaking API removal is
involved — without reading a single raw commit.

## Cross-references

- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md)
- [container-build-and-release](../container-build-and-release/SKILL.md)
