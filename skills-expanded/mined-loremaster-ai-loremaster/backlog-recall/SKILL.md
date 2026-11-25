---
name: backlog-recall
description: >
  Triggers after a large-scale plan change (PRD edited in Slack → reflected in the
  wiki) when an already-started backlog item must be re-kicked-off against the new
  plan — e.g. "/backlog-recall PROJ-32" — freshening the local lore vault, discarding
  the old decision/progress, and re-running backlog-kickoff (the re-kickoff reads the
  lore vault directly).
license: MIT
---

# Backlog re-kickoff — absorb a large-scale plan change

When the plan changes substantially in Slack, an already-started backlog item's
`decision`/`progress` are based on the old plan — discard them and **re-lay them
against the new plan**.

## 0. Input
- Argument = the **issue key** (`<KEY>-N`, e.g. `PROJ-32` — a.k.a. ticket). If missing, ask the user.

## 1. Get the latest plan (local lore vault)
- vault = the project's lore-vault clone (e.g. a sibling checkout `../<project>-lore-vault/`; `raw/` and `wiki/concepts/` sit directly at the vault root). Freshen: `git -C ../<project>-lore-vault pull --ff-only -q` (proceed even if it fails).
- **Do not copy into repo `docs/`** — the re-kickoff (backlog-kickoff in Step 3) reads the PRD, decisions, and concepts **directly from the lore vault `raw/` and `wiki/concepts/`**. (The plan's source = the lore vault.)

## 2. Discard this item's old artifacts
- Delete `docs/decisions/decision_<KEY>-N.md` + `docs/progress/progress_<KEY>-N.md` (based on the old PRD — void).

## 3. Re-kickoff — run backlog-kickoff
- **Run the backlog-kickoff skill** with `<issue key>` → regenerates the empty decision skeleton + progress against the new PRD/wiki. (If the Jira status is already `In Progress`, leave it.)

## Rules
- **Do not git push.** Leave the docs deletions in the working tree (backlog-complete commits and pushes after development).
- Do not edit the PRD itself here — this skill only pulls the plan *already changed in Slack* down locally and re-kicks off.
- Read only this project's docs and this project's lore vault.
