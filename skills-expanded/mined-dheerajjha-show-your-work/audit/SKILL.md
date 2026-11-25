---
name: audit
description: Audit recent coding-agent sessions for claims like "tests pass" that had no matching check after the last edit.
disable-model-invocation: true
allowed-tools: Bash(node:*)
metadata:
  internal: true
---

Run this and show the user its output exactly as printed:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/show-your-work.mjs" audit --days 30
```

Then add at most two sentences: which kind of unbacked claim is most common,
and one concrete habit that would have prevented it. Do not change any files.
