---
name: unmute
description: Unmute RTS sounds
allowed-tools: Bash
user_invocable: true
---

Unmute RTS sounds by removing the mute file:

!`rm -f ~/.claude/rts-muted`

RTS sounds are now unmuted. Run `/rts-sounds:mute` to silence them, or `/rts-sounds:config` to adjust volume and settings.
