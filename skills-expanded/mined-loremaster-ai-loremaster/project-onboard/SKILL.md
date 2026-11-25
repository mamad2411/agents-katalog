---
name: project-onboard
description: >
  Triggers once per project, when migrating an existing in-flight project into the
  backlog-file model — e.g. "/project-onboard" — and (1) detects and resolves
  PRD/decisions/progress conflicts, (2) consolidates the accumulated single decisions
  and progress files into the new format **one file each** (decisions = table form,
  progress = completed items only), (3) tidies the folder structure and LOREMASTER.md,
  after which the project switches to per-backlog-item files (detection by AI,
  judgment by humans).
license: MIT
---

# Project onboarding — legacy docs to the backlog-file model (one-time)

AI detects and converts; **humans judge conflicts and completion.** Run once per project.

## 0. Inventory — find the planning docs (structure varies per project → search broadly)
Structures differ, so **assume no names or locations — search wide.** Cover filenames
(English or your team's language), locations (root, `docs/`, subfolders), and both
standalone and embedded forms.
1. **Collect candidates (filenames):** scan the whole repo case-insensitively —
   - PRD: `prd` · `spec` · `requirements`.
   - decisions: `decision` · `ADR` · a `decisions/` folder.
   - progress: `progress` · `roadmap` · `dev*plan` · `todo` · a `progress/` folder.
   - Example: `find . -path ./.git -prune -o -iregex '.*\(prd\|decision\|progress\|roadmap\|plan\|spec\)\.*md' -print`
     (supplement with `grep -ril`). If your team names docs in another language, extend
     the keyword lists and regex with those equivalents.
2. **Validate candidates (content):** judge by content even when the filename does not
   match — decisions = decision blocks (date/number + decision/rationale/alternatives),
   decision logs / progress = checklists (`[x]`/`[ ]`), round/phase tracking / PRD =
   product requirements, feature specs.
3. **Embedded forms:** decisions/progress may live **as sections inside another doc**
   rather than standalone files (e.g. a `## Decision history` section in the PRD, a
   single DEV_LOG mixing decisions + progress) → extract and convert just that section
   and remove it from the host doc.
4. **Already folder-form (`docs/decisions/*.md`, one file per backlog item)** → that
   kind needs no onboarding — skip it.
5. **Confirm:** compile what counts as PRD/decisions/progress **into a list and get the
   user's confirmation** (ambiguous or multiple candidates → always ask). Mark missing
   kinds "none" and skip their consolidation (e.g. no decisions file → skip the
   decisions consolidation). If `LOREMASTER.md` exists, use its manifest as candidate
   input too.

## 1. Conflict check & resolution (PRD ↔ decisions ↔ progress)
- Detect, across the three docs: **contradictions · decision reversals · staleness**
  (the PRD changed but old decisions/progress no longer match) · **under-specification**.
- For each conflict, **present both sides as verbatim quotes with sources (`file:line`)**
  and **ask the user** to resolve it (never pick the winning side yourself).
- Once the user decides, edit the relevant doc to remove the contradiction. **Resolve
  every conflict** before the next step.

## 2. Consolidate decisions → `docs/decisions/decisions_legacy.md` (table form)
Convert **every decision** in the decisions source you found (standalone file or a
section inside another doc) into one table:
```markdown
---
backlog: legacy
doc_type: decision
status: stable
updated: <YYYY-MM-DD>
tags: []
---

# <project> · Legacy decision log (onboarding consolidation)

> Format: `date | decision | rationale | alternatives`. Consolidates pre-onboarding
> decisions. Decisions from here on go to `decision_<KEY>-N.md`.

| Date | Decision | Rationale | Alternatives |
|---|---|---|---|
| 2026-05-25 | <one-line decision> | <rationale> | <alternatives> |
| ... | ... | ... | ... |
```
- **1 decision = 1 row.** Compress each source block's decision/rationale/alternatives
  into its cell (preserve the substance, one line). Extra fields like "impact" fold into
  the decision cell or drop. Never distort or invent beyond the source.
- **Reversals & duplicates:** when a newer decision on the same topic supersedes an old
  one, keep only the newest as valid and mark the old row `(superseded → YYYY-MM-DD)`.
- Sort by date (oldest → newest); dates are `YYYY-MM-DD` in the team's timezone
  (`TZ="$TEAM_TZ" date +%F`, with `TEAM_TZ` set to your team's IANA timezone, e.g.
  `America/New_York`). When conversion is done, **remove the decisions source**
  (standalone file → `git rm`; section inside another doc → delete that section).

## 3. Consolidate & prune progress → `docs/progress/progress_legacy.md` (completed only)
Review each item in the progress source and keep **only what is complete**:
- **Complete (`[x]`)**: keep.
- **Incomplete (`[ ]`) and no longer needed** (dropped from scope, abandoned): delete.
- **Incomplete (`[ ]`) and genuinely remaining work**: leave it out of legacy and
  **surface it to the user as a "future backlog candidates" list** (for the PM to turn
  into backlog-proposal/Jira issues later).
- ⚠️ **Verify completion against the code and actual state** (never trust checkboxes
  alone). Ambiguous → ask the user.
```markdown
# <project> · Legacy progress (completed consolidation)

> Consolidates work completed up to onboarding. Progress from here on goes to
> `progress_<KEY>-N.md`.

- [x] <completed item>
- [x] ...
```
- Result: **all `[x]`**. **Remove the progress source** (standalone file → `git rm`;
  section inside another doc → delete it).

## 4. Structure & manifest cleanup
- Ensure the `docs/decisions/` and `docs/progress/` folders exist (create if missing).
- **Update LOREMASTER.md**: old single `docs/DECISIONS.md` → `docs/decisions/` (folder
  entry); **remove any progress entry** (progress is not part of the lore vault —
  repo-local only); keep the PRD. Example:
  ```
  - `docs/<Project>_PRD.md`
  - `docs/decisions/`
  ```
- If `.claude/skills/` lacks `backlog-kickoff`/`backlog-complete`, or the repo root
  lacks `.mcp.json`, tell the user to add them (needed for backlog work from here on).

## 5. Wrap-up
- Report a change summary: N conflicts resolved · M decision rows consolidated ·
  K completed items kept · **L future backlog candidates** (with the list).
- **Commit & push** (e.g. `chore: onboard to the backlog-file model — consolidate
  legacy decisions/progress`).
- From here on, each backlog item runs `/backlog-kickoff <ISSUE>` → develop →
  `/backlog-complete <ISSUE>`, which add `decision_<KEY>-N.md` / `progress_<KEY>-N.md`
  to the folders.

## 6. Post-push verification — confirm vault sync + initial conflict pass (final step, never skip)
If a **pre-onboarding PRD snapshot lingers** in the lore vault's `raw/`, later backlog
items hit stale-conflict false positives. Do not stop at the push — confirm the vault
actually caught up.
1. **Confirm vault sync:** after commit & push, freshen the project's lore-vault clone
   (e.g. a sibling checkout `../<project>-lore-vault`):
   `git -C ../<project>-lore-vault pull --ff-only -q`, then check that the PRD and
   decisions in the vault `raw/` (`../<project>-lore-vault/raw/`, directly at the vault
   root) are **byte-identical** to the repo `docs/` documents just pushed, via `cmp`
   (e.g. `cmp ../<project>-lore-vault/raw/PRD.md docs/<Project>_PRD.md`, and each
   decisions file likewise).
   - Different = the old snapshot lingers. Wait for the Loremaster host's server-side
     raw sync to propagate (webhook pipeline — on the roadmap; until it ships, copy the
     docs into vault `raw/` manually or via your server agent), retrying the pull
     **up to 15 minutes**, then **re-check until identical**.
2. **One initial conflict pass:** once identical, run **one explicit consistency check**
   of PRD ↔ decisions (including `decisions_legacy.md`) — same criteria as §1
   (contradictions, number mismatches, staleness). But **superseded old decisions
   (marked `(superseded → ...)`) are not conflicts.** Present any findings as verbatim
   quotes with sources and let **the human judge**.

## Rules
- **Humans judge** — ask whenever conflict resolution or completion status is ambiguous.
  Never invent decisions or completions.
- One-time: after consolidation, no old single decisions/progress file may remain (the
  switch to per-backlog-item folders is complete).
- Read only this project's docs (never another project's).
