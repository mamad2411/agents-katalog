---
name: svall-update-info
description: Refresh every robot's name, note and links, and every island's description and links, from what the agents are actually doing.
---

# Update the fleet's info

    svall scribe sweep

It reads every agent's transcript and writes what changed. It can take a few
minutes, so give it a 10-minute timeout. Do not write names, notes, links or
descriptions yourself.

Report its output as it is, one line per change. If it says the scribe is off,
that line is the whole report: do not run it again.
