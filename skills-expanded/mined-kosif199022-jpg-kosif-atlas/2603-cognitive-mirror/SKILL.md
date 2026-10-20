---
name: cognitive-mirror
description: Live extractor for the user's cognitive profile — observes the current or recent conversations to model how they think, decide, and evaluate; 5 modes /loms (current chat), Mine (recent chats), Diff, Query, Harvest (decision instances for DSPy); use for "/loms", "look over my shoulder", "mine my conversations", "update my cognitive profile", "harvest my decisions", "how do I typically approach X", "what's my pattern when". Prefer deep-mirror for bulk raw-log mining, scheduling, or auditing. Data lives in ~/.aai/.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/cognitive-mirror/<file>`.
When installed standalone, resolve those to `<file>` in this directory.

Data note: the profile and harvest data this skill reads and writes are NOT in
this skill directory — they live in the global ambient home `~/.aai/` (see
instructions.md § Data location). Only static doctrine (dimensions, template,
scheduled-task prompts) ships here in `references/`.
