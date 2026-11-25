---
name: changelog-generate
description: "Generate release notes from commit / PR history: breaking first with migration notes, computed semver bump; handles a repo with no tags."
kind: skill
pack: documentation
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# changelog-generate

## Premise

A changelog is *generated from categorized history* — conventional-commit types or PR labels grouped for humans — with breaking changes surfaced at the top and the version bump *derived* from the change set. It is not hand-written from memory (which forgets), and it is not a raw `git log` dump (which is noise no user reads). The reader wants three answers fast: *is anything going to break me, what's new, what got fixed* — in that order.

Cite-or-halt. Every changelog line traces to a commit SHA or a PR number; every breaking-change entry cites **the commit/PR that introduced it and the type marker that classified it** (`BREAKING CHANGE:` footer, `!` after type, or a `breaking`/`major` label). Every semver claim cites the change types that forced it. "This is roughly a minor release" without the type tally is a vibe. An unclassifiable commit is itself a reportable finding (a convention gap), not something to silently drop.

## When to run

- At release-cut time — generate the notes for the version being tagged from the range since the last tag.
- In CI on the release branch to keep an `Unreleased` section current as PRs merge.
- Before publishing a package — the changelog is the first thing a consumer diffs before upgrading.
- After a run of commits landed with no convention — to surface the classification gap *before* it's release day and too late to fix.
- **Not** for internal-only history browsing — that's what `git log` is for; this skill produces the human-facing, categorized artifact.

## Procedure

1. **Determine the range — and never let a missing tag read as an empty one.** `git describe --tags --abbrev=0` exits 128 in a repo with no tags, and a script that swallows that error generates notes for nothing. Resolve the base in this order and print which one was used:
   ```bash
   export GIT_OPTIONAL_LOCKS=0
   BASE=$(git describe --tags --abbrev=0 2>/dev/null); RANGE="$BASE..HEAD"; WHY="last tag $BASE"
   [ -z "$BASE" ] && { RANGE="HEAD"; WHY="no tags: the whole history from root $(git rev-list --max-parents=0 HEAD | tail -1 | cut -c1-7) (first release)"; }
   echo "range: $RANGE ($WHY) · $(git rev-list --count $RANGE) commits"; git rev-parse --is-shallow-repository
   ```
   With no tags but a generator that has already released (a `.release-please-manifest.json` version, a changeset release commit), the whole history over-counts: ask for the last release commit and pass it as the explicit range, rather than guessing one from a version string (a version is not a git ref). A shallow clone (`true` above) truncates the range: fetch full history first (`fetch-depth: 0` in CI), or the notes are incomplete. In a monorepo with per-package tags (`pkg@1.2.3`), resolve the base per package (`git describe --tags --abbrev=0 --match '<pkg>@*'`). An explicit range from the caller wins over all of these.
2. **Parse each commit / PR into a typed change.** Extract the conventional-commit type and scope from the subject (`feat(orders): …`, `fix: …`, `perf:`, `refactor:`, `docs:`, `chore:`), the `!` breaking marker (`feat!:`), and the `BREAKING CHANGE:` body footer. Where PR labels are the convention instead of commit types, read the labels (`type: feat`, `breaking`).
3. **Flag the convention gap.** Any commit with no parseable type and no classifying label is `UNCLASSIFIED` — list it separately. A pile of unclassified commits means the release notes are incomplete; that's a finding to surface, not a set to silently omit.
4. **Group by category, breaking-first.** Order sections: **⚠ Breaking Changes** → Features → Fixes → Performance → other (Refactor/Docs/Deps), each entry one human-readable line + its PR/issue link. Drop pure `chore`/`ci`/`test` noise from the user-facing view (keep it only in a verbose mode).
5. **Surface breaking changes with migration notes.** Each breaking entry gets its own paragraph: what broke, and the *before → after* the consumer must do. A breaking change buried as a one-liner in the fix list is a defect (see detectors) — it must be at the top with a migration path.
6. **Derive the semver bump — don't ask, compute.** `major` if any breaking change; else `minor` if any `feat`; else `patch`. Cross-check against the version the release *actually* proposes: if a `feat` is shipping as a patch, or a breaking change as a minor, flag `BUMP-MISMATCH`.
7. **Emit in Keep a Changelog format** — dated `## [x.y.z] - YYYY-MM-DD` heading, grouped `###` sections, an `## [Unreleased]` at the top for in-flight work, and link references at the bottom.
8. **Detect drift from a hand-maintained changelog.** If a `CHANGELOG.md` exists and was edited by hand, diff its latest section against generated history — entries in history but not the file are `MISSING`; entries in the file with no matching commit are `PHANTOM`.

**Detection is not this skill's job.** A breaking change already shipped without a note is `doc-drift-scan` §12 (DH-1), and a changelog whose grammar is broken (order, duplicates, dates, compare links, `[Unreleased]`) is `doc-structure-scan` §9 (DH-2); `/doc-refresh --audit` runs both. The changelog version against the released version is devops `release-integrity-scan` RL-2 (when the devops pack is installed). Step 8 below stays as this generator's **self-check** before it writes: it compares what it is about to emit with the hand-maintained file and lists MISSING and PHANTOM, it does not audit history. A changelog a generator owns (release-please, changesets, git-cliff, semantic-release) is regenerated, never hand-edited ([precedents § 17](../../../../snippets/precedents/documentation.md)).

## Adapt to the codebase

Prefer the generator the repo already uses; mirror its config rather than swapping tools.

| Signal | Tool |
|---|---|
| `conventional-changelog` config, or Angular-style commits | `conventional-changelog` / `standard-version` |
| `release-please-config.json` / release-please Action | `release-please` (PR-driven, monorepo-aware) |
| `cliff.toml` present | `git-cliff` (fast, language-agnostic, highly templatable) |
| `.releaserc` / semantic-release config | `semantic-release` (fully automated publish + notes) |
| `.changeset/` directory (JS monorepo) | `changesets` (per-PR intent files, per-package versioning) |
| No tool, but disciplined conventional commits | parse `git log` directly with the same rules |

Read the convention actually in force: conventional-commit *types* vs PR *labels* vs changeset *intent files*. In a monorepo, scope the range and the version bump **per package** — a `feat` in package A is a minor for A, not for B. Match the existing `CHANGELOG.md` heading style if one is established.

## Output

Literal report: the generated notes in Keep a Changelog format, the derived bump with its justification, then the convention/drift findings.

```
changelog-generate — v2.3.1..HEAD  ·  27 commits, 9 PRs  ·  convention: conventional-commits

Derived bump: MINOR → v2.4.0
  (1 feat, 4 fix, 0 breaking; highest = feat ⇒ minor)
  ⚠ BUMP-MISMATCH: release.yml proposes v2.3.2 (patch) but a feat shipped → should be v2.4.0.

## [2.4.0] - 2026-07-09

### ⚠ Breaking Changes
_(none this release)_

### Features
- Bulk order export as CSV (#412)

### Fixes
- Refund rounding error on partial refunds (#418)
- Race in the session-refresh interceptor (#420)
- Timezone offset dropped in the audit log (#421, closes #399)

### Performance
- Order-list query: 340ms → 45ms via covering index (#419)

CONVENTION GAP — 3 UNCLASSIFIED commits (excluded from notes):
  a1b2c3d  "wip"                 → no type; cannot categorize
  d4e5f6a  "fix stuff"           → `fix` type but empty scope/subject
  9f8e7d6  "update deps and also add retry to the webhook sender"
                                 → mixed feat+chore in one commit; split next time

DRIFT vs hand-maintained CHANGELOG.md:
  MISSING: #419 (perf) present in history, absent from the file.
```

Closure verb: **generate-and-write** when history is fully classifiable, **halt-handoff** when `UNCLASSIFIED` commits or a `BUMP-MISMATCH` need a human decision before the notes can be trusted.

## False positives / gotchas

- **Merge commits and reverts** double-count if not collapsed — squash-merge repos have clean 1:1 PR→commit mapping; merge-commit repos need `--first-parent` or PR-based parsing. A `revert:` of an unreleased `feat` cancels it; don't list both.
- **Non-conventional but legitimate commits** (a hotfix pushed straight to a release branch) aren't garbage — flag them `UNCLASSIFIED` for triage, don't silently drop a real fix.
- **`chore(deps)` that patches a CVE** is user-facing despite being a chore — a security-relevant dependency bump belongs in the notes; don't blanket-filter all chores.
- **Scope ≠ package in a polyrepo-shaped monorepo** — a `feat(ui)` scope is a label, not necessarily a package boundary; derive per-package bumps from the changed paths, not the scope string alone.
- **The version bump is computed, not negotiated** — if the team "wants" a patch but a breaking change landed, the honest bump is major. Report the derived bump; the mismatch is the finding.

## Halt conditions

- Refuse to emit notes that silently omit `UNCLASSIFIED` commits — an incomplete changelog that looks complete is the failure mode. List them and their SHAs.
- Refuse any semver bump not justified by the type tally in the output; no "feels like a minor" without the `feat`/`fix`/breaking counts.
- A breaking change must render at the top with a migration note. Halt rather than filing it as an ordinary fix line — burying it is the defect.
- Never hand-author entries from memory to "fill gaps" — every line cites a SHA/PR or it doesn't ship.
- On `BUMP-MISMATCH`, surface it and stop short of tagging; the version number is a contract, not a guess.

## Related

- `add-adr.md` (command) — the ADR's `## Recent Changes` / status log records *why a decision was made*; the changelog records *what shipped*. A breaking change here should point at the ADR that decided it; they're paired, not duplicative.
- `doc-refresh.md` (command) — after a release, doc-refresh reconciles `ai/status.md` `Updated:` + `## Recent Changes` with the just-generated notes.
- `@doc-writer` — polishes the human phrasing of feature/breaking entries once the categorized skeleton is generated; this skill produces the classified structure, doc-writer sharpens the prose.
- `devops` release flow (cross-pack) — consumes the derived semver bump + notes to tag, version, and publish; changelog-generate produces the artifact that flow ships.

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). **Preconditions are not verification** — this skill guards its entry and must also check its exit. Every entry under `## Failure modes` that this skill's own write could cause becomes a check here, observed rather than assumed, reported when it passes as well as when it fails, and `NOT RUN` with a reason where no signal is available. A failure mode the skill documented and never checked is a risk it accepted on the caller's behalf without saying so.
