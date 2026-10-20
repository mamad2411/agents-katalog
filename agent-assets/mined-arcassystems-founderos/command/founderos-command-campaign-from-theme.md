---
description: Turn one theme into a sequenced marketing campaign. Refuses to draft until five gate questions are answered (speaker, objective, audience temperature, channels, success metric). Output is a brief plus 3 to 7 content drafts.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob"]
---

Read `skills/campaign-from-theme/SKILL.md` and run it.

The skill is gated by design. Do not let the user push for drafts before the five gate questions are answered - that is the entire reason the skill exists.

If the user names a brand by display name, look it up under `brands/*/`. If no match, ask for the slug or offer to run `brand-voice-interview`.

If the operator has no brands set up, the campaign defaults to operator voice from `core/voice-profile.yml`.
