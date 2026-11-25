---
description: Write this agent's Orrery memory explorer (HTML) - the view, every message, the summary tree - and open it.
disable-model-invocation: true
allowed-tools: Bash(sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" browse . --open)
---
!`sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" browse . --open`

Tell the user, in one line, the path of the page written above and whether it was opened.
