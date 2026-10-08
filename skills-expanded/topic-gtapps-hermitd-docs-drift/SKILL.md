---
name: docs-drift
description: Documentation-drift audit for this plugin monorepo. Audit either each scoped plugin's unreleased changelog claims or its latest shipped release from the previous reachable plugin-name--v* tag, then verify that plugin READMEs, docs, CLAUDE.md or AGENTS.md files, and root documentation tell the truth for the matching snapshot. Report meaningful contradictions with concrete proposed edits and wait for approval before changing files. Use when preparing or verifying a release, when asked to check the latest version, or when the user says "docs drift", "check the docs", "are the docs up to date", "docs audit", "did the docs keep up", or whether documentation matches released or unreleased changes. Complements pre-release-review, which checks changelog claims against code; this skill checks changelog claims against docs.
---

# Docs Drift

Verify that documentation tells the truth about either the changes about to
ship or the latest version already shipped.

Keep the audit read-only. Do not edit, commit, tag, push, publish, or release
until the user explicitly approves specific findings. Even after approval,
never commit or publish from this skill.

## Invocation

- `$docs-drift` or `$docs-drift unreleased` — audit every plugin with a
  non-empty `[Unreleased]` section.
- `$docs-drift <plugin-slug>` — audit that plugin's unreleased changes.
- `$docs-drift latest` — audit the latest reachable release of every tagged
  plugin.
- `$docs-drift latest <plugin-slug>` — audit only that plugin's latest release.

Use unreleased mode by default. Treat "latest version", "latest release", or
equivalent wording as latest-release mode.

Typical release order, when the sibling skills are installed:

`$release-status` → `$pre-release-review` → `$docs-drift` → `$release`

## Step 1 — Scope plugins and snapshots

Never mix released and unreleased windows in one claim set.

### Unreleased mode

Identify plugins whose `[Unreleased]` section contains non-blank content:

```bash
for p in plugins/*/CHANGELOG.md; do
  slug=$(basename "$(dirname "$p")")
  awk '/^## \[Unreleased\]/{f=1; next} /^## \[/{f=0} f && NF' "$p" | rg -q '.' \
    && echo "$slug"
done
```

If the user named a plugin, limit scope to that slug after verifying it exists
and has unreleased content. If nothing is in scope, stop with:

`No unreleased changes in any plugin — nothing to drift-check.`

Use the working tree as the documentation snapshot. Keep incidentally noticed
older drift separate as pre-existing debt.

### Latest-release mode

Start from all `plugins/*/CHANGELOG.md` slugs, or only the user-named slug.
Resolve each plugin's refs independently:

```bash
EMPTY_TREE=$(git hash-object -t tree /dev/null)

for p in plugins/*/CHANGELOG.md; do
  slug=$(basename "$(dirname "$p")")
  latest=$(git describe --tags --abbrev=0 --match "${slug}--v*" HEAD 2>/dev/null || true)

  if [ -z "$latest" ]; then
    printf '%s\n' "$slug: skipped (no reachable release tag)"
    continue
  fi

  previous=$(git describe --tags --abbrev=0 --match "${slug}--v*" "${latest}^" 2>/dev/null || true)
  printf '%s\n' "$slug latest=$latest previous=${previous:-<empty-tree>}"
done
```

Use only reachable `<slug>--v*` tags. Do not select an unreachable tag merely
because its version sorts later. If a plugin has only one reachable tag, use
the empty tree as its previous snapshot. If every scoped plugin lacks a tag,
stop with:

`No reachable plugin release tags — nothing to latest-release drift-check.`

For each plugin, use:

- claim window: `<previous-tag>..<latest-tag>`, or empty tree to latest tag;
- changelog claims: the exact `## [<latest-version>]` section at the latest tag;
- documentation snapshot: the repository exactly at that plugin's latest tag.

Later commits and working-tree changes are not release claims in this mode.
Different plugins may have different latest-tag snapshots; preserve that
mapping throughout the audit.

## Step 2 — Extract doc-checkable claims

In unreleased mode, read only each scoped plugin's working-tree `[Unreleased]`
section.

In latest-release mode, derive the version from `<slug>--v<version>` and read
the matching changelog section from the tagged snapshot:

```bash
version=${latest##*--v}
git show "$latest:plugins/$slug/CHANGELOG.md" | awk -v ver="$version" '
  index($0, "## [" ver "]") == 1 {f=1; next}
  /^## \[/ && f {exit}
  f
'
```

Also inspect the plugin-scoped release diff to catch doc-checkable
consumer-visible changes that a changelog bullet may group:

```bash
release_diff_base=${previous:-$EMPTY_TREE}
git diff "$release_diff_base" "$latest" -- "plugins/$slug/"
```

Use that diff only in latest-release mode and only for claim discovery; this
skill does not replace changelog-versus-code review.

Turn each claim into zero or more checks:

- **Removal or rename** — a skill, command, script, hook, config key, doc file,
  or CLI changed identity.
- **New operator-visible surface** — a new skill, command, config block, hook,
  CLI, or channel behavior should appear where siblings are enumerated.
- **Changed default or behavior** — documentation may still state the previous
  default or behavior. Treat this as the highest-severity class.
- **Count or version claim** — a hand-written number or version marker may
  still contain the old value.
- **Promised documentation** — a cited file or anchor must exist and cover what
  the changelog promises.

Mark pure internal fixes, refactors, and test-only changes as `no doc surface`.
Do not manufacture a finding for every bullet.

## Step 3 — Sweep the matching documentation

For each scoped plugin, consider the files that exist in its selected snapshot:

- `plugins/<slug>/README.md`
- `plugins/<slug>/docs/*.md`
- `plugins/<slug>/CLAUDE.md`
- `plugins/<slug>/AGENTS.md`
- top-level plugin extras such as `SAFETY.md`, `DOCKER.md`, or
  `CONTRIBUTING.md`

Also check relevant root documentation:

- root `README.md`
- root `CLAUDE.md`
- root `AGENTS.md`
- root documentation extras relevant to a claim

Work claim-first, not file-first:

- **Unreleased:** use `rg -n` against the working tree. Sweep root files once
  against the union of all claims.
- **Latest release:** use `git grep -n <pattern> "$latest" -- <paths>` and
  `git show "$latest:<path>"`. Sweep root files at each plugin's own latest-tag
  snapshot. Deduplicate identical root findings in the report without losing
  the plugin/tag evidence.

Never silently substitute current documentation for a released snapshot.

When more than two plugins are in scope and agent delegation is available,
delegate one plugin audit per worker. Give each worker that plugin's claims,
mode, and snapshot ref, and require:

`snapshot:file:line — contradicted claim — current text — suggested fix`

Keep the root-file sweep in the main session because it needs cross-plugin
deduplication. Respect the available agent-slot limit and use additional waves
if needed. If delegation is unavailable, perform the checks sequentially.

In latest-release mode, re-check each snapshot finding against the current
working tree:

- If it is still stale, propose an edit to the current file.
- If it is already corrected, report it under `Fixed after release` with no
  proposed edit.
- If the file no longer exists, explain its replacement or removal and do not
  propose recreating it without evidence.

## Step 4 — Judge meaningfulness

Propose an edit only when a reader would be factually misled:

- **Meaningful:** references a removed or renamed surface; states an old
  default or behavior; gives a wrong count or version; omits a new surface from
  a sibling enumeration; or promises documentation that does not exist or does
  not cover the claim.
- **Not meaningful:** tone, formatting, absent marketing coverage, missing
  documentation for internal fixes, or changelog accuracy that
  `$pre-release-review` owns.
- **Borderline:** reader impact is unclear. Report it separately with a
  one-line rationale and no proposed edit.

This marketplace ships as a research preview. Removed operator surfaces are
deleted from documentation. Do not propose a Legacy section, leftover config
keys in examples, "legacy configuration" labels, or dual current/old
descriptions. State the present surface only.

Do not pad findings.

## Step 5 — Report and wait for approval

Use this shape:

```text
# Docs Drift — <date>

## Scope
Mode: <unreleased | latest release>
In scope: <slugs with snapshot refs>
Skipped: <slugs and reasons>
Claim windows: <[Unreleased] | previous-tag..latest-tag per plugin>
Documentation snapshots: <working tree | latest tag per plugin>

## Findings
### <n>. <slug> — <misleading | stale-reference | missing-doc>
- Claim: <abbreviated claim and changelog/diff evidence>
- Drift: <snapshot>:<doc file:line> — currently says: "<excerpt>"
- Current tree: <still stale | changed | file removed>
- Proposed edit: <exact replacement text, or "add section X covering Y">

## Fixed after release (no edit proposed)
- <snapshot>:<file:line> — <what was stale and where it is now corrected>

## Borderline (no edit proposed)
- <snapshot>:<file:line> — <one-line rationale>

## No doc surface
- <briefly grouped internal or test-only claims>

## Pre-existing drift (not this window)
- <anything noticed outside the selected claim window>

## Verdict
<N> actionable findings across <M> current files | Docs are clean for this window.
```

Ask which actionable findings to apply: all, selected finding numbers, or none.
The audit request itself is not approval to edit.

After the user approves:

1. Apply only the approved edits to the current working tree with `apply_patch`.
   Never edit a tag.
2. Match each document's existing style. Keep edits succinct: prefer one
   sentence or one table-cell correction, and do not restate a full policy when
   its established term or canonical link is enough. Delete a removed surface;
   do not relabel it as leftover, compatibility, or legacy support.
3. Re-read the changed passages and run `git diff --check`.
4. Do not add a changelog entry for documentation-only edits; repository
   guidance explicitly excludes them.
5. Report the uncommitted files and verification. Never commit, push, tag,
   publish, or release from this skill.
