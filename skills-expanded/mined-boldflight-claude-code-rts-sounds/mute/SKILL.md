---
name: mute
description: Mute RTS sounds
allowed-tools: Bash
user_invocable: true
---

Mute RTS sounds by creating the mute file:

!`touch ~/.claude/rts-muted`

RTS sounds are now muted. Run `/rts-sounds:unmute` to re-enable, or `/rts-sounds:config` to toggle individual events.
