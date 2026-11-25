---
name: caveman-init
description: Safely install persistent Caveman rules in a project. Use when the user asks to initialize or configure Caveman or invokes $caveman-init.
---

Use the bundled pinned upstream tool at `$PLUGIN_ROOT/upstream/src/tools/caveman-init.js`. Default to the current repository and `--only agents` for Codex. Run it with `--dry-run` first, show the exact plan, and apply without `--dry-run` only after the user explicitly approves. Pass other upstream targets only when the user asks for them. Never use `--force` without explicit approval.

For user-level mode defaults, set `CAVEMAN_DEFAULT_MODE` to `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`, or `off`. Do not modify unrelated Codex configuration. Explain that `stop caveman` and `normal mode` turn the current mode off.
