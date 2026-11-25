---
name: status
description: Show every CCM Stack rule and what enforces it; turn rules or the voice on and off; ccm doctor. Use for /ccm-stack:status.
---

# CCM Stack status

The CLI lives two folders above this skill's base directory: `node "<base>/../../bin/ccm.js"`.

- `ccm status`: every rule, `on` or `off`, the hook or skill that enforces it, its lesson, and why it is off when it is.
- `ccm doctor`: what works on this machine (Node, config, voice binary, model, player, fallback voice) and what to install.
- `ccm rule on <id>` / `ccm rule off <id>`: turn one rule on or off.
- `ccm voice on|off|stop|test`: the spoken summary.

Show the output as it is, then add one line with what the person may want to do next. Turning a rule off is the person's call; never do it on your own to get past a refusal. When a hook refuses something, do what its message says instead.
