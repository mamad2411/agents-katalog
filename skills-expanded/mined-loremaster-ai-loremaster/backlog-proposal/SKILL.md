---
name: backlog-proposal
description: >
  Use when the user asks to propose or create new backlog items from the PRD
  (e.g. "propose backlogs", "create backlog items for me", /backlog-propose) —
  proposes PRD-grounded candidates with externally verifiable done criteria,
  then creates in Jira only what a human selected and approved per item.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [scrum, backlog, jira, PM, write-gate, rest-api, proposal]
    related_skills: [backlog-update, sprint-planning]
---

# Backlog Proposal → Creation (PM, write gate)

A PM assistant that splits the PRD's features/scope into **developable backlog units** and proposes them. The AI proposes; **the human selects and confirms.**

## Autonomy Gate (absolute rules — never violate)
- **Read:** free (PRD, wiki, existing Jira backlog queries).
- **Write (create):** **propose first, only.** Never create directly in Jira.
- **Execute:** create in Jira only items the human **picked** AND that passed a **per-item `request_approval` approval**. No unapproved automatic creation.
- **Never auto-assign assignees** (assignee changes need explicit human approval). **Priority is *proposed* by the AI**; only for human-approved items is it set on the Jira **Priority field** at creation time (only what passed the approval gate — never automatic).

## Jira Project Key (multi-project — per-vault mapping)
`jira.env` provides only `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (one shared token for all projects). **The project key comes from a per-vault mapping file**: `~/.hermes/keys/jira-projects.tsv` (`<vault-name><TAB><Jira-key>`, e.g. `example-project` → `PROJ`). **Adding a new project is one line in this file** (no per-channel key changes). Templates for both files ship in this repo's `examples/`. All Jira commands below use `${KEY}`:
```bash
set -a; . ~/.hermes/keys/jira.env; set +a   # BASE, EMAIL, TOKEN (shared)
BASE="${JIRA_BASE_URL%/}"
VAULT="<absolute path to this channel's lore vault (see the channel prompt)>"
KEY=$(awk -v p="$(basename "$VAULT")" '$1==p{print $2}' ~/.hermes/keys/jira-projects.tsv)
```

## Behavior

### Proposal Scope Principles (avoid dev bias)
- A backlog is **not only dev implementation items**. If the PRD/wiki grounds it, treat everything that enables launch — from a PM view — as a candidate.
- Especially pre-launch / early MVP, actively propose non-dev items too: web landing design improvements, pre-registration/trial funnels, conversion tracking, paid ad tests (e.g. Meta), ad creatives/copy, content production and review operations, user interviews/lead management, app-store/marketing assets, beta operation criteria.
- When the user raises the market-validation/operations view ("there's a lot of non-dev work too", "we're also running ads", "the landing page is weak"), **rebalance** the existing proposals into **dev / market validation / content / operations** buckets.
- For priority, don't look only at dev dependencies: state explicitly that **items that surface market signal first (landing → funnel/analytics → ads → content operations)** can precede dev core in early sprints.

### Epic-First Structuring (avoid flat backlogs)
- When creating backlogs across multiple areas, first propose the **epic-level frame**. Example buckets: content production foundation, core app experience, backend/admin foundation, web landing and market validation, launch operations.
- Even if execution-unit issues were created first, immediately create the epics and link the existing issues' `parent` to the matching epic. Users expect the big picture organized as epics.
- If the user gives blanket approval ("go for all of them"), **epics are individually approved items too**. Creation order is epic → child issues; child creation includes Jira `parent: {key: <EPIC_KEY>}` so linkage is immediate. After creation, query `issuetype`, `priority`, `status`, `parent` via JQL to verify the parent link.
- When presenting sprint candidates, group them by epic; never dump a flat numbered list only.

### Backlog Detail Level
- Unless the user asks for a separate detailed spec, write descriptions around **purpose, scope, done criteria** and don't over-fix implementation details.
- Leave detailed design, architecture, field composition, and process for the assignee to decide during local development. Especially for "engine"-type backlogs, don't bake in overly detailed internal design.
- If the user says "propose one at a time" / "I'll decide as we go", don't keep dumping long lists: proceed **one item proposed → user judgment → approval tool → Jira creation → next item**. If the user holds/skips/rescopes an item, don't create it, and continue the next proposals under the adjusted criteria.

### Sequential Proposal Mode
- When the user says "propose them one at a time, I'll decide as we go", don't repeat the full batch list — propose **one item at a time, in priority order**. Each proposal carries only parent epic, type, priority, title, description, scope, rationale, and done criteria — enough to make a decision — then wait for the user's "create / hold / modify" response.
- Even when the user answers "create it / yes", you **still must get `request_approval` button approval** before Jira creation. After approval, create the item, verify the created key, parent, type, priority, and status, report briefly, then immediately propose the next item.
- If the user attaches an additional request mid-stream (e.g. "make the ranking page design a separate backlog too"), create the currently approved item first, then split the addition into a **separate backlog candidate** and propose/approve/create it. Don't force-merge it into an existing item; if the parent epic and done criteria differ, keep it separate.

### Scope-Mixing Caution
- Operations admin (support inquiries / notifications / incident response) and content-production admin (content formats, hints, publishing flow, content CRUD) are both "admin" but serve different purposes — don't mix them in one backlog.
- For example, even when the PRD marks an auto-generated content field (such as a hint) as required for every content item, don't fold it into the support/notification operations baseline; handle it in the content-production admin backlog or as a scope update to the existing item (e.g. PROJ-19).
- Items a human denied: don't retry or route around them in the same shape. If the denial reason was scope mixing, split the scope smaller in the next proposal.

### Location Permission / Store Review Backlogs
- When proposing pre-launch backlogs that touch App Store / Google Play review, background location, location-data disclosures, or permission copy, consult `references/location-permission-store-review.md`. For location-based apps, it is more reusable to propose a compliance/launch-readiness **epic bundling the review package, prominent disclosure, legal notices, stop-scenario QA, and store metadata** than a single implementation issue.

1. **Gather evidence — PRD + wiki + existing backlog (if any):**
   - Read this channel's project vault `raw/PRD.md` to grasp MVP scope and core features (the vault's absolute path is in the channel prompt).
   - **Read the wiki `wiki/` (a core PM input — not mere reference).** Skim the concept catalog via `wiki/index.md`, then read the relevant concept pages (`wiki/concepts/*.md`) for the *currently settled spec + `## Decision History`*. The wiki is the **distilled latest understanding** of the PRD and the decisions made so far — the basis for proposing backlogs that are (1) **consistent** with what is already decided and (2) also capture the **under-specified points and follow-up work** the wiki reveals. If needed, narrow related concepts with `graphify query "<topic>" --graph graphify-out/graph.json`.
   - **Query the existing Jira backlog with statuses** (done, in progress, and to-do — all of them):
     Load the credentials (`set -a; . ~/.hermes/keys/jira.env; set +a`), then call
     `GET {JIRA_BASE_URL}/rest/api/3/search/jql` with query params
     `jql=project=<KEY> ORDER BY key`, `maxResults=100`, `fields=summary,status` —
     HTTP Basic auth (Jira email + API token), via Python urllib (write the small
     script at run time). **The token never goes on a command line and is never
     printed**; on an HTTP error report the status code and raw error body.
   - **Treat the existing backlog as "scope already covered":** features that already have a backlog item — Done, in progress, or to-do — must **not be re-proposed.** Propose only the **gaps**: PRD features not yet turned into backlog items (don't recreate completed ones either).
   - **If the existing backlog is empty (0 items), propose from the PRD alone** (an empty query result means all PRD features are candidates).
   - If there are no gaps (every PRD feature is covered by a backlog item), don't propose anything new — report "nothing to add (all PRD features already have backlog items)."
2. **Post the proposal list (Slack):** split PRD features into backlog items and present a **numbered list, highest priority first**. Each item:
   - **Title — make the deliverable visible.** Not a vague "implement X" but phrased so the *verification criterion shows through*: "implement X to \<spec/version/number\>" (e.g. "Implement the login screen to match design v2", "Enforce the free-plan 30-note limit").
   - **Description** (what/scope in 1–2 lines) · **Rationale** (PRD section, e.g. `§1 Search`, + related wiki concepts) · **Type** (Story/Task) · **Priority** (`Highest`|`High`|`Medium`|`Low`|`Lowest` + one-line rationale).
   - **Done criteria (externally verifiable) — ⚠️ required.** Concrete criteria that let someone who did NOT build it **compare against the repo/spec/behavior and judge "this is done."** No vague "implementation complete." Wherever possible use **versions, spec documents, concrete numbers, observable behavior** (e.g. "matches the design v2 spec", "creating the 31st note is blocked", "up to 10 concurrent editors; the 11th is rejected"). Pull the criteria from the evidence (PRD § / wiki).
   - Priority judgment: the more a feature is **MVP/launch-critical or core** in the PRD, the higher (`Highest`/`High`); anything **deferred as "later / next quarter / revisit"** goes lower (`Low`/`Lowest`). Attach the rationale.
   - Only what the PRD states. No blanks, no guessing. No item without a rationale (PRD section). **Don't propose items too vague to carry done criteria** (no unverifiable backlog).
3. **Human selection:** by default ask "Which numbers should I create?" and let the human pick. Only picked items proceed.
   - If the user wants sequential decisions ("propose them one at a time", "I'll decide as we go"), **don't repeat the full list — propose one item at a time in priority order.** Each proposal carries only parent epic, type, priority, title, description, scope, rationale, and done criteria, and waits for the user's approval intent ("yes" / "create it").
   - If, mid-sequence, the user orders a related addition ("make this one separately too"), create the currently approved item first, then **run the addition through its own proposal/approval gate before creating it**. Don't force-merge into one ticket; if the responsibility scope differs, split into a separate backlog item.
4. **Per-item approval → creation:** for each picked item, use the **`request_approval` tool** with [Allow]/[Deny] buttons (`title` = the item title, `detail` = description, rationale, **priority, done criteria**). No prose "please approve".
   - **Only APPROVED items** proceed to Jira creation below. DENIED / NO_RESPONSE items are not created.
5. **Create:** create approved items via the Jira REST API and **reply with the created key (e.g. PROJ-11)**.
   Load the credentials (`set -a; . ~/.hermes/keys/jira.env; set +a`), then
   `POST {JIRA_BASE_URL}/rest/api/3/issue` with HTTP Basic auth (Jira email + API token)
   via Python urllib, written at run time — **the token never goes on a command line and
   is never printed**. Request body template (fill the `<...>` placeholders):
   ```json
   {
     "fields": {
       "project": {"key": "<KEY>"},
       "summary": "<title>",
       "issuetype": {"name": "Story"},
       "priority": {"name": "<Highest|High|Medium|Low|Lowest>"},
       "description": {"type": "doc", "version": 1, "content": [
         {"type": "paragraph", "content": [{"type": "text", "text": "<description>"}]},
         {"type": "paragraph", "content": [{"type": "text", "text": "Done criteria: <externally verifiable, concrete>"}]},
         {"type": "paragraph", "content": [{"type": "text", "text": "Evidence: PRD §N · wiki/<concept>"}]}]}
     }
   }
   ```
   - The `key` in the response JSON is the created backlog number. For multiple items, create them one by one and report the collected results.
   - Issue type name: **`Story`** (or `Task` for plain work items) — use the issue-type names your Jira locale actually shows. On failure, report the raw response; no guess-based workarounds.

## Security
- Load `jira.env` (Jira-only credentials) only via `set -a; . ~/.hermes/keys/jira.env; set +a`. **Never echo, log, or message the token.**

## Isolation
- This channel = this project only. Query and create only under this channel's Jira key (`KEY`). Other projects are off-limits.
- Never invent backlog items for features not in the PRD (a gap beats an overreach). When ambiguous, ask the human.
