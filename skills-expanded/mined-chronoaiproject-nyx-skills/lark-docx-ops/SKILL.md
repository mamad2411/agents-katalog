---
name: lark-docx-ops
version: "1.2"
description: Create and edit Lark cloud documents (Docx) through the bot's NyxID-brokered docx/v1 + drive/v1 APIs — create a document and grant the requester access, append headings and text paragraphs, read a document's plain-text content, and share it with other people or make it tenant-readable. Handles the Docx block model (block_type + text_run elements) and the document-root block_id, grants the requester full_access on any doc it creates, and doubles as the docx-scope probe — on a scope 403 it reports the exact missing permission.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - docx
    - documents
---

# Lark Docx Ops

Use for "把结论整理成一篇飞书文档 / 新建个文档写进去 / 把这段存成 Lark Doc / 读一下这个文档写了什么".

**You (the agent) run the flow yourself** via NyxID-brokered access `nyxid_proxy`
`{slug:"api-lark-bot", path:"/open-apis/docx/v1/..." | "/open-apis/drive/v1/...", method:...}`.
NyxID injects the bot's `tenant_access_token` server-side — never ask the user for a token. Paths
start at `/open-apis/...`.

**Who to grant / act on:** the requester is `sender_id` in the injected `<channel-context>` (their
Lark **open_id**, `ou_...`). "我 / 给我 / 帮我" means the sender → use `sender_id`. `@_user_1`,
`@_user_2`, … inside the message text are @-mention display placeholders, NOT ids — passing one to the
permission API returns `Invalid parameter`. Never grant to or target an `@_user_N` token.

## The footgun: Docx is a block tree, not markdown

A doc's body is an ordered list of **blocks**. You append blocks under a parent block. The document
itself is the root block, so the root `block_id` **equals the `document_id`**. Each block has a
`block_type` and a typed payload whose `elements` carry `text_run`s:

- text paragraph → `block_type:2`, payload key `text`
- heading 1/2/3 → `block_type:3/4/5`, payload key `heading1`/`heading2`/`heading3`
- bullet item → `block_type:12`, payload key `bullet`

A text run is `{"text_run":{"content":"...","text_element_style":{...optional...}}}`. There is no
markdown — convert "##" / "- " yourself into the right `block_type`.

## How to run it

1. **Scope probe (cheap, first if unsure).** `POST /open-apis/docx/v1/documents` with a throwaway
   title is the cheapest write probe, but prefer a read if you already have a doc:
   `GET /open-apis/docx/v1/documents/{document_id}/raw_content`. On 403/scope error, report it
   verbatim, say the tenant app needs docx scopes (e.g. `docx:document`, `drive:drive`), and stop.

2. **Create a document (and grant the requester).** `POST /open-apis/docx/v1/documents` body
   `{"title":"<title>"}` (add `"folder_token":"..."` to place it in a folder). Read back
   `data.document.document_id` and `data.document.url`.
   Then **immediately grant the requester full_access** before handing back the link — a new doc is
   private to the bot, so the user cannot open it otherwise:
   `POST /open-apis/drive/v1/permissions/{document_id}/members?type=docx&need_notification=false`
   body `{"member_type":"openid","member_id":"<sender_id from channel-context>","perm":"full_access"}`.
   Say the `url` and confirm the user now has access.
   **Fallback if you have no usable id:** if `sender_id` is empty (or the grant is rejected, e.g. a
   cross-app `open_id`), do NOT return a link the user can't open — share the doc with the whole
   tenant/org instead: `PATCH /open-apis/drive/v1/permissions/{document_id}/public?type=docx` body
   `{"link_share_entity":"tenant_editable"}` (use `tenant_readable` for view-only; stays inside the
   org — never `anyone_*`), then return the link and say you shared it org-wide because the personal
   id wasn't resolvable.

3. **Append content.** `POST /open-apis/docx/v1/documents/{document_id}/blocks/{document_id}/children`
   body `{"index":-1,"children":[ ...blocks... ]}` (parent block = the document root = `document_id`,
   `index:-1` appends at the end). Example children for a heading + paragraph:
   ```json
   {"index":-1,"children":[
     {"block_type":3,"heading1":{"elements":[{"text_run":{"content":"周报"}}]}},
     {"block_type":2,"text":{"elements":[{"text_run":{"content":"本周完成了 X、Y、Z。"}}]}}
   ]}
   ```
   Append in batches of paragraphs; keep each request under a few hundred blocks.

4. **Read a document.** `GET /open-apis/docx/v1/documents/{document_id}/raw_content` for plain text,
   or `GET /open-apis/docx/v1/documents/{document_id}/blocks?page_size=500` for the structured tree.

5. **Share with someone other than the requester (on explicit request).** The requester is already
   granted on create (step 2). To add another person:
   `POST /open-apis/drive/v1/permissions/{document_id}/members?type=docx&need_notification=false`
   body `{"member_type":"openid","member_id":"ou_...","perm":"view"}` (`perm` = `view`|`edit`|`full_access`).
   You need that person's real `open_id` — never an `@_user_N` placeholder; if you only have a
   placeholder, ask for their id or share the link with the requester.
   - tenant-wide link: `PATCH /open-apis/drive/v1/permissions/{document_id}/public?type=docx` — the
     accepted body fields vary by tenant; send the minimal change, and if it 400/403s, report the
     error verbatim rather than guessing field names.

## Failure semantics

- Scope 403 / `99991xxx` anywhere → verbatim error + the missing docx/drive scope; never retry blindly.
- Permission grant `Invalid parameter` → you passed a non-id (e.g. an `@_user_N` placeholder) as
  `member_id`. Use the requester's real open_id from `<channel-context> sender_id`.
- Block 400 (`invalid block` / parse) → your `children` block shape is wrong; re-check `block_type`
  and that every text payload nests `elements[].text_run.content`.

## Guardrails

- Granting the **requester** access to a doc you just created for them is automatic — do it without
  asking. Only confirm before granting a **different** person or making the doc public/tenant-wide;
  reading is free.
- Never invent a `document_id`, `folder_token`, `open_id`, or member id — read it from context or a
  list call.
- Only use real returned data; never ask the user for tokens — NyxID handles all credentials.
