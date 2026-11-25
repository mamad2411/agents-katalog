---
name: foreman-vision
description: Start, stop or check foreman-vision, the live browser view of this machine's Claude Code sessions. Only triggered explicitly by the user via "/foreman-vision start|stop|status|url" (as a plugin, the full name is /foreman-vision:foreman-vision).
argument-hint: "start | stop | status | url"
disable-model-invocation: true
---

# foreman-vision

Arguments: `$ARGUMENTS`

Take the first word of the arguments; with none, use `status`. If it is not one of `start`, `stop`, `status` or `url`, reply with the usage `/foreman-vision start|stop|status|url` and run nothing. Otherwise run:

```bash
bash "${CLAUDE_SKILL_DIR}/../../bin/fv-server.sh" <word>
```

- `start` - starts the server unless it is running, then prints the URL.
- `stop` - stops the server. Every Claude Code session on the machine shares this one view.
- `status` - prints `running <url>` or `stopped`.
- `url` - prints the URL; it opens this session's floor.

Reply with the script's output in one line. On an error, show its output as it is; do not work around it.
