---
name: bulk-reader
description: "Delegate bulk file reading to a cheap worker model. Use when you need to read a file over 350 lines, answer a question across 3+ files, or summarize a large diff."
---

```bash
"${extensionPath:-$HOME/.gemini/extensions/shunt}/plugins/shunt/scripts/bulk-read" --question "<question>" --paths <file1> [<file2> ...]
```

Each call is independent. To ask a follow-up, ask again with the same `--paths` — the files
go to the worker, never into your context, so re-sending them costs you nothing.

Verify specific line numbers or exact values before using them in edits.

If neither variable is set in your shell, the refusal from the BeforeTool gate names the
absolute path to the script.
