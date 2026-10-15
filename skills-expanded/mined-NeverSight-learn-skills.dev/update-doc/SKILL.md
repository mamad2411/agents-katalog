---
name: update-doc
description: >
  Sync documentation with code changes. Scans for README, CLAUDE.md, docs/ pages, and skills
  that reference behavior the current branch modifies, and updates or flags them. Use when
  user says 'update docs', 'sync documentation', 'is our documentation current', 'docs are
  stale', or 'update READMEs after this refactor'. Do NOT use for writing a fresh feature
  doc (use document-feature) or a new ADR (use document-decision).
allowed-tools: Read, Grep, Glob, Bash, Edit
---

# Update docs — sync documentation with the current diff

Scan the repo for documentation that references behavior touched by the current branch, and either update it in place or flag it for human review.

## Before You Start

- `principles/04-file-references-over-snippets.md` — why snippets go stale and file references don't.
- `CLAUDE.md` at root and at every subdirectory — ambient docs most likely to drift.
- `docs/`, `README.md`, `CONTRIBUTING.md`, inline `*.md` files across the repo.

## Step 1: collect what changed

```bash
git diff origin/main...HEAD --name-only > /tmp/changed-files.txt
git diff origin/main...HEAD --stat

# What symbols / functions / endpoints changed? Harder — look at the diff itself.
git diff origin/main...HEAD -- '*.py' '*.ts' '*.js' '*.go' '*.rs' \
  | grep -E '^[+-](def |class |function |const |export |impl )' \
  | sort -u
```

Note:

- New files added.
- Removed files.
- Renamed symbols or moved files (these break every doc that referenced the old path).
- Changed function signatures or behavior.
- New or removed config options.

## Step 2: find docs that reference the changed code

```bash
# Find every markdown file that mentions a changed file path or symbol
# (Adapt the search terms based on step 1's findings.)
find . -type f \( -name '*.md' -o -name '*.mdx' \) \
  -not -path './node_modules/*' -not -path './.git/*' \
  -not -path './.claude/worktrees/*' \
  | xargs grep -l -E '{changed-path-or-symbol}' 2>/dev/null
```

For each hit, open the file and assess:

| Situation | Action |
|---|---|
| The doc's claim is still accurate | Skip — no update needed. |
| The doc names a file/symbol that was renamed | Update the reference. |
| The doc embeds a snippet that no longer matches the source | Replace the snippet with a file reference (principle 04). |
| The doc describes old behavior | Rewrite to match the new behavior, OR flag and ask the user. |
| The doc is now irrelevant | Delete or merge into another doc. |

## Step 3: classify each doc hit

Put each doc in one of three buckets:

- **Safe to auto-update** — rename updates, trivially corrected file paths. Apply the edit.
- **Needs human review** — behavior changes, removed features, cross-doc inconsistencies. Flag; don't edit.
- **Delete candidate** — the doc is about code that no longer exists. Flag; don't delete.

## Step 4: apply the safe updates

For each **Safe** item, use `Edit` to make the change. Prefer small, targeted edits — change one path or symbol at a time, not a wholesale rewrite.

After edits:

```bash
# Lint markdown if the project does
mdformat --check docs/ 2>/dev/null || true

# Re-run the docs site build to catch broken links
# (pull the command from CLAUDE.md Quick Reference)
# pnpm docs:build  OR  mkdocs build --strict  OR  yarn build
```

## Step 5: present the flag list

For everything in **Needs human review** and **Delete candidate**, print a table:

```markdown
## Docs needing review

| File | Line | Issue | Proposed action |
|---|---|---|---|
| `docs/guides/auth.md` | 42 | Describes old OAuth flow removed in this PR | Rewrite or delete |
| `README.md` | 18 | Mentions `src/legacy/` which this PR deletes | Remove the paragraph |
| `packages/api/CLAUDE.md` | 55 | References behavior of `OldClass` renamed to `NewClass` | Update references |

## Delete candidates

| File | Reason |
|---|---|
| `docs/tutorials/legacy-setup.md` | The "legacy-setup" path this documents is gone |
```

The user picks actions; apply them next pass.

## Step 6: update `CLAUDE.md` "Things to Know" if a gotcha was resolved

If this PR fixed or changed a documented gotcha in `CLAUDE.md`:

- **Fix made the gotcha obsolete** → remove the entry.
- **Fix changed the gotcha** → rewrite the entry.
- **This PR introduces a new gotcha** → add it.

Validate after:

```bash
```

## Verify

```bash
# Every auto-updated doc still builds
# (project-specific build command)

# No markdown file references a file that no longer exists
for md in $(find . -type f -name '*.md' -not -path './node_modules/*' -not -path './.git/*'); do
  grep -oE '`[a-zA-Z_./-]+/[a-zA-Z_.-]+`' "$md" | tr -d '`' | while read p; do
    [ ! -e "$p" ] && echo "STALE: $md references missing $p"
  done
done | sort -u | head -30
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Auto-updating a behavior description because the path stayed the same but the behavior changed | Behavior changes go in the "human review" bucket, not the "safe" bucket. Be conservative. |
| Embedding an updated snippet instead of referencing the file | Principle 04: replace snippets with file references. The snippet will rot again. |
| Deleting a doc because the current PR makes it look stale, when it describes behavior that's still shipping | Verify the *current state of the code* matches the doc's claim before declaring the doc stale. |
| Skipping subdirectory `CLAUDE.md` files | Every scope can have its own `CLAUDE.md`. Scan the full tree, not just root. |
