---
name: ship-notes
description: "Generate dual-audience release notes from an exact git scope (upstream delta, tag range, ref range, or time window) with semver bump suggestions and commit-appendix traceability. Use after a sprint, before a release, or when asked 'what shipped'."
alwaysAllow: ["Bash", "Read", "Glob", "Grep"]
---

# ship-notes: Scoped Release Notes Generator

<objective>
Generate dual-audience release notes from a precisely defined git scope. Prefer exact compare ranges over fuzzy date windows, use PR data only as enrichment, and preserve traceability with a full commit appendix whenever the scope is large or explicitly range-based.
</objective>

## Prerequisites

- **git** >= 2.12
- **gh** >= 2.0 (optional; enrichment only)
- **Python 3** (optional; only for portable date helpers if needed)

Check:

```bash
git --version
gh --version
```

## 1. Resolve Repository and Scope First

Do **not** collect logs until the repository and scope are explicit.

### Input Forms

`$ARGUMENTS` may contain any of these forms:

- nothing
- a repo path
- a single branch or ref
- an exact range like `from..to` or `from...to`
- flags: `--from`, `--to`, `--since`, `--base`, `--full`, `--include-merges`

Examples:

- `ship-notes`
- `ship-notes main`
- `ship-notes origin/main..HEAD`
- `ship-notes v2.7.12..HEAD`
- `ship-notes --from v2.7.12 --to HEAD`
- `ship-notes --since "30 days ago"`
- `ship-notes /path/to/repo`
- `ship-notes /path/to/repo origin/main..main --full`

### Repository Resolution

- If the first token is an existing directory, `cd` there and continue parsing the remaining arguments.
- Otherwise stay in the current directory.
- Stop if not inside a git repo.

Checks:

```bash
git rev-parse --is-inside-work-tree
git rev-parse --show-toplevel
```

### Scope Precedence

Resolve scope in this exact order:

1. **Explicit `--from` / `--to`**
   - If `--from` is provided, treat scope as exact range.
   - Default `--to` to `HEAD` if omitted.
   - Result: `FROM..TO`

2. **Explicit range token**
   - If the user supplied `A..B` or `A...B`, use it exactly as written.
   - Prefer two-dot ranges for release notes unless the user explicitly requested three-dot.

3. **Explicit `--since <expr>`**
   - Use a time window only when the user explicitly asked for one, or when no exact compare target can be resolved.

4. **Explicit single branch/ref**
   - Validate the ref.
   - If it is different from `HEAD`, compare `REF..HEAD`.
   - If it resolves to the current branch name (for example you are already on `main` and the user says `ship-notes main`), prefer `@{upstream}..HEAD`; if no upstream exists, prefer latest reachable semver tag..HEAD; if neither exists, fall back to `--since="7 days ago"` and say so explicitly.

5. **No explicit scope provided**
   - First choice: `@{upstream}..HEAD` if upstream exists
   - Otherwise: latest reachable semver tag..HEAD
   - Otherwise: `--since="7 days ago"`

### Scope Rules

- **Never silently replace an explicit range with a 7-day window.**
- **Always print the exact scope used** in the final output.
- If the chosen scope is `@{upstream}..HEAD`, describe it as a **local delta vs upstream**, not as a time-based release window.
- If the user wants the exact local-main delta, prefer an explicit range like `origin/main..main`.

### Reference Validation

Use these checks before running logs:

```bash
git rev-parse --verify --quiet <ref>^{commit}
git rev-parse --abbrev-ref HEAD
git rev-parse --abbrev-ref --symbolic-full-name @{upstream}
git tag --merged HEAD --sort=-v:refname | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1
```

## 2. Collect Data from the Resolved Scope

Build the commit set from git first. PR data is optional enrichment only.

### Merge Handling

- Default: exclude merges with `--no-merges`
- If the user passes `--include-merges`, include them
- State which mode you used

### Primary Git Commands

If scope is an exact range:

```bash
git log --format="%H|%h|%an|%ad|%s" --date=short [--no-merges] <range>
git log --reverse --format="%ad" --date=short [--no-merges] <range> | head -n 1
git log --format="%ad" --date=short [--no-merges] <range> | head -n 1
git log --format=tformat: --numstat [--no-merges] <range>
```

If scope is a time window:

```bash
git log --since="<expr>" --format="%H|%h|%an|%ad|%s" --date=short [--no-merges]
git log --since="<expr>" --reverse --format="%ad" --date=short [--no-merges] | head -n 1
git log --since="<expr>" --format="%ad" --date=short [--no-merges] | head -n 1
git log --since="<expr>" --format=tformat: --numstat [--no-merges]
```

Use the `--numstat` output to compute:

- commit count
- total additions
- total deletions

If the chosen scope produces no commits:

- For an exact range, report **"No commits in scope `<range>`"** and stop.
- For a time window, report **"No commits in the last <window>"** and include `git log -1 --format="%ad" --date=relative`.

### Latest Version Tag

Find the latest reachable semver tag from the output side of the comparison:

```bash
git tag --merged <to-ref-or-HEAD> --sort=-v:refname | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1
```

If no version tags exist, say so explicitly.

### Optional PR Enrichment

If `gh` is available and authenticated, use it only to enrich the already chosen git scope.

1. Compute `RANGE_START` and `RANGE_END` from the resolved commit set.
2. Query merged PRs by date range:

```bash
gh pr list \
  --state merged \
  --search "merged:${RANGE_START}..${RANGE_END}" \
  --json number,title,author,mergedAt,labels \
  --limit 200
```

Rules for PR enrichment:

- **Do not let PR results widen or shrink the git commit set.**
- PR mapping can be partial; say so when uncertain.
- If `gh` fails, continue with git-only data and note **"PR data not available"**.
- If `gh pr list` hits the limit, warn that PR enrichment may be truncated.

### Shallow Clone Check

```bash
git rev-parse --is-shallow-repository
```

If shallow, warn that results may be incomplete.

## 3. Classify and Consolidate

Read the resolved commit set and optional PR titles. Categorize changes into:

1. **Breaking Changes**
   - Only when the commit message contains `BREAKING CHANGE:` in the footer, uses conventional-commit bang notation like `feat!:` or `feat(scope)!:`, or the diff removes public API surface.
   - Do **not** treat routine renames, internal refactors, or private helper removals as breaking.

2. **Features**
   - New user-facing capabilities
   - Significant operator-facing workflows

3. **Fixes**
   - Behavior corrections, regressions, crash fixes, recovery fixes, security fixes

4. **Other**
   - Performance
   - Refactors
   - Docs
   - Chore / CI / dependency work

### Consolidation Rules

- Combine related commits into a single bullet when they clearly belong to one feature or one fix stream.
- Preserve important detail in the technical version.
- Compress aggressively in the non-technical version.
- Omit trivial formatting-only noise from summaries, but still keep it in the appendix if the appendix is shown.

### Semver Suggestion

Base the bump strictly on classified impact:

- Any Breaking Changes → **MAJOR**
- Any Features and no Breaking Changes → **MINOR**
- Only Fixes / Other → **PATCH**

If a current version tag exists, show `vCurrent → vNext`. If not, say **"no version tags found"**.

## 4. Output

Generate both versions in a single response. Skip empty categories.

### Technical Release Notes

Use this structure:

```markdown
# Release Notes — [repo-name]
**Scope:** [exact range or time window]
**Period:** YYYY-MM-DD → YYYY-MM-DD
**Bump:** PATCH (v1.2.3 → v1.2.4)
**Stats:** X commits, +A/-D lines
**Merge handling:** no-merges | includes merges
**PR data:** enriched | partial | not available

## Breaking Changes
- **description** — migration path if known (`a1b2c3d`, PR #N)

## Features
- **description** (`a1b2c3d`, PR #N)

## Fixes
- **description** (`a1b2c3d`, PR #N)

## Other
- Summary of improvements, docs, refactors, and chores (`a1b2c3d`)
```

Technical-version rules:

- Include 7-character commit hashes
- Include PR numbers when confidently known
- Include file paths only for breaking changes when they materially help migration
- Always print the exact scope used

### Commit Appendix

Add a `## Commit Appendix` section when **any** of these are true:

- the user passed an explicit range
- the user passed `--full`
- the commit count is greater than 20

Format:

```markdown
## Commit Appendix
- a1b2c3d 2026-04-04 feat: add workspace top nav management controls
- b2c3d4e 2026-04-04 fix: recover session sync failures
```

Do **not** summarize away the appendix. The appendix is the traceability backstop.

### Non-Technical Release Notes

Use this structure:

```markdown
# What's New — [product-name]
**Released:** YYYY-MM-DD

## New Features
- **Name** — what users can now do

## Fixes
- **Issue** — what was broken and is now resolved

## Action Required
- Only include this section if a breaking change affects users
```

Non-technical rules:

- No hashes
- No file paths
- No jargon
- Combine related work into a few clear user-facing bullets
- Omit changes with no visible user or operator impact

## 5. Follow-up

After the notes, mention that `gh release create --draft` is available if `gh` is present. Let the user drive the next step.

## Error Handling

| Situation | Action |
|-----------|--------|
| Not a git repo | Stop and tell the user |
| Explicit ref invalid | Stop and tell the user which ref failed validation |
| Exact range has no commits | Report "No commits in scope <range>" and stop |
| No commits in time window | Report last activity date and stop |
| `gh` not installed or not authenticated | Continue with git-only data, note "PR data not available" |
| No version tags found | State "no version tags found" in semver section |
| Shallow clone detected | Warn results may be incomplete, continue |
| `gh pr list` limit hit | Warn PR enrichment may be truncated |

## Rules

- Resolve scope **before** running `git log`.
- Exact compare ranges beat time windows.
- PR data is enrichment only; git decides the commit set.
- Always print the exact scope used.
- Append a full commit list for explicit ranges, `--full`, or large scopes.
- If the user wants the local branch delta, prefer an explicit compare like `origin/main..main`.
- For monorepos, if the user targets a package path, filter the git scope with `-- <path>` after the range or time selector.

## Anti-Patterns

- **Do not silently answer with "last 7 days" when the user asked for a branch delta.**
- **Do not let PR merged dates define the shipped scope.** Git is the source of truth.
- **Do not overcompress the technical output until most commits disappear.** Use a grouped summary plus appendix instead.
- **Do not classify internal refactors as breaking.**
- **Do not guess the semver bump.** Base it on actual classified impact.
- **Do not use `git diff HEAD~N..HEAD` as a shortcut.** It breaks scope accuracy.
- **Do not prompt with multiple follow-up questions.** Mention the draft-release path once and stop.

## Example Output

Given a repo where the resolved scope is `origin/main..main` with 12 commits and latest tag `v2.7.12`:

### Technical Version

```markdown
# Release Notes — vesper
**Scope:** origin/main..main
**Period:** 2026-04-04 → 2026-04-04
**Bump:** MINOR (v2.7.12 → v2.8.0)
**Stats:** 12 commits, +2820/-652 lines
**Merge handling:** no-merges
**PR data:** not available

## Features
- **Workspace top nav management controls** — adds top-level workspace controls and keyboard shortcuts (`100211f`, `f9b0e07`)
- **Pinned item removal** — lets users remove pinned items directly (`fc27465`)

## Fixes
- **React 19 blank session status recovery** — prevents blank session status states and startup ref loops (`d669489`)
- **Electron dev watcher cleanup** — stops orphaned watcher processes in development (`bc3523f`)

## Other
- Refined recovery briefs and re-entry overlays (`960a1bd`, `bbf100b`, `1dd1454`)
- Polished workspace switching transitions and top-nav UX (`acc2bb8`, `72fa638`, `c28fe7e`, `b2b1d32`)

## Commit Appendix
- 960a1bd 2026-04-04 Clarify recovery brief source status
- bbf100b 2026-04-04 Improve fresh-session recovery briefs
- d669489 2026-04-04 fix: prevent React 19 session status blank screen
- 1dd1454 2026-04-04 refactor: simplify re-entry brief overlay
- acc2bb8 2026-04-04 refactor: polish workspace switch loading transition
- fc27465 2026-04-04 Add Pinned Item removal
- bc3523f 2026-04-04 fix(dev): stop orphaned electron watcher processes
- f9b0e07 2026-04-04 feat: add workspace top nav keyboard shortcuts
- b2b1d32 2026-04-04 polish: distill workspace top nav chrome
- 72fa638 2026-04-04 refactor: replace workspace switch blur with scoped loading states
- c28fe7e 2026-04-04 polish: refine workspace top nav management UX
- 100211f 2026-04-04 feat: add workspace top nav management controls
```

### Non-Technical Version

```markdown
# What's New — Vesper
**Released:** 2026-04-04

## New Features
- **Workspace Top Navigation** — key workspace controls are now easier to access from the top bar
- **Pinned Item Cleanup** — you can now remove pinned items directly

## Fixes
- **Session Status Reliability** — fixed a blank-state issue during session recovery
- **Development Runtime Stability** — improved watcher cleanup during local development
```

## Success Criteria

- [ ] Repository and scope resolved before log collection
- [ ] Exact scope printed in the output
- [ ] Exact ranges never downgraded to a date window
- [ ] Technical and non-technical versions produced in one response
- [ ] Semver bump justified by classified impact
- [ ] Commit hashes included in technical notes
- [ ] Commit appendix included for explicit ranges, `--full`, or large scopes
- [ ] Non-technical notes contain no hashes, file paths, or jargon
- [ ] If `gh` is unavailable, output notes "PR data not available"
- [ ] If no activity exists in scope, output says so explicitly

## Next Steps

- Review the last 7 days only when a true time window is desired: `skill: last7days`
- Compile agent-optimized history: `skill: agent-changelog`
- Persist follow-up work in your preferred issue or todo tracker
