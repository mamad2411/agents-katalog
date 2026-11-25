---
name: deep-mirror
description: Lifecycle operator for the cognitive-mirror database (not the live extractor) — bootstrap deep-mine of raw agent session logs, weekly Mine/Harvest maintenance, quarterly blind audit; use for "bootstrap the mirror", "deep mine my session logs", "audit the mirror", "mirror status", "is my profile still accurate". Prefer over cognitive-mirror when maintaining/auditing/bulk-mining logs rather than extracting from the current conversation.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/deep-mirror/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
