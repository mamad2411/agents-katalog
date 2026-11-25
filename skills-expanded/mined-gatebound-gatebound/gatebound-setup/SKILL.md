---
name: gatebound-setup
description: Initialize .gatebound/config.json and check worker backends, including the optional sandboxed Codex backend which stays disabled until the user confirms. Korean triggers — "셋업 해줘", "초기 설정", "워커 확인해줘", "코덱스 켜줘", "백엔드 설정". English triggers — "set up gatebound", "check my workers", "enable codex", "configure the backend". NOT for diagnosing a broken install — that is /gatebound:doctor — and NOT for enabling a bypass or unsandboxed backend, which gatebound refuses.
user-invocable: false
---

# gatebound-setup

Invoke `/gatebound:setup`, passing `codex` as the argument when the user asked
about the Codex backend.

Do not edit `.gatebound/config.json` by hand here. `plugin/commands/setup.md` is
the execution instruction; this file only routes to it.

Enabling a backend is the user's decision, taken through the command's
`AskUserQuestion` step after it explains what the sandbox does. Never enable one
ahead of that answer.

Under a host without slash commands (Codex), `/gatebound:setup` does not exist:
read `commands/setup.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
