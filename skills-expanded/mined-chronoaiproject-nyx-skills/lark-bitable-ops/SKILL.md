---
name: lark-bitable-ops
version: "1.3"
description: Create and operate Lark Base (多维表格 / Bitable) tables through the bot's NyxID-brokered bitable/v1 + drive/v1 APIs — create a new Base and grant the requester access, list a Base's tables and a table's fields, read and filter records, create or update single rows, and batch-write many rows. Handles the app_token + table_id extraction from a Base share URL, writes by field NAME with the right typed value shapes (date = ms timestamp, person = open_id, single/multi-select = existing option names), grants the requester full_access on any Base it creates, and doubles as the bitable-scope probe — on a scope 403 it reports the exact missing permission. Lark Base here is the Bitable database product, distinct from Lark Sheets — use the Sheets skill for plain grid spreadsheets.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - bitable
    - base
    - data-ops
---

# Lark Bitable Ops

Use to **create** a Lark Base or to read/write an existing one — "随便建个多维表格 / 查一下这张表 /
加一条记录 / 把这条状态改成 X / 把这事记到多维表格里" — when no dedicated skill already owns that
table. (For a plain **Lark Sheets** grid spreadsheet — cell ranges, append rows — use the Sheets skill
instead; Base and Sheets are different products with different APIs.)

**You (the agent) run the whole flow yourself** via NyxID-brokered access `nyxid_proxy`
`{slug:"api-lark-bot", path:"/open-apis/bitable/v1/..." | "/open-apis/drive/v1/...", method:...}`.
NyxID injects the bot's `tenant_access_token` server-side — never ask the user for a token. Paths
start at `/open-apis/...`. A scope/permission error is a finding — quote it verbatim and suggest the
fix; never invent ids or fail silently.

## Three footguns

1. **`app_token` + `table_id` both live in the Base URL**:
   `https://…/base/{app_token}?table={table_id}&view={view_id}`. The `app_token` identifies the Base,
   the `table_id` (starts with `tbl`) the specific table. Read them from the URL the user pasted; if
   only the `app_token` is known, list tables (step 1) and pick by title. Never guess tokens or ids.
2. **Write by field NAME, with the right typed shape.** The write body is
   `{"fields": {"字段名": value}}` keyed by the REAL field name from the schema (step 2), and each
   field type wants a specific value shape:
   - text → string; number → number; checkbox → `true` / `false`
   - single-select → an existing option name (string); multi-select → array of existing option names
   - date → millisecond timestamp (number, e.g. `1718000000000`)
   - person → `[{"id":"ou_..."}]` (open_id); link → array of linked `record_id` strings
   - formula / lookup / auto-number / created-time are read-only — never write them.
3. **Who to grant / act on = the requester, from context — never a mention placeholder.** The
   requester is `sender_id` in the injected `<channel-context>` (their Lark **open_id**, `ou_...`).
   "我 / 给我 / 帮我" means the sender → use `sender_id`. `@_user_1`, `@_user_2`, … inside the message
   text are display placeholders for @-mentions, NOT ids — passing one to the permission API returns
   `Invalid parameter`. Never grant to or target an `@_user_N` token.

## Create a Base (and grant the requester)

When the user asks you to create a new Base ("建个多维表格 / 新建一张多维表格"):

1. **Create it.** `POST /open-apis/bitable/v1/apps` body `{"name":"<name>"}` (add
   `"folder_token":"..."` to place it in a folder). Read back `data.app.app_token` and `data.app.url`.
2. **Immediately grant the requester full_access** — a freshly created Base is private to the bot, so
   the user cannot open the link otherwise. Do this BEFORE returning the link:
   `POST /open-apis/drive/v1/permissions/{app_token}/members?type=bitable&need_notification=false`
   body `{"member_type":"openid","member_id":"<sender_id from channel-context>","perm":"full_access"}`.
   Use the requester's real open_id (`sender_id`) — never an `@_user_N` placeholder.
3. **Return** the `data.app.url` and confirm the user now has full access.
4. **Fallback if you have no usable id.** If `sender_id` is empty (or the step-2 member grant is
   rejected, e.g. a cross-app `open_id`), do NOT hand back a link the user cannot open. Instead share
   the Base with the whole tenant/org so any member (including the requester) can open it:
   `PATCH /open-apis/drive/v1/permissions/{app_token}/public?type=bitable`
   body `{"link_share_entity":"tenant_editable"}` (use `tenant_readable` for view-only; this stays
   inside the org — never `anyone_*`). Then return the link and say you shared it org-wide because the
   personal id wasn't resolvable.

To grant someone **other than** the requester, you need that person's real `open_id` (or `user_id` /
`email`, with the matching `member_type`): match an `@_user_N` placeholder to a `mentions` entry from
`<channel-context>` to get the real `open_id`; if you still have no real id, ask for it or fall back
to the org-wide share above — do not guess or pass a placeholder.

## How to run it (existing Base)

1. **Resolve the target (and scope probe).**
   `GET /open-apis/bitable/v1/apps/{app_token}/tables?page_size=100` lists every table with its
   `table_id` and `name`. On a 403 / scope error, report it verbatim, say the bot tenant needs bitable
   scopes (`bitable:app` read/write) or the Base must be shared to the bot app, and stop. Pick the
   `table_id` for the table the user means (default the only table if there is just one).

2. **Discover the schema before writing.**
   `GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields?page_size=100` — note each
   field's `field_name`, `type`, and whether it is required. Map the user's intent onto REAL field
   names; ask only when a required field is genuinely unknowable. Skipping this is the #1 cause of
   failed writes.

3. **Read records.** Default path:
   `GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=100`
   (follow `page_token` for more; filter client-side for small tables). For large tables, try the
   server-side search first:
   `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search`
   body `{"filter":{"conjunction":"and","conditions":[{"field_name":"状态","operator":"is","value":["进行中"]}]}}`
   — if the endpoint or scope rejects it, fall back to the paginated GET and say so. Render a compact
   table of only the columns the user cares about (cap ~20 rows; say how many more exist).

4. **Write.** Echo a one-line preview (table + fields + values) before ANY write and confirm it
   matches the ask.
   - Create one: `POST .../records` body `{"fields":{...}}`
   - Update one: `PUT .../records/{record_id}` body `{"fields":{...}}`
   - Batch (2+ rows): `POST .../records/batch_create` body `{"records":[{"fields":{...}}, ...]}` /
     `POST .../records/batch_update` body `{"records":[{"record_id":"rec...","fields":{...}}, ...]}`

5. **Report.** Reply with what changed — the `record_id`s created/updated, the key field values, and a
   Base deep link when you have one. For reads, the compact table from step 3.

## Failure semantics

- Scope 403 / `99991xxx` token error / bitable `1254xxx` permission code → the bot tenant lacks
  bitable/drive scope or this Base isn't shared to the bot app. Report it verbatim plus the missing
  scope; never retry blindly.
- Permission grant `Invalid parameter` → you passed a non-id (e.g. an `@_user_N` placeholder) as
  `member_id`. Use the requester's real open_id from `<channel-context> sender_id`.
- `NOTEXIST` / 404 → wrong `app_token` / `table_id` / `record_id`; show what you used and re-ask.
- Field validation error (unknown field name, bad option, wrong value shape) → re-read the step 2
  schema, fix the field name / type / shape, retry ONCE; if it still fails, report the request body
  plus the verbatim error.

## Guardrails

- Granting the **requester** access to a Base you just created for them is automatic — do it without
  asking. Only confirm before granting a **different** person or making the Base public/tenant-wide.
- **Never delete** records, tables, or fields unless the user explicitly says delete, names the
  target, and you have confirmed the `record_id` in this conversation.
- Writes are not idempotent — never auto-retry a successful-looking `POST`; verify by reading back.
- Only use real returned data; never invent app tokens, table ids, record ids, field names, option
  values, or member ids.
- Use credentials only through your NyxID-brokered tools — never ask the user for a token.
