---
name: chrono-ai-weekly-report
version: "1.0"
description: Pulls a GitHub account's issues and pull requests for the week, analyzes what shipped, what is in progress, and what is blocked with real workload metrics, then renders a Lark interactive card with hyperlinked rows and a metrics table, or a markdown report. The agent runs the whole flow itself using its own NyxID-brokered tools.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - payload-builder
    - github
    - weekly-report
    - lark
  clawdbot:
    emoji: "bar_chart"
    files:
      - "references/*"
      - "scripts/*"
---

# Chrono AI Weekly Report

Use this when someone asks for a weekly GitHub report — "本周我做了什么 / 周报 / weekly
report / what shipped this week" — for a GitHub account.

**You (the agent) run the WHOLE flow yourself, calling your own tools — then actually
deliver.** Do NOT just describe the steps; do NOT refuse because "the skill only formats".
Never ask the user for a token; your NyxID tools broker every credential. This skill owns
only the deterministic card/markdown formatting (step 6); you do all the GitHub reading,
analysis, and Lark sending.

## How to run it

1. **Resolve target + window.** If the user gives a `username`, use it; otherwise resolve
   the caller's own login with `nyxid_proxy` service `api-github-pat`: `GET /user` and read
   `login`. Default the window to the last 7 days; honor an explicit `since`/week the user
   names. Compute `start` and `end` as `YYYY-MM-DD` strings — you compute the dates, the
   bundled script never reads a clock.

2. **Fetch issues + PRs** with `nyxid_proxy` service `api-github-pat` (PAT-backed so private
   repos like `aevatarAI/aevatar` are visible). Run the Search API and merge `items`:
   - `GET /search/issues?q=author:{login}+created:{start}..{end}&per_page=100&sort=updated`
   - `GET /search/issues?q=author:{login}+updated:{start}..{end}&per_page=100&sort=updated`
     (catches items created earlier but worked on this week)
   Paginate while `total_count` exceeds what you have. Dedupe by `html_url`. Each item is a
   PR when it has a `pull_request` field, otherwise an issue. Parse `repository_url`
   (`https://api.github.com/repos/{owner}/{repo}`) and `number` from every item.

3. **Enrich each PR** with `nyxid_proxy` service `api-github-pat`:
   - `GET /repos/{owner}/{repo}/pulls/{number}` → `state`, `draft`, `merged`, `merged_at`,
     `mergeable_state`, `additions`, `deletions`, `changed_files`, `head.sha`, `base.ref`.
   - Optional CI rollup: `GET /repos/{owner}/{repo}/commits/{head_sha}/check-runs` → count
     `conclusion` failure/in_progress.
   - Optional review state: `GET /repos/{owner}/{repo}/pulls/{number}/reviews`.
   Map each PR to a status: `merged` (merged=true), `draft` (draft=true), `blocked`
   (`mergeable_state` in dirty/conflicting OR a required check failed), `review` (review
   requested / changes requested), else `open`. If `mergeable_state` is null, GitHub is still
   computing it — say "unknown", do not claim conflict-free.

4. **Categorize.** Bucket every item by its title prefix: `feat`/`feature` → Feature,
   `refactor` → Refactor, `fix`/`test`/`chore`/`docs` → Fix / Test / Chore. Items without a
   conventional prefix: judge from the title. Inside Feature, you may sub-group by theme
   (e.g. 技能系统 / OpenAI 兼容 / Lark / 基础设施) using the section `title`.

5. **Analyze with your own model** and assemble the `report` object:
   - `account`, `window:{start,end,label}`
   - `headline`: one sentence — the week's throughline, not a list.
   - `metrics`: sum across the fetched PRs — `additions`, `deletions`, `changed_files`; plus
     `rework_commits` (count items whose title matches `review` / `r\d` / `gate`).
   - `sections`: `[{ title, items:[{ number, title, url, status, scope }] }]` — `url` is the
     PR/issue `html_url` (this is the hyperlink), `scope` is a short tag like the target
     branch or `#1698`. List EVERY item; do not summarize away the long tail.
   - `blockers`: `[{ title, url, why, cost }]` — only genuinely blocked items (conflicting,
     CI red, stale draft), each with why it is blocked and what it is holding up.

6. **Build the deliverable deterministically.** Run
   `scripts/build_weekly_report_payload.js` with `code_execute` (Node), passing the `report`
   object on stdin. It returns `markdown` and `lark.body` (an interactive card with a metrics
   table, per-section hyperlinked rows, and a red header when blockers exist). Prefer this
   script over hand-building the card; it is the deterministic source of truth. If you truly
   cannot execute code, follow `references/weekly-report-contract.md` field-for-field.

7. **Deliver.**
   - **On Lark** (the user is talking to you through a Lark bot): take the `chat_id` from your
     runtime conversation context — never hardcode or invent it — set it as `receive_id`, then
     `nyxid_proxy` service `api-lark-bot`:
     `POST /open-apis/im/v1/messages?receive_id_type=chat_id` with the returned `lark.body`
     (`msg_type` is `interactive`, `content` is the stringified card).
   - **Otherwise**, return the `markdown`.

8. **Report** one line: how many issues and PRs were fetched, how many merged / open / blocked,
   and where the report was delivered.

If GitHub returns no items in the window, say so plainly and stop.

## Payload builder reference (step 6)

Bundled script: `scripts/build_weekly_report_payload.js`. Mode: single (`build_report`).
Input may be at the root, under `report`, or under `body`. It accepts `sections`, or the
aliases `features` / `refactors` / `fixes` as arrays. Per-item status accepts
`merged|open|review|draft|blocked|closed` (or infers from `merged`/`draft` booleans). It emits
either `{ needs_more_information: true, missing: ["report"] }` or a
`message_type: "weekly_report"` object with `markdown` and `lark.{path,query,body,card}`.

Exact aliases, the card element shapes, and a full worked example are in
`references/weekly-report-contract.md`.

## Guardrails

- Use real returned GitHub data only; never invent issue numbers, URLs, statuses, counts, or
  diff metrics. Every hyperlink must be a real `html_url`.
- Never fetch or store a token; `nyxid_proxy` brokers GitHub and Lark credentials.
- The Lark `receive_id` (chat_id) comes from your runtime context, never a literal in this skill.
- Conflict detail is API-level (`mergeable_state`, check-runs, reviews). File-level conflict
  diffs require a clone and are out of scope — report `mergeable_state` instead.
- Prefer running the bundled script over hand-building JSON.
