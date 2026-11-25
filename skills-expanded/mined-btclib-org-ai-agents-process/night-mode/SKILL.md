---
name: night-mode
description: "night-mode — turn night mode on or off in any session, or say whether it is on, since when and what it has deferred"
argument-hint: "[on|off|status]"
---

# Night mode

Do what the word after the skill's name says.
`$PROCESS/process/night-mode.md` says how the night starts and ends,
what status answers and what the night does, and the session reads it
whole whatever the word. A session that has not read
`$PROCESS/process/every-session.md` whole reads it first. `$PROCESS` is
two directories above this skill's own.

- `on` starts the night as `night-mode.md`'s activation says.
- `off` ends it as `night-mode.md`'s paragraph on turning it off says.
- `status` answers as `night-mode.md`'s paragraph on status says.

With no word, do what `on` does where the session's night is off, and
what `off` does where it is on, and say which it did. Where the
session's context no longer holds whether the night is on, say so and
change nothing. With any other word, name the words above and change
nothing.
