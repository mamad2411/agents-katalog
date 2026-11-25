---
name: restart-herd
description: Restart the local Herd server for this repository when the user asks to restart, relaunch, or recover the app or dev server.
---

# Restart Herd

Use this skill only in the Herd repository.

Run the repo script:

```bash
bash ./scripts/restart-herd.sh
```

Then verify the restart:

```bash
lsof -iTCP:3456 -sTCP:LISTEN
tail -n 20 /tmp/herd.log
```

Rules:

- Prefer the repo script over ad hoc restart snippets.
- Run the restart as one foreground command unless you are actively debugging a failure.
- Report whether port `3456` is listening and point the user to `/tmp/herd.log` for server output.
