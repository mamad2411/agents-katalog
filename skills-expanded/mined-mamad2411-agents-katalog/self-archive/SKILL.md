---
name: self-archive
description: Archive the current thread and release its runtime. Use when the user explicitly asks to "self-archive", "archive yourself", or "archive this thread".
---

# Self-archive

Only act on an explicit request to archive this thread. Never use the thread deletion command.

1. Send a brief closing summary before running commands.
2. Archive this thread and its children. If this fails, report the error and do not stop the runtime.
   ```bash
   <archive-current-thread-command>
   ```
3. After archiving succeeds, stop the runtime. Run nothing afterward.
   ```bash
   <stop-runtime-command>
   ```

Undo: `<unarchive-thread-command>`.

Note: Use the current platform's equivalent commands.
