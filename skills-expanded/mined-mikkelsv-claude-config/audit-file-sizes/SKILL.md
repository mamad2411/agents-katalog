---
name: audit-file-sizes
description: "Audit source files against soft (400) / near-cap (760) / hard (800) line-count caps. Reports violations grouped by tier; respects top-of-file `SIZE-EXEMPT:` comments. Run before merge, when a file feels overgrown, or when the user asks \"is this file too long\" or \"should I split this\". This is the read-only check — to actually execute splits use /refactor-file-sizes."
disable-model-invocation: true
---

# Audit File Sizes

Mechanical scan of source files vs. the soft (400) and hard (800) line-count caps, with a near-cap band called out separately. The line-count work runs in `check-file-sizes.ps1`.

## Mode

- **Mode A** (no args): scope = files changed in the current commit / branch.
- **Mode B** (path arg, e.g. `src/Foo`): scope = the specified directory.
- **Mode C** (`all`): scope = the full source tree.

## Steps

1. **Determine scope:**
   - **Mode A** — collect changed files: `git diff --name-only HEAD` (unstaged) + `git diff --name-only --cached` (staged). If both empty, fall back to `git diff --name-only main...HEAD` (branch scope). If still empty, report "no changes; pass `all` to scan the full tree" and exit.
   - **Mode B** — scope = the supplied path.
   - **Mode C** — scope = repo root.
2. **Resolve the script.** Prefer the project-local copy (per `meta-project-local-skill-copies`, project copies are deliberate forks and may carry a customized extension list):
   - **Project-local**, if `.claude/scripts/check-file-sizes.ps1` exists: `pwsh -NoProfile -File ".claude/scripts/check-file-sizes.ps1"`.
   - **Global fallback**: `pwsh -NoProfile -File "$HOME/.claude/scripts/check-file-sizes.ps1"`.
3. **Run the script** with the invocation from step 2, plus:
   - Mode A: `-Files <list>` (pass the collected files).
   - Mode B: `-Path <dir>`.
   - Mode C: no args.
4. **Parse the JSON** — `hard`, `soft`, `justified`, `totalScanned`. The script emits only two violation buckets; **split its `soft` array at 760 here in the skill** to produce the near-cap tier below. There is no `-NearCap` parameter, so don't look for one.
5. **Report** grouped by tier:
   - **Hard cap (>800, unjustified)** — flagged findings. For each, propose splitting the file (suggest a seam if obvious) or adding a top-of-file `SIZE-EXEMPT: <reason>` comment.
   - **Near-cap (>760, ≤800)** — call these out as their own tier, not buried in the soft list. A file 40 lines from the hard cap will cross it on the next ordinary edit, at which point the split is someone's surprise blocker mid-feature. Flag as "resolve before merge" while the split is still cheap and unhurried.
   - **Soft warnings (>400, ≤760)** — informational. List with line counts; no action required.
   - **Justified exemptions (>800, with `SIZE-EXEMPT`)** — list with reason so a reviewer can verify the justification still holds.
6. **Verdict**: **Clean** / **Soft warnings only** / **Hard-cap violations**.

## Exemption convention

A file is exempt from flagging if its first 10 lines contain a comment matching `SIZE-EXEMPT: <reason>`. Comment style is free (`// SIZE-EXEMPT: ...`, `(* SIZE-EXEMPT: ... *)`, `<!-- SIZE-EXEMPT: ... -->`, `# SIZE-EXEMPT: ...`). The reason is logged in the report. Marker on a file ≤800 lines suppresses soft warnings too.
