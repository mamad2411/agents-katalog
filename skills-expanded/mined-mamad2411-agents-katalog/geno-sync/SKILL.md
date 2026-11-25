---
name: geno-sync
description: Detect and reconcile drift between OpenGeno feature docs (under feat-tree/) and the source code they describe. Walks every L3 doc, reports drift since last_synced_commit, and walks the user through fixing it. Use after vibe-coding sessions, after merging branches, after manual edits that bypassed the workflow, or as a periodic audit. Auto-detects the tree's language from CLAUDE.md.
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep AskUserQuestion"
metadata:
  version: "0.1.0"
---

# /geno-sync

Detect and (optionally) reconcile drift between L3 feature docs and the
code they describe. This is the second of OpenGeno's two skills; run it
on demand when you suspect the tree is out of sync with code.

## Pre-flight

```bash
test -d feat-tree || { echo "no tree — run /geno-init first"; exit 1; }
```

If no tree exists, abort with the message above.

## Detect the tree's language

Before printing anything to the user, determine which language the tree
is written in. Check, in order:

1. `.feat-tree.json` for a `language` field (added by future versions)
2. `CLAUDE.md` for the OpenGeno injection block — look for "文档语言：中文"
   or "Doc language: English" inside the `<!-- BEGIN OpenGeno -->` /
   `<!-- END OpenGeno -->` markers
3. The actual content of `feat-tree/index.md` — if its prose is in
   Chinese, use Chinese; otherwise English

Use that language for **all output of this skill** — drift summary,
clarifying questions, reconciliation prompts, any new doc prose written
during reconciliation.

## Workflow

### Step 1 — Run the drift checker

The script lives next to this skill (or in the global install location):

- `${CLAUDE_PLUGIN_ROOT}/scripts/drift-check.sh`
- `~/.claude/skills/geno-init/scripts/drift-check.sh`
- `.agents/skills/geno-init/scripts/drift-check.sh`

(Note: scripts live under `geno-init/scripts/` because that skill is
where they were installed; `geno-sync` reads them as siblings.)

Run it:

```bash
bash <path-to>/drift-check.sh
```

It prints lines like:

```
DRIFT  feat-tree/auth/login.md  lib/features/auth/login_page.dart  4
STUB   feat-tree/onboarding/welcome.md
BROKEN feat-tree/legacy/old.md  lib/legacy/old_screen.dart
STALE_SHA feat-tree/profile/edit.md  abc123...
```

### Step 2 — Categorize

Bucket the results into:

- **red** (`DRIFT` lines with > 1 commit, especially with non-trivial diff)
- **yellow** (`DRIFT` with 1 commit, or commits that look like
  refactor/format/comment-only)
- **gray** (`STUB` — never synced; awaiting first fill)
- **broken** (`BROKEN` — referenced code file no longer exists)
- **stale** (`STALE_SHA` — recorded SHA is no longer in git history,
  e.g. after a force-push)

For each `DRIFT`, briefly inspect the commits to make the red/yellow
call:

```bash
git log --oneline <last_synced_commit>..HEAD -- <code-path>
```

Heuristic:

- "fix", "format", "lint", "rename", "move" alone → likely yellow
- "add", "remove", "change", "feat", "refactor" → likely red
- Anything that touches > 30 lines → red, regardless of message

### Step 3 — Report

Print the report in the tree's language. Structure:

```
OpenGeno drift report — <project> @ <current-sha>

In sync (n)
Yellow / suspicious (n)
  - <doc-path> — <reason>

Red / likely drift (n)
  - <doc-path>
      <code-path>: <commit-count> commits — <commit subjects, top 3>

Never-synced stubs (n)
  - <doc-path>

Broken code links (n)
  - <doc-path> -> <missing-code-path>

Stale SHA (n)
  - <doc-path> — last_synced_commit not in repo history

Orphan code candidates (suggested, may be intentional)
  - <code-path>
```

The orphan-code section is optional — surface only if the user
explicitly asks or the count is small (< 10). Otherwise it's noise.

### Step 4 — Ask the user how to proceed

Use `AskUserQuestion` (in the tree's language) with options:

1. **Walk through reds together** (recommended)
2. Walk through everything (reds + yellows + grays + broken)
3. Just produce the report, don't change anything
4. Mark a specific doc(s) as in-sync without content edits

Default to option 1.

### Step 5 — Reconcile each chosen doc

For each doc the user wants to reconcile:

1. **Read the L3 doc fresh.**
2. **Read the diff** for each `code:` path:
   ```bash
   git diff <last_synced_commit>..HEAD -- <code-path>
   ```
3. **Walk the doc section by section**, asking which sections need
   updating based on the diff. Edit only those sections. Stay in the
   tree's language.
4. **Cross-link maintenance**: if you removed/added an outgoing
   cross-feature link, update the linked-to doc's "Cross-feature links"
   (or 「跨功能链路」for Chinese trees) section.
5. **Bump frontmatter:**
   - `last_synced_commit:` → current `git rev-parse HEAD`
   - `last_reviewed:` → today

**Critical**: do not bump `last_synced_commit` if you only spot-checked
one section. Either reconcile fully or leave the SHA stale and let the
next run flag it again. Bumping SHAs without verification is the one
failure mode that destroys this whole system.

### Step 6 — Handle other categories

- **Stubs** (`gray`): empty-SHA docs from `/geno-init`. Don't conflate
  with drift. Their meaning depends on `gen_mode` in `.feat-tree.json`:
  - `gen_mode: "stub"` (or missing) — section bodies are placeholders
    (`TODO` / `待补充`). The reconciliation action is **fill**: write
    the prose from a code read, then bump SHA only after the user
    confirms the result is right.
  - `gen_mode: "full"` — section bodies already contain best-effort
    prose generated at init from a code read, but unverified. The
    reconciliation action is **review**: read the doc against the
    current code, correct anything wrong, then bump SHA. Don't bump
    just because prose exists; the SHA is the verification signal,
    not the content.

  Surface both in the report; only act on them when the user asks
  ("fill stubs" or "review full-mode docs" can be its own pass).
- **Broken** (`broken`): for each, ask: was the file moved, renamed, or
  deleted?
  - Moved/renamed → edit the doc's `code:` to the new path.
  - Deleted → ask if the feature was removed entirely. If yes, archive
    the doc (move to `feat-tree/_archived/<original-path>.md` and remove
    its row from the L2 index). If no, the user has a problem to solve
    in the tree's structure.
- **Stale SHA** (`stale`): the recorded SHA isn't in history (likely
  force-push or branch rebase). Treat the doc as never-synced (gray) and
  reconcile from current HEAD.

### Step 7 — Final report

Print, in the tree's language:

- Reconciled (n) docs
- Skipped (n) docs (left as drift for next time)
- Stubs remaining (n) — informational
- Final state — should be all-green if user reconciled all reds

## When to run

- After any session that changed code without going through the
  documented workflow (vibe coding, manual edits, merge from another
  branch)
- Periodically (weekly is a reasonable cadence on active projects)
- Before relying on doc content for a non-trivial task
- When the Stop hook reports drift

## Distinction from the Stop hook

The Stop hook (installed by `/geno-init`) runs `drift-check.sh`
**non-interactively** at session-end and either warns or blocks. It
doesn't fix anything.

`/geno-sync` is the **interactive** counterpart: it runs the same
checker but walks the user through reconciliation.

## Anti-patterns

| Don't | Why |
|-------|-----|
| Bulk-bump all SHAs to current HEAD without per-doc review | Defeats the whole purpose; produces a "fresh" tree that doesn't actually match code |
| Treat all yellows as noise | Refactors sometimes change behavior subtly; spend 30 seconds on each |
| Auto-edit doc content based on git diff alone | Risk of describing "what changed" rather than "current behavior" — needs judgment, not diff translation |
| Conflate stubs with drift | Stubs are unfinished bootstrapping, not drift. Different action |
| Bump a `gen_mode: "full"` doc's SHA without re-reading the code | Full-mode prose is unverified by definition; bumping the SHA without verification destroys the entire drift system |
| Switch language mid-reconcile | The tree's language is fixed at init time; respect it |
| Run sync at session-end of every change | That's what the Stop hook is for. `/geno-sync` is for catching what other people / sessions did |
