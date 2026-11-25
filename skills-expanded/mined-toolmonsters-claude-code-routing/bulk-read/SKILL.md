---
name: bulk-read
description: Use when you need to understand one or more large files (over ~350 lines) or read several files to answer one question. Sends the files to a cheap model in one call and returns dense bullets with line numbers. The files never enter your context. Do not use for editing or for subtle debugging.
---

# bulk-read

Run it from Bash. One call, all the files, one precise question:

```bash
~/.claude/bin/bulk-read --question "What does this service do and which methods touch the database?" --paths src/Service.java src/Handler.java
```

Rules:
- Ask the exact question you need answered. Vague questions return vague bullets.
- Follow-ups on the same files are fine, re-send the same paths. Nothing is cached, nothing is stored.
- The answer carries line numbers (`N|`). When you must edit, Read only that section with offset and limit.
- Do not delegate reasoning: debugging, architecture, safety-critical code. Use the bullets to find the right section, then read it yourself.
