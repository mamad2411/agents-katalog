---
name: backlog-complete
description: >
  Triggers when implementation of a backlog item is finished and ready to ship — e.g.
  "/backlog-complete PROJ-20", "PROJ-20 is done, wrap it up" — and, before push, detects
  planning conflicts and resolves them with the user, then commits and pushes in one pass
  (no conflicts → check, then straight to commit/push; detection by AI, judgment by humans;
  issue key goes in the commit message).
license: MIT
---

# Backlog completion — conflict check & resolve → commit & push

Close a backlog item started with `backlog-kickoff` **after development is done**. Catch
and resolve conflicts **before push**. AI detects; **humans judge.**

## 0. Input
- Argument = the **issue key** (`<KEY>-N`, e.g. `PROJ-20` — a.k.a. ticket). If missing,
  ask the user. Used for the commit message and to judge the change scope.

## 1. Freshen the comparison baseline (local lore vault)
- The source of planning knowledge = the project's **local lore-vault clone** (`raw/` +
  `wiki/concepts/` directly at the vault root). Ensure freshness:
  `git -C ../<project>-lore-vault pull --ff-only -q` (proceed even if it fails).
- vault = the project's lore-vault clone (e.g. a sibling checkout
  `../<project>-lore-vault/`; if it lives elsewhere, ask the user).
- **Do not copy into repo `docs/`.** The conflict check (Step 2) uses the just-pulled
  **lore vault directly as the baseline**. (The PRD copy in repo `docs/` can be stale —
  never use it as the baseline.) Decisions the developer pushes are propagated raw→wiki
  by the **server-side Loremaster host** **(requires the webhook sync pipeline — on the
  roadmap; until it ships, refresh the vault via your server agent or copy pushed
  decision docs into vault `raw/` manually before relying on the conflict baseline)**.

## 2. Conflict check (this item's planning changes ↔ the existing wiki)
- What to compare: **the planning docs added/changed by this backlog item** — the changed
  subset of the docs `LOREMASTER.md` points to (mostly
  `docs/decisions/decision_<KEY>-N.md`). Identify changes via `git status`/`git diff`.
- Baseline: **lore vault `raw/PRD.md` + `wiki/concepts/*.md`** (the refined existing
  decisions and specs). ⚠️ Read the baseline PRD and concepts **directly in the lore
  vault** — the PRD copy in repo `docs/` can be stale; do not use it.
- **A conflict = your change contradicting established knowledge.** Types:
  1. Direct contradiction  2. Number/spec mismatch  3. Decision reversal
  4. Package/integration conflict (e.g. auth via Firebase vs Supabase RLS `auth.uid()`)
  5. Definition/terminology drift.
- ⚠️ **Mitigations (not conflicts — pass):** implementation details left to code
  ("schema columns and exact policy values decided in implementation"), explicit
  deferrals ("policy TBD" · "deferred to next quarter"), empty/draft docs.
- Report only what is actually written. Never invent conflicts. When in doubt, report
  (a missed conflict costs more than a false positive).
- **"Needs real-system verification" items — never close them as terminal output alone
  (force a trackable artifact):** when an item cannot be judged by comparing documents
  and needs checking against something real (a DB, a remote system, a physical device),
  a terminal-only report gets lost in scrollback (real incident: a detected mismatch
  reported only in the terminal went untracked until the user rediscovered it by chance
  and had to close it under a follow-up issue). Handle every such item one of two ways:
  1. **If verifiable right now, verify on the spot** (e.g. query the DB via REST/psql)
     and record the verdict in the relevant decision/progress file.
  2. **If not, leave a trackable artifact** — create a Jira issue (MCP) or add a TODO
     row to the related backlog item's `docs/progress/progress_<KEY>-N.md`. Either way,
     include it in the commit so it gets pushed.
- **No conflicts → skip 3 and go to 4 (commit & push).**

## 3. Conflict resolution (ask the user)
- For each conflict, **present both sides as verbatim quotes with sources (`file:line`)**
  and **ask the user** how to resolve it (AskUserQuestion). Never pick the winning side
  yourself.
- **Before editing the PRD doc, refresh the repo PRD copy from the just-pulled lore
  vault `raw/PRD.md`** (so a conflict fix is never based on a stale copy), and keep the
  edit limited to the resolved contradiction.
- Once the user decides, edit the relevant doc (`docs/decisions/...` or the PRD doc
  `LOREMASTER.md` points to) to remove the contradiction. **Repeat until every conflict
  is resolved.**

## 4. Commit · Push
- Once all conflicts are resolved (or there were none), commit and push **this backlog
  item's entire change set** (code + decision + progress + docs).
  ```bash
  git add -A
  git commit -m "<issue-key> <type>: <summary>"
  git push
  ```
- **Commit message format: `<issue-key> <type>: <summary>`**
  - `<issue-key>` = the issue key (`<KEY>-N`, e.g. `PROJ-20`) — must be included.
  - `<type>` = nature of the change (`feat`/`fix`/`refactor`/`docs`/`chore`/`test`,
    etc. — judged by what was implemented).
  - `<summary>` = one-line summary (in your team's working language).
  - Example: `PROJ-20 feat: OAuth sign-in + app entry skeleton`
- **If the push is rejected:** `git pull --rebase`, then push again (on a rebase
  conflict, do not resolve it yourself — check with the user).
- **After a successful push — Jira status transition:** via the Jira **MCP, transition
  the issue `In Progress` → `Done`** (list the available transitions and pick the
  Done one — status names may be localized in your Jira's language). If it is already
  done, leave it alone.
- **Fallback on transition failure:** if MCP is not connected, ask the user to connect
  Atlassian via `/mcp` and retry. If it still fails, give the user the issue key and
  target status (`Done`) and guide a manual transition (the push already happened —
  do not roll it back).
- The skill is complete once the transition is done.

## Rules
- **Humans judge** — never choose a conflict's resolution direction; ask.
- Never commit or push with conflicts unresolved.
- **Never close a "needs real-system verification" item as terminal output alone** —
  verify and record on the spot, or track it as a Jira issue / progress TODO (Step 2).
- **Issue key is mandatory** in the commit message; keep the
  `<issue-key> <type>: <summary>` format.
- Read only this project's docs and this project's lore vault.
