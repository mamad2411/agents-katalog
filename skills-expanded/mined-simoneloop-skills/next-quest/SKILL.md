---
name: next-quest
description: >-
  Given the project currently open in the working directory, pull its Jira
  issues via the Atlassian MCP server, rank them by priority while honoring
  blocker/blocked-by links, and hand back the single next task to develop
  (plus the ordered shortlist behind it). Use when the user asks "what should
  I work on next", "what's my next Jira task", "give me the next ticket",
  "cosa sviluppo adesso", "qual è il prossimo task", or wants their backlog
  triaged into one actionable pick for the current repo.
---

# next-quest

<!--
  Standing instructions. Keep lean. The whole flow is: resolve project key →
  query Jira via MCP → classify blocked/blocking from issue links → rank →
  return the next task. No bundled scripts or references needed.
-->

## Setup (run this FIRST, before any other step)
This skill talks to Jira through the **Atlassian MCP server** (Rovo). It needs no
CLI binaries and no secrets of its own — auth is handled by the MCP connection.

1. **Verify the Atlassian MCP is connected.** Use `ToolSearch` with query
   `atlassian jira` and confirm tools like `searchJiraIssuesUsingJql`,
   `getJiraIssue`, and `getAccessibleAtlassianResources` are available. If they
   don't appear, check whether the server merely needs auth vs. isn't added at
   all — run `claude mcp list`:
   - **Listed but "Needs authentication"** (common — the Atlassian connector
     ships with claude.ai): just run `/mcp`, pick **Atlassian**, and complete
     the browser login. Do **not** `claude mcp add` — it would duplicate it.
   - **Not listed at all:** add it, then `/mcp` to log in:
     ```bash
     claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
     ```
   Auth is **OAuth via browser by default — no token to paste.** An API token
   is only needed for headless/non-interactive setups (passed to the MCP
   config, never committed to `settings.json`). Re-check before continuing.
2. **Load the tool schemas** you'll call via `ToolSearch`
   (`select:searchJiraIssuesUsingJql,getJiraIssue,getAccessibleAtlassianResources`).

Do not continue until setup passes.

## When to use
The user, while working inside a project repo, asks what to build next:
"what's my next task", "next Jira ticket", "what should I pick up",
"cosa faccio adesso", "dammi il prossimo task". The goal is **one** actionable
pick for the **current** project, not a raw issue dump.

## Steps

1. **Resolve the project key from the repo.** Read it from a `.jira-project`
   file at the repo root — a single line holding the Jira project key, e.g.:
   ```
   PROJ
   ```
   - If the file is missing, ask the user for the project key, then offer to
     create `.jira-project` so future runs are config-free. (Tip: add it to
     `.gitignore` if it shouldn't be shared.)
   - An optional second line may hold the site URL
     (`https://yoursite.atlassian.net`); if absent, resolve the cloudId via
     `getAccessibleAtlassianResources` (use the first/only site, or ask if
     there are several).

2. **Query the project's issues** with `searchJiraIssuesUsingJql`. Important:
   the search does **not** return Agile custom fields (`Flagged`, `Sprint`) when
   you request them by name — so **filter on them with JQL clauses**, don't try
   to read their values from the payload. Run two queries:

   a. **Candidates** — issues you could actually start now (the pick comes only
      from here):
      ```
      project = "<KEY>" AND assignee = currentUser() AND statusCategory != Done
      AND Flagged is EMPTY AND sprint in openSprints()
      ORDER BY priority DESC, updated DESC
      ```
   b. **Parked** — open issues excluded above, for the report's context
      sections (⛔ ON HOLD / 📅 NEXT SPRINT):
      ```
      project = "<KEY>" AND assignee = currentUser() AND statusCategory != Done
      AND (Flagged is not EMPTY OR sprint not in openSprints())
      ORDER BY updated DESC
      ```
   Fields for both: `summary, status, priority, issuetype, issuelinks,
   description, assignee`. (`updated DESC` is the deterministic base for step 5.)
   **Fallbacks:** if a clause errors (instance has no Agile board / no `Flagged`)
   or `openSprints()` returns nothing, drop that predicate, fold everything into
   one query, and note that the sprint/flag filter was skipped. To widen scope:
   drop `assignee` for the team backlog, or use `(assignee = currentUser() OR
   assignee IS EMPTY)` for unassigned-ready work.

3. **Classify blocked vs. blocking** from each issue's `issuelinks`:
   - **Blocked** — has an inward `is blocked by` link to an issue whose status
     category is **not** Done. These are *not* startable now.
   - **Blocking** — has an outward `blocks` link to other open issues. Starting
     these unblocks downstream work → higher impact.
   - If a linked issue's status isn't in the payload, fetch it with
     `getJiraIssue` only when it's decisive for the pick (avoid over-fetching).

4. **Bucket by status first — exclude post-development work.** `statusCategory`
   has only three values, so review/merge states (e.g. **Merge Request, In
   Review, Code Review, QA, Testing, Verified, Waiting**) fall under the same
   *indeterminate* bucket as active development. Those are **done developing** —
   never offer them as "next to develop". Split the issues:
   - **To-Do** (statusCategory new) and **actively in development** → real
     *candidates* for the pick.
   - **Post-development** (name signals review/merge/QA/verify/waiting) → drop
     from candidates; mention them separately at most ("STVR-154 is in Merge
     Request — chase the review", not "develop it"). Status *names* vary by
     workflow, so judge this from the name; when unsure, treat it as a candidate
     and say why.
   These post-development issues still count as **theme anchors** in 5.3 (they
   tell you what thread you're on), just not as the thing to build next.

   The query already split off two more kinds that are open but **must not be
   picked** — they came back in query 2b, never in 2a:
   - **Flagged / impediment** (`Flagged is not EMPTY`, value "Impediment") —
     *explicitly on hold*; someone added the flag, usually with a comment saying
     why (e.g. "tenere da parte, troppo complicata"). Show under "⛔ ON HOLD"
     and surface the reason from the issue's latest comment.
   - **Out of the active sprint** (`sprint not in openSprints()` — `future`,
     backlog, or none) — on a sprint-driven project the next task comes from the
     **current sprint**, so show these under "📅 NEXT SPRINT / BACKLOG".
   - An issue that is *both* flagged and out-of-sprint goes under ⛔ ON HOLD (the
     flag is the stronger signal).
   - **If query 2a is empty** (active sprint has no startable candidate): say so,
     then fall back to the most thread-coherent backlog item from 2b — but never
     silently promote a flagged one.

5. **Rank and pick the next task.** Order the *startable* (non-blocked) candidates by:
   1. Jira **priority** (Highest → Lowest),
   2. then **blocking** issues first (they free up others),
   3. then **lowest context-switch cost from the work just done** (see below) —
      this is the primary differentiator once priority is tied (the common case),
   4. then **most recently updated** as the deterministic base/tiebreaker.
   The **next task** is the top of this list. If every issue is blocked, say so
   explicitly and surface the blockers (so the user knows what to chase) rather
   than forcing a pick.

   **Context-switch cost (minimize).** The whole point is to flow from one story
   to the next with the **least re-orientation**: ideally the next task keeps
   editing the *same files and layers* the user just touched. Recency (step 5.4)
   is the deterministic base; on top of it, promote candidates that minimize
   switch cost:
   - **Anchor** = the story the user just finished or is on. Prefer the *active
     branch / latest commits* and any *in-progress* issue (statusCategory neither
     "new"/To-Do nor Done). The most recently developed story is the strongest
     anchor — the next pick should sit right next to it in the codebase.
   - **Estimate switch cost from code overlap, not just topic.** Read each
     candidate's **technical-details / "in this task"** section and judge how
     much it reuses what the anchor already touched:
     - **Lowest cost (promote to the pick)** — *additive* change on the **same
       files/layers** the anchor changed: extends the same model/struct, adds
       fields to the same serializer/API response, augments the same FE
       component. No new subsystem.
     - **Higher cost (push down)** — needs a **new subsystem or layer** the
       anchor didn't touch: file upload/ingestion, document parsing, new
       persistence/state, a separate detection pipeline, new integrations. Same
       *theme* but different *code* still costs a switch.
   - Same theme ≠ same code. Two tickets in one epic can have very different
     switch costs; rank by the **code** they touch, not the topic they share.
   - This step is **model-judged**, so state *why* a task won on switch cost
     (e.g. "extends the same question struct + serializer + FE list you just
     wrote in STVR-152 — purely additive, ~0 switch"). If you can't tell from the
     descriptions which candidate reuses the anchor's code, briefly inspect the
     anchor's recent diff (`git log`/`git diff` on the branch) to ground the
     judgement. If there's no anchor at all, rank by recency alone.

   **Finish WIP before starting new.** If the user has an issue *in active
   development* (not post-development, not To-Do) on the anchor's thread, that
   issue **is** the next task — continuing it beats opening a fresh ticket and
   multiplying context switches. Only when there's no active in-development work
   on the thread does the pick fall to the most thread-coherent **To-Do**
   candidate. (Post-development issues from step 4 never win this — they're done
   developing.)

   **Sanity-check the winner's comments.** Before committing to the pick, fetch
   the chosen candidate's latest comments (`getJiraIssue` with `comment`) and
   read them for a *defer/hold* signal not captured by a formal flag — "tenere
   da parte", "aspettare", "non ancora", "on hold", "blocked by X". If present,
   drop it to "⛔ ON HOLD" and move to the next candidate, stating the reason.
   Only check the top one or two — don't fetch comments for the whole list.

6. **Report as a quest log.** Render the ranking as an RPG-style questline, not
   prose. The whole thread is **one main questline** in order (every task is
   "main" — they only differ by position); the **side quests** are the
   off-thread issues (different theme / stale). Emit it inside a fenced block so
   the monospace alignment holds. Use coloured **glyphs/emoji** (not ANSI) so it
   renders everywhere — no libraries.

   Glyph legend (keep consistent):
   - **Priority dot** maps to the instance's priority scheme: 🔴 Highest/High ·
     🟠 Medium · 🟢 Low/Lowest.
   - **Node**: `⊙──▶` = the pick ("ORA"/NOW) · `◇` = upcoming steps in order ·
     `🏁` = finish line (post-development: review/merge/QA).
   - **State tick**: `☐` To-Do · `▶` in development · `✔` done-developing · `⚠`
     ambiguous status (e.g. "Pending") · `🚩` flagged/on-hold.
   - **Progress bar** = closed/total issues on the thread, e.g. `███████▇░░░░`.
   - Side-quest icons: `⚔` bug · `📦` task/story.

   **Truncate every title to a fixed width** (≈42 cols) so the right-hand
   priority/state columns line up — long titles otherwise break the map. Always
   render issue keys as clickable links when the site URL is known. Template:

   ```text
   ╔══════════════════════════════════════════════════════════╗
   ║  🗺  QUESTLINE — «<thread name>»                          ║
   ║  ███████▇░░░░░░░░  <closed>/<total>                       ║
   ╚══════════════════════════════════════════════════════════╝

   🔴 ⊙──▶ ORA · <KEY-1> · <title, truncated>          ☐
   │        ↳ <one-line objective / why now>
   │
   🟠 ◇ 2 · <KEY-2> · <title, truncated>               ☐
   🟠 ◇ 3 · <KEY-3> · <title, truncated>               ☐
   │
   🏁 review/merge: <KEY> · <KEY> · <KEY>

   ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
   ⛔ ON HOLD — flagged / deferred, not to develop
      🚩 <KEY> · <title>            « <flag or comment reason> »
   📅 NEXT SPRINT / BACKLOG — not in the active sprint
      <KEY> · <title>                                  <sprint name>
   🧭 SIDE QUESTS — off-thread
      ⚔ <KEY> · <title>                                ⚠ <status>
      📦 <KEY> · <title>                               ☐ · <note>
   ```
   Omit any of the ⛔ / 📅 / 🧭 sections that have no issues.

   If every issue is blocked, drop the questline and instead list the blockers
   to chase. Keep it tight — a decision, not the whole board.

## Notes / gotchas
- **Strictly read-only.** This skill only fetches, ranks, and reports. Use
  **only** read/search Jira tools (`searchJiraIssuesUsingJql`, `getJiraIssue`,
  `getAccessibleAtlassianResources`). **Never** call any write tool
  (`createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`,
  `addCommentToJiraIssue`, `createIssueLink`, etc.) — it must not create,
  modify, assign, transition, or comment on anything in Jira.
- **Priority names vary** per Jira instance (Highest/High/… vs P1/P2/…).
  `ORDER BY priority DESC` respects the instance's own priority scheme, so trust
  it rather than hard-coding labels.
- **Blocked ≠ Done blocker.** A `blocked by` link to an issue already Done does
  **not** block — only count blockers whose statusCategory isn't Done.
- **cloudId format:** when the Atlassian MCP expects it as
  `https://yoursite.atlassian.net`, pass that and skip
  `getAccessibleAtlassianResources`; otherwise resolve the cloudId first.
- Keep the JQL deterministic — the value of this skill over a raw "list my
  issues" is the consistent ranking, so don't improvise the ordering.
- **`Flagged` / `Sprint` are Agile-board fields** and may not exist on every
  instance. If a query errors on those clauses/fields, retry without them and
  note that the impediment/sprint filter was skipped — never let it block the
  whole run. A flag's value is "Impediment"; its reason lives in the comment the
  flag generated, not in the field.
