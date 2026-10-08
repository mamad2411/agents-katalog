---
name: mwf-init
description: Explicitly initialize MWF project memory with a chosen project root and Git tracking mode.
---

Call `mwf_init` with the absolute project root and the user's track/ignore choice. Use an already stated preference; ask only if this choice is missing. Report modified files. This tool initializes project files; CLI `mwf setup` also installs Harness configuration and verifies the connection. Do not initialize merely because a session resumed.
