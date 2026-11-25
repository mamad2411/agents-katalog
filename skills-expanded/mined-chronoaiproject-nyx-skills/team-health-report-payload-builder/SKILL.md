---
name: team-health-report-payload-builder
version: "2.2"
description: Runs the team-health report flow end to end and posts a digest to the chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - team-health
    - lark
    - github
    - payload-builder
  clawdbot:
    emoji: "bar_chart"
    files:
      - "references/*"
      - "scripts/*"
---

You (the agent) run the WHOLE flow yourself with your tools, then POST the result to the current Lark chat. Do NOT refuse, do NOT just describe. If a data source or sink is unavailable, SKIP it and still post what you have.

# Lark Team Health Report

Use this when someone asks for a team-health report, team activity digest, individual teammate health check, or CHO/COO-style summary based on GitHub and public activity signals.

## How to run it

1. **COLLECT via tools, using ONLY bound connectors.**
   - GitHub → `nyxid_proxy` slug `api-github` (bound ✓).
   - Public web / RSS / Hacker News (and any other public endpoint) → `web_fetch` (no credential, ✓).
   - ⚠ `api-reddit` and `api-twitter` are NOT bound for this bot — do NOT depend on them. Use `web_fetch` on public endpoints instead where possible; otherwise SKIP that source and note "(<source> skipped — connector not bound)" in the message. NEVER fail the run because one source is unavailable.

2. **ANALYZE with your own model.** Summarize, score, and rank the collected signals. Keep the result grounded in observed data: recent merged PRs, open PRs, issues, reviews, comments, stale work, milestone/deadline risk, and any public context that was actually available.

3. **BUILD the message body by running `scripts/build_team_health_payload.js` via `code_execute` (language `"javascript"`) with the collected data.** Build a concise digest string first. `code_execute` has NO stdin, so inline that digest into the code: paste the whole script, then call its exported `buildPayload`. The script exports `module.exports = { buildPayload }`, so end the code with:
   ```javascript
   // ...full contents of scripts/build_team_health_payload.js above...
   console.log(JSON.stringify(buildPayload({
     mode: "build_messages",
     chat_id: "<current chat id when available>",
     report: "<your digest string>"
   })));
   ```
   Use `lark.reportBody` / `lark.body` from the script output. If you cannot run code, fall back to `references/team-health-contract.md` and construct the same Lark text body shape.

4. **POST it to the CURRENT chat via `lark_messages_send`** (or `lark_messages_reply` / `reply_with_interaction`). THIS STEP ALWAYS HAPPENS — it is the demo output. If some sources were skipped, include a short skipped-source note inside the posted digest.

5. **OPTIONAL:** writing a Lark Bitable record is best-effort ONLY — do it only if a target base `app_token` + table is actually provided; if not, SKIP and still post the chat message. Never block on a missing Bitable.

## Payload builder reference

The bundled script accepts:

- `mode: "parse_command"` with a raw Lark event body to parse `/team-health [targetUser]`.
- `mode: "build_messages"` with `chat_id` or `parsed.chat_id`, plus optional `report`, to produce connector-ready progress and final report message bodies.

Exact aliases, required keys, and fallback payload shapes are in `references/team-health-contract.md`. Prefer the script output when possible; it is the deterministic source for the Lark send body.

## Guardrails

- Never invent GitHub activity, teammates, scores, URLs, Lark ids, Bitable ids, or connector credentials.
- Missing optional sources are not fatal. Say what was skipped and post the digest anyway.
- Keep the posted message useful and short enough to read in chat: headline, overall risk counts, notable people/items, skipped sources, and next actions.
