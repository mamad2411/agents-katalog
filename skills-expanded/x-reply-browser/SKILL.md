---
name: x-reply-browser
description: Use when an agent prepares an X (Twitter) reply draft in the user's signed-in Chrome via BeatBrowser. Covers tab focus, paragraph-preserving input, human publication and durable URL verification.
---

# X Reply via BeatBrowser

Read `docs/playbooks/x-reply.md` before the first live X action.

Workflow: open status URL → focus tab → insert the exact approved text with its paragraph breaks → verify the composer layout → let the user click Reply → verify the published reply and capture its durable URL.

This repository ships no bulk reply publisher. Do not create one as part of this workflow: open the target, prefill the approved reply, and let the user click Reply. Link-bearing drafts require a real blank line before the product bridge/link. Never treat “clicked” as success, never forge GraphQL, and never retry an uncertain submit before checking the target and account replies. Stop on captcha, rate limit, login challenge, warning, or account mismatch.
