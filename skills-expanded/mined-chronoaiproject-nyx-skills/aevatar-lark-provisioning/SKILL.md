---
name: aevatar-lark-provisioning
description: "Lark resource provisioning for Aevatar agents: after creating any private doc/Base/sheet/folder for a user, grant the requester full access BEFORE returning the link, with an org-wide (tenant) share fallback when no personal id resolves. Always-on correctness rule."
version: "1.1"
metadata:
  category: plain
  tag:
    - aevatar
    - aevatar-system
    - lark
    - provisioning
    - permissions
    - overlay-scope-lark
---

### Provisioning resources on the user's behalf

When you create a resource that is private or permission-gated (a doc, a Base / 多维表格, a sheet, a folder, …) for the user, you **MUST grant the requester full access BEFORE you return the link** — a freshly created resource is private to the bot, so the user cannot open it otherwise. On Lark, immediately after the create call, make this grant yourself (do not skip it, do not wait to be asked, do not defer it to a skill):

```
nyxid_proxy {slug:"api-lark-bot", method:"POST",
  path:"/open-apis/drive/v1/permissions/{token}/members?type={obj_type}&need_notification=false",
  body:{"member_type":"openid","member_id":"<sender_id>","perm":"full_access"}}
```

— `{token}` = the new resource's token (Base `app_token` / doc `document_id` / sheet `spreadsheet_token`); `{obj_type}` = `bitable` | `docx` | `sheet` | `folder`; `member_id` = the requester's `sender_id` from `<channel-context>` (NEVER an `@_user_N` placeholder). Only after the grant succeeds do you reply with the link. This same grant call (with the right `member_id` — `sender_id` for 「给我」, or a `mentions` entry's `open_id` for 「给 @某人」) is also how you fulfill an explicit access request on an existing resource.

**Fallback when you have no usable id:** if you cannot resolve a real `open_id`/`user_id` for the person (the `sender_id` is empty and there is no matching `mentions` entry), OR the member grant above is rejected (e.g. a cross-app `open_id`), do NOT return an inaccessible link. Instead make the resource accessible to the whole tenant/org so any member (including the requester) can open it:

```
nyxid_proxy {slug:"api-lark-bot", method:"PATCH",
  path:"/open-apis/drive/v1/permissions/{token}/public?type={obj_type}",
  body:{"link_share_entity":"tenant_editable"}}
```

`tenant_editable` = anyone in the tenant can open and edit (use `tenant_readable` if only viewing is appropriate); it stays inside the org — never use `anyone_*`. Then return the link and tell the user you shared it org-wide because their personal id was not resolvable.
