---
name: tarocub-gdocs
description: Create or update Google Docs from a TaroBot Gateway turn using the host's authorized Google account.
---

# TaroBot Google Docs

Use when a user requests a Google document or a Gateway answer needs a document
artifact. Run `tarobot gdocs status` first. It checks local configuration and
saved authorization, not live Google access. For missing configuration, point the
owner to **Settings → General → Google Docs**. The owner must enable Google Docs
API, configure OAuth consent, download a **Desktop app** OAuth JSON to the host,
and run `tarobot gdocs configure --client-file /private/installed-app.json` followed
by `tarobot gdocs auth`. This is not a normal API key. Open the printed authorization
URL on that same host computer; the callback uses loopback. If only authorization
is missing/invalid, repeat `tarobot gdocs auth`. Do not read, copy, print, or transport
credentials. Do not attempt another browser login.

The CLI selects the canonical App/host directory (including `TAROBOT_HOST_DIR`);
use `--state-dir` consistently for a custom host. Import saves a private managed
copy without rewriting unrelated Hub configuration; `auth --client-file` also
imports persistently. Refresh tokens stay in macOS Keychain or Linux Secret
Service. Windows host authorization is not supported. Phones use the connected
host's configuration. The historic skill identifier is retained for compatibility.

Write the intended UTF-8 text or Markdown to a workspace file, then:

```sh
tarobot gdocs create --title 'Document title' --file /absolute/path/document.md
tarobot gdocs update --id DOCUMENT_ID --file /absolute/path/document.md
```

`update` replaces all content in the first tab, guarded by its current revision.
Use it only when replacing that tab is within the user's request. The tool keeps
Markdown as source text; it does not claim rich Google Docs formatting.
Use the JSON `url` returned after the tool's content read-back succeeds. A
partial-write error can contain an existing document link; report the partial
state and retry `update` on that ID rather than creating duplicates.

Gateway turns use this tool for Google Docs. Never route a Gateway document
operation through Feishu SDK, lark-cli, or another account's credentials.
