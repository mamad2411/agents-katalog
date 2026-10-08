---
name: refresh
description: "Refresh threads_daily_tracker.json. Prefer the Threads API when available; fall back to authenticated browser profile scraping when API access is not available. Trigger words: 'refresh', 'update tracker', 'scrape profile', '更新貼文', '抓最新數據'."
version: "2.0.0"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AK-Threads-Booster Profile Refresh Module

You are the tracker-refresh worker for the AK-Threads-Booster system. Pull the user's latest posts, metrics, and comments, then merge them into `threads_daily_tracker.json` without losing existing data.

Two refresh sources are supported and must be tried in this order:

1. **Threads API** — preferred when a token is available. Faster, more reliable, better for scheduled refresh.
2. **Authenticated browser automation** — fallback for users who cannot or do not want to use the API. Scrapes the user's own logged-in Threads profile.

Browser scraping is slower and more fragile than the API. Use it only when the API path is unavailable or the user explicitly asks for browser-based refresh.

---

## Step 0: Pick the Refresh Source

Follow `references/api-path.md` to decide whether the API path applies. If it does, run the API commands there and **stop** — do not run the Chrome flow. If the user explicitly asks for Chrome even with a token, honor that and note the override in the final summary.

---

## Execution Modes

`/refresh` runs in **interactive mode** (direct user invocation — may ask questions, pause) or **headless mode** (scheduler, other skill, or `--headless` in `$ARGUMENTS` — must not ask or pause).

Full contract, recognized arguments, log schema, and preconditions (browser automation available, logged in, handle match, handle known) are in `references/headless-contract.md`. Every precondition failure in headless mode maps to a specific `reason` value for the log entry.

---

## Principles and Knowledge

Load `knowledge/_shared/principles.md` before scraping. Follow discovery order in `knowledge/_shared/discovery.md`. For `/refresh`, also load:

- `data-confidence.md`
- `chrome-selectors.md`

Never hard-code selectors in this skill. `chrome-selectors.md` is the source of truth.

---

## Chrome Execution Flow

Follow `references/chrome-flow.md` for Steps 1–7:

- **Step 1** — load or create tracker (ask for handle in interactive mode if needed)
- **Step 2** — navigate to `https://www.threads.com/@<handle>` and confirm header handle
- **Step 2.5** — mandatory selector health check from `knowledge/chrome-selectors.md` (abort with `login_wall` or `selector_health_failed` on failure)
- **Step 3** — scroll until no new posts, `--max-posts` reached, or `--max-minutes` reached
- **Step 4** — extract post data (id, text, created_at, permalink, media_type, metrics); preserve last-known tracker value when a metric token fails to parse
- **Step 5** — extract replies only for posts that are new or whose reply count changed
- **Step 5.5** — sweep expired `pending-` placeholders (into `discarded_drafts[]`, merge snapshot into real post if matched)
- **Step 6** — merge into tracker per the 6-rule merge matrix; keep existing `prediction_snapshot` untouched
- **Step 7** — persist under `templates/FAILSAFE.md`: backup → prune to 5 → write temp → atomic rename → regenerate companions → rebuild compiled memory → write headless log if applicable. Companion and compiled-memory failures are non-fatal.

### Step 8: Report

Use the exact report shape in `references/output-and-failures.md`. The failure-mode table is there too — consult it before giving up on a partial refresh.

---

## Boundary Reminders

- It is valid for this skill to write the tracker, backup files, refresh log, and companion files. Those writes are part of the contract.
- It is valid for this skill to rebuild `compiled/` after tracker changes. Compiled memory is a cache; if rebuild fails, keep the refreshed tracker and report that low-token runtime is stale.
- Do not modify `prediction_snapshot`, `review_state`, or enriched analysis fields outside the merge rules in `references/chrome-flow.md`.
- If a post is no longer visible on the profile, report it but do not delete historical data.
- Browser automation actions must stay inside `threads.com` during this flow.
