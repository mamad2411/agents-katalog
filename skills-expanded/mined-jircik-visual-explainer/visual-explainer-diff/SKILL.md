---
name: visual-explainer-diff
description: "Use when asked to visualize, explain, or document what changed between two git refs in a codebase. Triggers: 'show what changed in this PR', 'visualize the diff', 'explain the changes between main and this branch', 'generate a change report', 'what did this commit change architecturally', or any request to understand code changes visually rather than via raw git diff."
---

# Visual Explainer — Diff

Generate an interactive HTML dashboard that visually explains what changed between two git refs — added, modified, and deleted files with annotated purpose, which architecture layers were touched, and how primary data flows shifted.

Companion skill to `visual-explainer`. That skill explains a codebase at rest; this one explains a codebase in motion.

## When to Use

- User asks to visualize, explain, or document a diff, PR, or commit range
- User wants a change report for review or release notes
- User needs to understand the architectural impact of a branch before merging
- User wants to onboard a reviewer to a large PR

## When NOT to Use

- Single-line or single-file diffs (just show the diff inline)
- Commits with no meaningful code change (formatting, lockfile bumps)
- The user wants a textual changelog or PR description (use a different tool)

## Input

Two git refs. Resolution order:

1. Explicit args from the user (`main..feature/x`, `HEAD~5 HEAD`, `<sha1> <sha2>`)
2. If on a feature branch: `<default-branch>..HEAD` (detect default via `git symbolic-ref refs/remotes/origin/HEAD`)
3. Fallback: `HEAD~1..HEAD`

Confirm the chosen range with the user before running if it was inferred.

## Output

A self-contained `./visual-explainer/diff.html` file in the project root. Same CDN-only stack as `visual-explainer` (Mermaid.js, Tailwind CSS, Inter font). Does not overwrite an existing `index.html`.

## Process

### Phase 1: Collect

1. **Resolve the range.** `git merge-base <base> <head>` → use the merge-base as `BASE`, the tip as `HEAD`.
2. **List changed files.** `git diff --name-status BASE..HEAD` → bucket into Added / Modified / Deleted / Renamed.
3. **Get stats.** `git diff --numstat BASE..HEAD` for per-file insertions/deletions.
4. **Get commit list.** `git log --oneline BASE..HEAD` for the commit narrative.
5. **Skip noise.** Lockfiles, generated code, snapshot files, `dist/`, `build/`, vendored deps. Same skip list as `visual-explainer`.

### Phase 2: Analyze

For every changed Core file:

1. **Read the file at HEAD** (`git show HEAD:<path>`).
2. **Read the file at BASE** for modified/deleted files (`git show BASE:<path>`).
3. **Classify the change kind:**
   - **New capability** — a new export, route, command, or model
   - **Behavior change** — existing function logic changed
   - **Refactor** — structure changed but behavior preserved
   - **Removal** — code deleted or capability removed
   - **Config/infra** — non-code change
4. **Locate it in the architecture.** Map each file to a layer (route / controller / service / repository / model / infra / test). Reuse the layer model from `visual-explainer` if a prior `index.html` exists.
5. **Detect flow changes.** If a route/handler/entry-point file changed, trace the new flow at HEAD and compare it to BASE. Note added/removed steps.
6. **Detect API surface changes.** New or removed exports, new or removed CLI flags, new or removed routes, schema migrations.

### Phase 3: Generate

Create `./visual-explainer/diff.html` with five tabs:

#### Tab 1: Summary

- Header: `<base-ref> → <head-ref>` with short SHAs and commit count
- Stats row: files changed, insertions, deletions, commits
- One-paragraph summary of the change's intent (inferred from commit messages + file changes)
- "Risk surface" callouts: changes touching auth, payments, migrations, public APIs, infra

#### Tab 2: Architecture Delta

- Mermaid diagram of the architecture
- Each box color-coded by change intensity: untouched (gray), modified (blue), added (green), removed (red)
- Arrows that were added or removed are dashed with a legend
- Brief text below explaining which layers absorbed the change

#### Tab 3: Changed Files

- Three collapsible sections: **Added**, **Modified**, **Deleted** (and **Renamed** if any)
- Each file row shows: path, +/- counts, change-kind badge, one-sentence "what changed and why"
- For modified files, an expandable section with the *behavioral* delta (not the raw diff — describe what the code now does that it didn't before)
- Skip-list files hidden by default with a toggle

#### Tab 4: Flow Delta

- For each primary flow that changed, two side-by-side Mermaid sequence diagrams: BASE on the left, HEAD on the right
- New steps highlighted green, removed steps red, modified steps blue
- Annotated with file names so reviewers can jump into the code

#### Tab 5: API Surface

- Three tables: **Added**, **Changed signature**, **Removed**
- Columns: kind (function / route / CLI flag / schema field / env var), name, file, breaking-change indicator
- Anything marked breaking gets a prominent warning banner at the top of the tab

### HTML Implementation Rules

Same as `visual-explainer`:

1. Single file, CDN-only.
2. Dark theme: `#0a0a0a` bg, `#141414` cards, `#262626` borders, `#e5e5e5` text, `#a3a3a3` muted.
3. Diff-specific accents: added `#22c55e`, removed `#ef4444`, modified `#3b82f6`.
4. Mermaid dark theme with `startOnLoad: true`.
5. Vanilla JS only. Print-friendly via `@media print`.

### Quality Checklist

Before writing the file, verify:

- [ ] The ref range was confirmed with the user (or explicitly provided)
- [ ] Every Core changed file has been read at both BASE and HEAD
- [ ] Behavioral deltas describe *what changed*, not raw line diffs
- [ ] At least one flow diagram pair exists if any entry-point/handler changed
- [ ] Breaking changes are flagged prominently
- [ ] Mermaid diagrams use valid syntax
- [ ] No "TODO" or placeholder text

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reproducing `git diff` line-by-line | Describe behavior change, not text change |
| Missing the BASE side of flow diagrams | Always render both sides for changed flows |
| Calling everything "modified" | Distinguish refactor from behavior change — readers care |
| Hiding breaking changes in the file list | Surface them in the Summary tab and the API Surface tab |
| Overwriting an existing `index.html` | Always write to `diff.html`, never `index.html` |
| Forgetting renames | `git diff --name-status -M` and present them as a separate group |
| Treating a 200-commit range like a 5-commit range | If commits > 50, suggest narrowing the range first |

## Interaction with `visual-explainer`

If `./visual-explainer/index.html` already exists:

- Reuse its architecture model and layer assignments instead of re-deriving them
- Link from `diff.html` back to `index.html` ("See full architecture")
- Do not regenerate `index.html` unless asked

If it doesn't exist, the diff dashboard stands alone but suggest running `visual-explainer` first for full context.

## Example Invocations

```
User: "Visualize what changed in this PR"
→ Detect base branch → confirm range → generate ./visual-explainer/diff.html

User: "Show me the architectural impact of the last 10 commits"
→ Range = HEAD~10..HEAD → generate diff.html

User: "Compare main and feature/payments and explain the diff"
→ Range = main..feature/payments → generate diff.html
```
