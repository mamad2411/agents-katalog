---
name: echotik-api-assistant
description: Route natural-language TikTok commerce intelligence requests into authenticated EchoTik API workflows through local scripts. Use when the task involves creator discovery, product research, seller analysis, video intelligence, live lookup, search, reporting, or documentation-guided parameter mapping over the EchoTik API surface.
---

# EchoTik API Assistant

This Claude Code entrypoint points to the shared canonical skill in this repository.

Before any live request:

- check setup status with `node ./configure-echotik-auth.mjs --status`
- if EchoTik auth is not configured yet, ask the user to run `node ./configure-echotik-auth.mjs`
- continue only after the environment variable setup is complete

Read the canonical skill first:

- `../../../.agents/skills/echotik-api-assistant/SKILL.md`

Use the same supporting references:

- `../../../.agents/skills/echotik-api-assistant/references/global-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/influencer-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/product-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/seller-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/video-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/live-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/search-rules.md`
- `../../../.agents/skills/echotik-api-assistant/references/routing-policy.md`
- `../../../.agents/skills/echotik-api-assistant/references/scenarios.md`
- `../../../.agents/skills/echotik-api-assistant/references/orchestration-playbooks.md`
- `../../../.agents/skills/echotik-api-assistant/references/setup-and-auth.md`

Use these repository scripts when needed:

- `./configure-echotik-auth.mjs`
- `./search-echotik-docs.mjs`
- `./echotik-api.mjs`
