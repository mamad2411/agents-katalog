---
name: sprint-planning
description: >
  Use on /sprint-planning or when the user asks for planning poker or story-point
  estimation: the AI seeds Fibonacci story-point estimates with grounded rationale
  and the team votes in a Slack thread, with the AI only proposing and humans
  finalizing, scoped to this channel's project only.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [scrum, planning-poker, estimation, PM, story-points, jira]
    related_skills: [backlog-update, sprint-retro]
---

# AI-Seeded Planning Poker (PM)

The AI throws out a **grounded seed estimate** and the team finalizes it by vote. Unit = **story points (Fibonacci 1·2·3·5·8·13)**.
**The AI only proposes estimates. Voting, consensus, and finalization are human.**

## Jira Project Key (multi-project — per-vault mapping)
`jira.env` provides only `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (one shared token for all projects). **The project key comes from a per-vault mapping file**: `~/.hermes/keys/jira-projects.tsv` (`<vault-name><TAB><Jira-key>`, e.g. `example-project` → `PROJ`). **Adding a new project is one line in this file** (no per-channel key changes). Templates for both files ship in this repo's `examples/`. All Jira commands below use `${KEY}`:
```bash
set -a; . ~/.hermes/keys/jira.env; set +a   # BASE, EMAIL, TOKEN (shared)
BASE="${JIRA_BASE_URL%/}"
VAULT="<absolute path to this channel's lore vault (see the channel prompt)>"
KEY=$(awk -v p="$(basename "$VAULT")" '$1==p{print $2}' ~/.hermes/keys/jira-projects.tsv)
```

## Flow

### A. When asked only for a sprint-scope proposal
When the user asks for *sprint candidate selection, not planning poker* — e.g. "suggest what's worth doing this sprint", "recommend a 2-week sprint scope" — do not start by posting poker cards; propose a scope draft first.

1. **Query the full backlog:** query all project issues from Jira (key, title, status, priority, type). Separate done / in progress / to do, and exclude completed items from this sprint's candidates.
2. **Collect grounds:** use the PRD/wiki/graphify to see each issue's MVP importance, dependencies, impact radius, and unresolved status. Mark items with an open conflict or "to be decided later" as held or low-confidence.
3. **Recommend a 2-week scope:** if there is no team velocity, state explicitly that this is a cold start and split conservatively into `must / recommended / stretch / hold`. An MVP first sprint usually prioritizes items that later features build on — e.g. "platform / login / core CRUD".
4. **Seed points are optional:** you may attach Fibonacci seed points to aid the scope judgment, but never present them as finalized values. Label them explicitly as "seeds for planning poker".
5. **Next action:** end by offering "if you want, I'll open planning poker cards for these candidates". Move to flow B below only after the user asks for poker/estimation/voting.

### B. Planning poker (estimate, vote, finalize)
1. **Collect targets:** read this sprint's candidate issues from Jira (`POST /rest/api/3/search/jql`, `project=${KEY}`, items with no story points yet). Prepare Jira auth and the project key per "## Jira Project Key" above — load `jira.env` and look up `KEY` from `jira-projects.tsv` (never print the token).
2. **Seed estimate + rationale (per item):**
   - One point estimate + **the rationale for why that score**.
   - **Cold start (no history)** rationale material: (1) relative complexity (vs other items); (2) **graphify impact radius** (`graphify query "<item>"` for the full dependency neighborhood, `graphify explain/path` for the key connections and paths — more connections and touching god-nodes = bigger impact); (3) dependencies, open conflicts, under-specification (uncertain = round up + mark low confidence).
   - Cite wiki sources (traceability).
3. **Card posting = `poker.py`'s job (Block Kit):** once estimation is done, save the item data as **JSON** to `/tmp/loremaster_poker.json` and run the helper. The script posts the card and opens the thread — **do not print the card content again as text yourself (duplication).**
   - JSON schema: `{"items":[{"key":"PROJ-1","title":"...","seed":5,"confidence":"medium","rationale":"one line"}, ...], "hold":["Login: CONFLICT-001 open", ...]}` (key = Jira issue key, seed = integer, rationale = one line, hold = topics held due to conflicts).
   - Run: `python3 ~/.hermes/scripts/loremaster-poker.py post --estimates /tmp/loremaster_poker.json`
   - After posting, reply **briefly only**: e.g. "🃏 Planning poker cards posted. Vote once in the thread as `PROJ-…=N` (add `— rationale` if you differ from the seed)."
   - **If the helper post fails on auth/channel configuration:** do not hide the failure — post the same content yourself as a Slack mrkdwn text card and run the vote. Use no tables; list each item as `*PROJ-… · Title*`, `• Seed: *Npt*`, `• Rationale:`, and include a thread-reply format example (`PROJ-18=8 — rationale, ...`). Then, as users vote, tally manually from the votes that arrive in the conversation only.
4. **Aggregation = `poker.py`'s job:** on a "tally/close the vote" request, run `python3 ~/.hermes/scripts/loremaster-poker.py aggregate`. The script collects everyone's thread votes via `conversations.replies` and posts an aggregate card with the **distribution, median, outliers (🔥 re-discuss), and rationale** (like real poker, contested items get their rationale surfaced). **Do not duplicate the card as text.**
   - (Alternative) if emoji voting is preferred: one message per item + number emoji (`reactions` scope). The default is the thread form above.
5. **Finalize and apply:** ask for consensus-point finalization via **`request_approval` [Allow]/[Deny] buttons** (`title` = item + final points; no prose). Apply only APPROVED items to the Jira Story Points field (`PUT /rest/api/3/issue/{key}`). No automatic application without approval. **Assignment is never automatic.**
   - Find the Story Points field via the Jira field lookup (`/rest/api/3/field`) — look for `Story point estimate`. It is often `customfield_10016` on Jira Cloud, but look it up before hardcoding.
6. **When asked to create and start a sprint:** first summarize the sprint name, period, included issues, and finalized points and get **approval via `request_approval`**. Once approved, use the Agile API in order: find the board (`/rest/agile/1.0/board?projectKeyOrId=${KEY}`), create the sprint (`POST /rest/agile/1.0/sprint`), add issues (`POST /rest/agile/1.0/sprint/{id}/issue`), start it (`POST /rest/agile/1.0/sprint/{id}` with `state=active`). After creation, re-query the issues' Sprint field, points, and the sprint state to verify, then report. If the user says "2 weeks", set start = now in the team's timezone (`TZ="$TEAM_TZ"` — always pass an explicit timezone so dates match the team's wall clock) and end = +14 days, and report the team-timezone and Jira UTC values separately.
   - If backlog creation and sprint start arrive in the same request: (a) backlogs not yet in Jira are created first with per-item approval per the `backlog-proposal` rules, and (b) only the issues the user explicitly named for the sprint get a separate `request_approval` and go into the sprint. Do not confuse "add the whole backlog" with "issues for this sprint", and never create duplicates of already-created issues.
   - The Agile start payload may need more than the creation response's fields depending on the Jira instance — send `id`, `name`, `state: active`, `startDate`, `endDate`, `originBoardId`, `goal` together. Then confirm `state=active` and the dates via `GET /rest/agile/1.0/sprint/{id}`, and re-query the included issues by JQL, verifying at least key, status, priority, type.
   - See `references/jira-sprint-create-start-tested.md` for a verified run. In particular, issue addition may succeed with HTTP 204/empty body, and report "sprint started" only after the re-query confirms `state=active`.

## Calibration (cumulative, follow-up)
- At sprint end (chained with sprint-retro), match **actual time spent ↔ finalized points** to learn velocity (points→time) and category/individual bias → refine the next seeds. The unit is points; the calibration fuel is time.

## Slack output format (important — this is read in Slack)
- **Seed/aggregate cards are posted by `poker.py` as Block Kit.** Your direct replies are short guidance only (no card duplication).
- All other replies: **Slack mrkdwn only.** Markdown **tables (`| ... |`), `**bold**`, and `#headers` break in Slack — forbidden.**
- Bold = `*text*`, italic = `_text_`, code = `` `code` ``, lists = `•` or `-`.
- Items as **short sections instead of tables**. Example:
  ```
  *PROJ-PP-1 · Real-time co-editing*  — seed *8pt* (low confidence)
  • Rationale: co-editing approach and cursor UI unspecified; collaborator-count conflict open
  ```
  Separate items with a blank line. If long, keep the essentials; rationale 1-2 lines.

## Rules (invariant)
- The AI estimate is **a starting point, not an anchor** — the team vote wins. The AI never forces consensus.
- Never invent estimation rationale without grounds in the wiki/Jira. If uncertain, mark "low confidence" and round up.
- Items with an open conflict may be held as "estimate after conflict resolution".
- This channel = this project only. This project's Jira key (`${KEY}`) only. Other projects forbidden.

## Output
- Post per-item [seed points, rationale, voting instructions] to Slack. Finalization and Jira application only after human approval.
