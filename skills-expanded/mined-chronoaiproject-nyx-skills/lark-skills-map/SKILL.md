---
name: lark-skills-map
description: Index, router, and dependency map for the aevatar Lark/Feishu skill family on ornn — load this FIRST when someone wants the bot to do anything in Lark (send a message, recall a chat, write a doc / sheet / Base record, manage a calendar event, run an approval). It names the six core operation primitives (im / docx / sheets / bitable / calendar / approval), states the one shared premise (every call goes through nyxid_proxy slug api-lark-bot, scope-probe-first), routes intent to exactly one primitive, lists which business workflows consume them, and flags the current cleanup items. It does not call Lark itself — it routes to the right ops skill.
version: "1.0"
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - map
    - router
    - index
---

# Lark skills map

One premise for the whole family: every Lark call goes through the bot's NyxID-brokered Lark
OpenAPI — `nyxid_proxy { slug:"api-lark-bot", path:"/open-apis/…", method }`. You never hold
Lark tokens; the bot tenant's scopes decide what works. Probe-first; on a 403 report the exact
missing scope verbatim (e.g. `im:message.group_msg`) — do not retry, do not guess, do not
fabricate ids.

## Route by intent (pick exactly one primitive)

| You want to…                                              | Use                          | API                |
|-----------------------------------------------------------|------------------------------|--------------------|
| send / reply / react / read / find messages, chat history | `lark-im-ops`                | im/v1              |
| summarize "who said what" over a window                   | `lark-im-ops` (history)      | im/v1              |
| create / append / read cloud docs (Docx)                  | `lark-docx-ops`              | docx/v1 + drive/v1 |
| read / append / overwrite spreadsheet ranges              | `lark-sheets-ops`            | sheets             |
| operate Base / 多维表格 records                            | `lark-bitable-ops`           | bitable/v1 + drive |
| free/busy, find a slot, create / update events            | `lark-calendar-ops`          | calendar/v4        |
| check / list approval status                              | `lark-approval-status-probe` | approval           |
| SUBMIT an approval instance                               | matching approval workflow   | approval           |

Value-shape footguns: `im` content is a JSON string not an object; `bitable` writes by field
NAME (date = ms timestamp, person = `[{"id":"ou_…"}]`, select = an existing option name); extract
`spreadsheet_token` / `doc_token` / `app_token` from the share URL. After creating a Base/Doc,
grant the requester via `drive/v1/permissions/{token}/members` (member from the channel-context
sender_id).

## Dependency map

```
Consumers (19 payload-builders: approval ×7 · reporting ×6 · recruiting ×4 · misc ×2)
    │  compose, do not re-implement
    ▼
Core ops:  im-ops · docx-ops · sheets-ops · bitable-ops · calendar-ops · chat-recall · approval-status-probe
    │  all via
    ▼
NyxID proxy (slug api-lark-bot) → Lark OpenAPI
```

## Health / cleanup (as of 2026-06-26)

- `lark-chat-recall` overlaps `lark-im-ops` (same im/v1 history) — prefer im-ops; recall is the legacy alias.
- `lark-calendar-ops` and `lark-approval-status-probe` are private + on the older SKILL.md shape — owner-only until org-shared and upgraded.
- Gaps (no bot-side ops yet): contacts, standalone Drive, mail, tasks, wiki, minutes, VC, whiteboard.

## Re-discover live (do not trust this list blindly)

The roster drifts. To get the current set, search the registry instead of relying on this file:
`ornn skill-search scope=mine q=lark` (and scan each item's tags for `lark`).

## Guardrails

- Echo and confirm before any write or send; never invent ids; never delete unless explicitly asked.
- One primitive per area — do not re-implement another area's calls inside a workflow.
