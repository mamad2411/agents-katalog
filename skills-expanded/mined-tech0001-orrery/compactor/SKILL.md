---
description: Show or pick the summary model of this agent's Orrery memory. Sources are Sign in (openai, openrouter), API key (openai, anthropic, openrouter) and Local. Shared with pi's /compactor.
argument-hint: "[signin|key|local [name [words] | name/model [thinking]] | provider/model [thinking] | reset]"
disable-model-invocation: true
allowed-tools: Bash(sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" compactor:*)
---
!`sh "${CLAUDE_PLUGIN_ROOT}/bin/orrery-run" compactor . --prefix /orrery:compactor $ARGUMENTS`

Show the lines above to the user exactly as printed, with no commentary.
