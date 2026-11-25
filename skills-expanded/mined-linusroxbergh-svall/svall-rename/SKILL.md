---
name: svall-rename
description: Give every robot a short name that says what it is doing.
---

# Rename the fleet

    svall scribe sweep --names

It reads every agent's transcript and renames where the rules allow. It can
take a few minutes, so give it a 10-minute timeout. Do not rename robots
yourself.

Report its output as it is, one line per rename. If it says the scribe is off,
that line is the whole report: do not run it again.
