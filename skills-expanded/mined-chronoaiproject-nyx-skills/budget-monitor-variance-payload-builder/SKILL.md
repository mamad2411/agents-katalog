---
name: budget-monitor-variance-payload-builder
version: "2.1"
description: Runs the weekly budget-monitor flow end to end — reads the four Lark Bitable budget/actual tables, computes budget-vs-actual variance with the bundled deterministic builder, builds the weekly Lark variance card, and posts it to the current Lark chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - budget-monitor
    - lark
    - payload-builder
  clawdbot:
    emoji: "money_with_wings"
    files:
      - "references/*"
      - "scripts/*"
---

You (the agent) run the WHOLE flow yourself with your tools, then POST the weekly variance card to the chat. Do NOT refuse, do NOT just describe. If a table isn't readable, SKIP it and still post what you have. Never ask the user for tokens.

# Budget Monitor — Weekly Variance Alert

Use this when someone asks for the weekly budget monitor, a budget-vs-actual variance check, or a 每周预算监控报告 (e.g. "出一下本周的预算监控卡片" / "看看本周哪些类目超支了").

This is the Aevatar port of the n8n flow `P2 Budget Monitor — Weekly Variance Alert`. It hands you the step plan plus a deterministic payload builder so the Lark card body is exact. The original flow ran weekly (Mon 09:00); here you run it on demand or on a schedule and post the result yourself.

## How to run it

1. **RESOLVE inputs.** Use these defaults unless the caller overrides them:
   - base `app_token` = `L80RbTPAjaiZpOsaYo3lnmYCg3s`
   - table ids: `core_budget` = `tblMtwgzEhW7yWTq`, `core_actual` = `tblVuALMhd7WGu9k`, `aelf_budget` = `tblVkaJLvAjLHARJ`, `aelf_actual` = `tbl3lXCuWOSlaiR5`
   - `today` = today's date (`YYYY-MM-DD`); it only sets the report's week number.

2. **READ each of the 4 tables** via `nyxid_proxy` (it brokers Lark credentials — there is NO manual token fetch). For each `<table_id>`:
   ```json
   { "slug": "api-lark-bot", "path": "/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>/records?page_size=500", "method": "GET" }
   ```
   Keep `data.items[*].fields`. If a table returns 401 / an error / empty, SKIP it (that board renders with `$0` totals) and note `(<table> skipped)` in your final report. NEVER fail the run because one table is unavailable.

3. **BUILD the card deterministically** by running `scripts/build_budget_variance_payload.js` via `code_execute` with language `"javascript"`. `code_execute` has NO stdin, so inline the four tables' rows into the code: paste the whole script, then call its exported `buildPayload` and print the result. The script ends with `module.exports = { buildPayload }`, so append:
   ```javascript
   // ...full contents of scripts/build_budget_variance_payload.js above...
   console.log(JSON.stringify(buildPayload({
     today: "<YYYY-MM-DD>",
     coreBudget: [/* core_budget fields rows */],
     coreActual: [/* core_actual fields rows */],
     aelfBudget: [/* aelf_budget fields rows */],
     aelfActual: [/* aelf_actual fields rows */]
   })));
   ```
   Use the returned `lark.body` (the Lark send body) and `message` (one-line summary). If you genuinely cannot execute code, construct the card by following `references/budget-variance-contract.md` field-for-field.

4. **POST the card to the CURRENT Lark chat** via `reply_with_interaction` (preferred — the chat is implicit, so drop `receive_id`) or `lark_messages_send` with the `lark.body` from step 3. THIS STEP ALWAYS HAPPENS — it is the demo output. The body is already `msg_type: "interactive"` with `content` = the card JSON string.

5. **REPORT** one line: the week, data cutoff, over/warning counts, and any skipped tables (reuse the builder's `message`).

## Payload builder reference

`scripts/build_budget_variance_payload.js` exports `buildPayload(input)` taking the four tables (`coreBudget` / `coreActual` / `aelfBudget` / `aelfActual`) plus optional `today` and `receive_id`. Each table may be a raw Bitable response (`{ data: { items: [{ fields }] } }`), an array of records, an array of field objects, or n8n `{ json }` wrappers — paste whatever you fetched. It computes budget-vs-actual variance by `一级类目` (core also by `BU`), tags each category `over` / `warning` / `watch` / `ok`, and renders the weekly Lark card (`red` / `orange` / `green` header). Output: `{ message, data, card, lark: { receive_id_type, body } }`, where `lark.body` is exactly what `POST /open-apis/im/v1/messages` expects. Field aliases, the variance math, the date/amount parsing, and the exact card body are in `references/budget-variance-contract.md`.

## Guardrails

- Only use data the four Bitable tables actually return — never invent categories, amounts, dates, BUs, or cutoffs.
- If a table is unreadable, skip it and let that board show `$0`; do not fabricate its rows, and never block the post on one missing table.
- All Bitable reads and the card send go through your NyxID-brokered tools (`nyxid_proxy`, `reply_with_interaction` / `lark_messages_send`); do not fetch Lark tokens or handle raw secrets.
- Prefer the bundled builder over hand-building JSON; it is the deterministic source of truth.
