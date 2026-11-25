---
name: backlog-kickoff
description: >
  Triggers when you start implementing an assigned backlog item — e.g. "start PROJ-12",
  "kick off PROJ-6", "beginning work on this backlog item" — and lays down that item's
  empty decision-doc skeleton (docs/decisions/decision_<KEY>-N.md, format only; the body
  is filled during development) plus its task checklist (docs/progress/progress_<KEY>-N.md),
  consulting the PRD, project wiki (graphify), and codebase for the checklist, identifying
  metadata, and developer orientation (the decision doc syncs as raw and is tracked by the
  wiki; progress is a dev-only local file).
license: MIT
---

# Backlog kickoff — create decision + progress

You assist the developer implementing this project. Given one backlog item, set up its
**empty decision-doc skeleton (decision)** and **task checklist (progress)**.
**Leave the decision body empty — the developer fills in real decisions while implementing.**
No guessing, no invention — blanks stay blank.

## 0. Confirm the backlog key (varies per project — never hardcode)
- **`<KEY>` is this project's Jira/space key.** Derive it, do not assume:
  - from existing `docs/decisions/decision_*.md` filenames (e.g. `decision_PROJ-7.md` exists → KEY=`PROJ`), or
  - from the backlog-item key the user said (e.g. "start PROJ-6" → KEY=`PROJ`, N=`6`), or from the Jira project key.
- Every filename and in-doc backlog-item reference uses this `<KEY>-N` (each project has its own key — the examples here use `PROJ`).

## 1. Context gathering (for the checklist, metadata, and orientation)
Collect context to ① build the progress checklist, ② fill the decision doc's identifying
metadata (`prd_ref`, title), and ③ orient the developer in the prior decision flow.
**Do not fill the decision body.**

0. **Freshen the repo and the plan — before anything else.**
   **(1) Pull the project repo.** Kicking off unaware of backlog items teammates completed
   and pushed in parallel (code, validators, seed-structure changes, etc.) breaks the
   checklist's premises (real incident: a kickoff almost started assuming an old data
   format, unaware a teammate had already shipped the new-format validator and archived
   the old seeds).
   - `git status --short` first — **if uncommitted changes exist (especially decision/progress),
     tell the user and confirm before pulling** (a rebase or sync could clobber them).
   - If clean, `git pull --rebase -q`. On a rebase conflict, do not resolve it on your own — stop and report.
   - If incoming commits (`git log --oneline ORIG_HEAD..` or the pull output) show changes
     overlapping this backlog item, factor them into context steps 1–4 below.

   **(2) Freshen the plan (local lore vault clone).**
   The single home of the plan is the **local lore vault clone** (Obsidian auto-pulls it, so
   it is always current — including PRD changes made in Slack and resolved decisions).
   Before kickoff, update it and read the context below **directly from the lore vault**
   (do not copy into repo `docs/`).
   - Find the project's lore-vault clone (usually a sibling checkout of this repo, e.g.
     `../<project>-lore-vault`; `raw/` and `wiki/concepts/` sit directly at the vault root).
     Freshen: `git -C ../<project>-lore-vault pull --ff-only -q` (proceed even if it fails).
   - From here on, reference the PRD, prior decisions, and concepts **directly in the vault
     `raw/` (`raw/PRD.md`, `raw/decisions/*`) and `wiki/concepts/`**. Repo `docs/` is where the
     developer authors decisions; the plan's source is the lore vault — the PRD copy in repo
     `docs/` can be stale, so read raw.
   - (repo→wiki publishing is automatic: when the developer pushes a decision, the
     **server-side Loremaster host** propagates it raw→wiki. Nothing to sync locally.)
1. **The Jira issue (`<KEY>-N`, a.k.a. ticket) — the kickoff's starting point.** Fetch this issue
   via the Atlassian/Jira **MCP tools** (summary, description, **acceptance criteria**, priority,
   assignee, status, comments). It is the primary basis for "what to build and when it counts as done."
   - If MCP is not connected, ask the user to connect Atlassian via `/mcp` or to paste the
     issue essentials (summary, acceptance criteria). Never fill by guessing.
   - The issue's **acceptance criteria** are the backbone of the progress checklist
     (1 criterion → verifiable task steps). Pull the decision title and `prd_ref` from the issue too.
   - **Reflect the kickoff — status transition:** since this backlog item is being *started*,
     transition the issue **`To Do` → `In Progress` via the Jira MCP** (list the available
     transitions and pick "In Progress" — status names may be localized in your Jira's language).
     The assignee explicitly kicked off, so proceed without separate approval. If it is already
     `In Progress` or in a done state, leave it alone.
2. **PRD** (lore vault `raw/PRD.md` — the plan's source): the *what/why/scope* of the
   feature/policy this backlog item implements (connect the issue to the PRD section it
   implements). The PRD copy in repo `docs/` can be stale, so read raw.
3. **Project wiki — graphify query (prior backlog decisions, connected concepts):**
   - Locate the wiki vault (e.g. the sibling checkout `../<project>-lore-vault/`; if absent,
     `git clone git@github.com:your-org/<project>-lore-vault.git`).
   - `graphify query "<backlog topic>" --graph <vault>/graphify-out/graph.json` narrows the
     reading to **related concepts and prior decisions** (e.g. for an auth item, a prior
     "settled on Firebase Auth" decision surfaces). `graphify explain "<concept>"` for connections.
   - If there is no graph, fall back: read the lore vault `raw/decisions/*.md` (prior decisions) directly.
   - **Purpose**: surface the related decisions up front so that when the developer later
     fills the body, it *does not contradict prior decisions* (e.g. if auth is already
     Firebase, they know that premise).
4. **Codebase**: find the files/packages this backlog item will touch and read the current
   structure and related code (the reference tables in `CLAUDE.md`, related directories).

## 2. Create ① `docs/decisions/decision_<KEY>-N.md` — **empty decision skeleton** (format only; the developer fills the body)
At kickoff, **how to implement is not yet decided.** So lay down only a **clean skeleton**
for the decision doc and leave the body **empty**. The developer fills real decisions into
this skeleton while implementing (once filled and stable, it is pushed → the wiki tracks it).
Use **exactly the format below** — a **decision-log table** (header + 1 empty row). The
developer fills one row per decision as they arise. **Never fill it by guessing.**
```markdown
---
backlog: <KEY>-N
doc_type: decision
status: draft            # becomes stable once it reflects the implementation
prd_ref: "§"             # related PRD section (fill if known)
updated: <YYYY-MM-DD>
tags: []
---

# <KEY>-N · <backlog item title>

> Format: `date | decision | rationale | alternatives`
> Record the **implementation decisions that take shape** while implementing per the PRD (§<N>)
> — library, approach, schema: what to build and how. If the plan itself must change,
> request it in Slack, not here.

| Date | Decision | Rationale | Alternatives |
|---|---|---|---|
|  |  |  |  |
```
- Fill **only the identifying metadata** — `backlog`/`updated`/title, plus the `prd_ref`
  *confirmed* from Jira/PRD (and the `§N` in `> ... PRD (§<N>)`). **Leave the table data row
  blank** — header + 1 empty row only.
- **The developer adds one row per decision while implementing** (1 row = 1 decision:
  `date | decision | rationale | alternatives`; dates are `YYYY-MM-DD` in the team's timezone
  — `TZ="$TEAM_TZ" date +%F`, with `TEAM_TZ` set to your team's IANA timezone, e.g.
  `America/New_York`). The empty row is filled with the first decision.
- Never fill the table by guessing. If implementation forces a PRD change (e.g. the PRD says
  "free" but a paid module is required), do not push it through in code/docs — request the
  plan change in Slack (backlog-complete catches that conflict as a gate).

## 3. Create ② `docs/progress/progress_<KEY>-N.md` — task checklist (dev-only, not part of raw)
Break this backlog item's PRD scope into **small, genuinely implementable steps** (the
decision doc is still an empty skeleton, so base this on the PRD and code). (This file does
not go to the wiki; it is for dev tracking.)
```
# <KEY>-N — <title> progress

> Backlog item: <KEY>-N · Decisions: docs/decisions/decision_<KEY>-N.md

- [ ] <subtask 1 — concrete, verifiable>
- [ ] <subtask 2>
- [ ] ...
```
- Example (login = Firebase): `[ ] Create Firebase project` · `[ ] Enable Google provider + OAuth consent screen` ·
  `[ ] Install and configure the firebase SDK` · `[ ] Wire ID token → Supabase custom claims` ·
  `[ ] Login screen + error handling` · `[ ] e2e login test`.
- Checkable units (neither too fine-grained nor too lumped).

## 4. Wrap-up — **create only, no auto-push**
- Create the two files and ask the user to **review** (does the progress checklist cover the
  PRD scope; are the decision skeleton and metadata right).
- ⚠️ **The decision doc is an empty skeleton — filled during development.** When a decision
  takes shape against reality mid-implementation, write the body then (e.g. "Google login" →
  turns out "the Google login API requires a subscription" → that decision goes into the
  decision doc, the steps into progress). Such mid-implementation decisions are **not plan
  changes** (the PRD stands). Only when the plan itself must change, request it in Slack.
- **This skill must not git push.** The decision doc is pushed **once its body is filled by
  the real implementation and stable** (usually during/after development, in the developer's
  normal commit/push flow). The **server-side Loremaster host** then propagates it raw→wiki so
  **the whole project learns of that implementation** (if there is a conflict, the gate catches
  it then — that is fine). Pushing an empty skeleton or a soon-to-change draft makes the wiki
  track phantoms and duplicates detection — do not.
- progress: update the checkboxes while implementing. Even if pushed, it does not enter the
  wiki (dev tracking, not part of raw).
