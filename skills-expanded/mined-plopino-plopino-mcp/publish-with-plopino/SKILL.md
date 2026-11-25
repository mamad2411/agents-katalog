---
name: publish-with-plopino
description: Publish an HTML page, Markdown or CSV document, or multi-file bundle to a public Plopino link. Use when the user asks to share, send, publish, or get a link to content Codex produced.
---

Use the Plopino connector to publish content as a public page.

1. Never publish passwords, API keys, access tokens, private credentials, or other secrets. If the user asks to expose them, refuse and suggest non-sensitive content instead.
2. For one text page or document, call `publish_page` with the complete `content`. Pass `filename` when it is not HTML, such as `report.md`, `data.csv`, or `query.sql`; use `index.html` only for a self-contained page.
3. For several related text files, call `publish_files` with each relative `path` and complete `content`. Keep paths inside the bundle. Do not invent binary content; this connector cannot accept inline binary files.
4. If the user wants to replace an existing page and has connected their Plopino account, pass that page's URL as `update_url` so the link stays unchanged. Never claim an update succeeded when the tool returns an error.
5. Return the public URL from the tool result. If a private `claimUrl` is returned, explain that it is only for the publisher and must not be appended to the public link or shown to viewers.

Anonymous pages are public and kept for 30 days. An OAuth-connected Plopino account provides permanent storage and in-place updates. Do not use local paths, do not fabricate URLs, and do not use shell commands for publishing.
