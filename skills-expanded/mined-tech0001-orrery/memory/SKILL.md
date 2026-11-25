---
description: Show this agent's Orrery memory - messages, view size, summaries, recording state and token use.
disable-model-invocation: true
allowed-tools: Bash(sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" status .), Bash(sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" usage .)
---
!`sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" status .`
!`sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" usage .`

Show the report above to the user exactly as printed, in a code block, with no commentary.
