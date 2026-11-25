---
name: deadline-monitor-digest-payload-builder
version: "2.3"
description: Runs the deadline-monitor flow end to end — reads GitHub repo or org milestones/issues, ranks deadline risk, builds the exact Lark digest with the bundled deterministic builder, and posts it to the current Lark chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - deadline-monitor
    - lark
    - github
    - payload-builder
  clawdbot:
    emoji: "alarm_clock"
    files:
      - "references/*"
      - "scripts/*"
---

# Deadline Monitor

Use this when someone asks for a deadline / milestone risk digest or check-in for a GitHub repo
or GitHub organization (e.g. "看看 aevatarAI/aevatar 临近截止的 milestone，生成今日风险摘要",
"看看 ChronoAIProject 今天有哪些截止风险").

**You (the agent) run the WHOLE flow yourself, calling your own tools — then actually post the
result.** This skill hands you the step plan plus a deterministic payload builder so the Lark
message body is exact. Do NOT just describe what you would do, and do NOT refuse because "the
skill only formats" — that is wrong; drive the flow. Never ask the user for tokens; your NyxID
tools broker all credentials.

## How to run it

1. **Resolve inputs.** Parse the target from the user's message and today's date. The target is
   either:
   - a concrete repo: `owner/name`, for example `aevatarAI/aevatar`;
   - a GitHub org/user only: `owner`, for example `ChronoAIProject`.

   Do not fabricate a repo from an org/user name. If the target has no slash, first treat it as an
   org/user candidate and verify it through GitHub discovery. Never rewrite a single-segment target
   into `owner/name`, and never call `/repos/{owner}/{name}/...` until discovery returns an actual
   repository `full_name`.

   Choose a mode: `daily_risk_digest` (open milestones with due dates, ranked by days left),
   `orphan_milestone_digest` (open issues with no milestone), `friday_progress_report`
   (milestone progress), or `checkin_payloads` (per-assignee check-ins). Default to
   `daily_risk_digest`.

2. **Collect from GitHub** using your NyxID-brokered GitHub access (the `api-github` service via
   `nyxid_proxy`).

   For a concrete repo `owner/name`, call:
   - milestones: `GET /repos/{owner}/{name}/milestones?state=open&sort=due_on&direction=asc`
   - issues: `GET /repos/{owner}/{name}/issues?state=open&per_page=100`

   For an org/user target `owner`, first discover repos:
   - org repos: `GET /orgs/{owner}/repos?per_page=100&type=all`
   - if that returns 404, user repos: `GET /users/{owner}/repos?per_page=100&type=owner`

   Then call the repo endpoints above for each discovered non-archived repo you need. Keep the
   number of repo fan-out calls reasonable: for `daily_risk_digest` and `friday_progress_report`,
   milestone calls are enough; for `orphan_milestone_digest` and `checkin_payloads`, issue calls are
   needed. Preserve the full repo name on every row (`repo` or `repository`, e.g.
   `ChronoAIProject/Ornn`) before passing data to the builder. Keep only the fields you need
   (title, due_on, state, closed_at, open/closed issue counts, html_url, assignee, milestone).

   If every GitHub call for the selected target returns 404, stop and report that the target was not
   found; do not build or send an empty "no risk" digest from failed calls.

3. **Build the exact Lark payload deterministically.** Run `scripts/build_deadline_monitor_payload.js`
   via `code_execute` (language "javascript"). `code_execute` has NO stdin, so inline the collected
   data into the code — the script exports a builder, so append
   `console.log(JSON.stringify(buildPayload({ mode: "<mode>", today: "<YYYY-MM-DD>", ...rows })))`.
   Use the `lark.body` (and `message`) from its output. If you genuinely cannot execute code,
   construct the body by following `references/deadline-monitor-contract.md` field-for-field.

4. **Send it to the current Lark chat.** Post the digest into this conversation with
   `lark_messages_send` (or `lark_messages_reply` to reply, or `reply_with_interaction` for a
   card) using the `lark.body` from step 3.

5. **Report** a one-line summary of what you posted (mode, repo, item count).

If GitHub succeeds and returns no matching items for the chosen mode, say so plainly and stop — do
not invent records. If GitHub failed, report the failure instead of posting a clean empty digest.

## Payload builder reference (step 3)

Modes the bundled script accepts:

- `daily_risk_digest` — `today` + GitHub milestones (or precomputed risk rows).
- `orphan_milestone_digest` — `today` + open GitHub issues.
- `friday_progress_report` — `today` + milestone records.
- `checkin_payloads` — selected check-in rows (after assignee mapping / filtering / dedupe).

Fields may be at the root or under `body`. Exact aliases, required keys, and examples are in
`references/deadline-monitor-contract.md`.

Script output is one of: `skip: true`; `needs_more_information: true` + `missing` keys; a digest
object with `message`, `larkBody`, and `lark.body`; or a check-in object with per-item
`larkMsgBody`, `lark.body`, `githubCommentBody`, and `github.body`. The Lark bodies already match
the field names Lark's send API expects.

## Guardrails

- Only use data GitHub actually returned — never invent milestones, issues, user ids, or status.
- Prefer running the bundled script over hand-building JSON; it is the deterministic source of truth.
- All sending and token exchange go through your NyxID-brokered tools; do not handle raw secrets.
