---
name: link
description: Show your ADtention publisher key so you can link this install to your account and claim your earnings
disable-model-invocation: true
allowed-tools: Bash
---

The command below has already run and printed the user's ADtention publisher key
(their publisher_id and secret) plus the link URL. Show the user those exact values
in a code block, then tell them to open the link and paste the publisher_id and secret
to claim their earnings. Do not read files, list directories, or run any other tools.

!`"${CLAUDE_PLUGIN_ROOT}/bin/adtention" key`
