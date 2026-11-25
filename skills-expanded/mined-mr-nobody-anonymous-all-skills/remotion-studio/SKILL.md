---
name: remotion-studio
description: Preview a Remotion video
version: 4.0.526
source: "https://github.com/guanyang/open-agent-hub"
source_repository: "guanyang/open-agent-hub"
source_path: "skills/remotion-studio/SKILL.md"
license: "Apache-2.0"
imported_at: "2026-09-20"
---

Execute the following command:

```bash
npx remotion studio --no-open
```

If the Studio is already opened, the URL will be printed and the command will exit.
Otherwise, a long-running process will start, and the URL will be printed.

Open the URL in the browser.

## Useful flags

| Argument          | Purpose                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------- |
| `--log=<level>`   | Set `error`, `warn`, `info` (default), or `verbose` logging.                                  |
| `--port=<number>` | Request a Studio server port; otherwise Remotion finds a free port.                           |
| `--force-new`     | Start another Studio instance even when one is already running for the same project and port. |
