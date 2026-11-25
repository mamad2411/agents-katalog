---
name: devel-jb-codebase-audit
description: "Devel Jb Codebase Audit."
domain: cybersecurity
---

-|
| install   | Yes | Yes | SYNCED   |
| diff      | Yes | No  | CLI-ONLY |

== Summary: X OK / Y issues found ==
```

## Rules

- **Read-only** — never modify files, only report
- **Evidence-based** — every finding must include file path and line number
- **No false positives** — verify with grep before flagging
- **Scope $ARGUMENTS** — if user specifies "flags", only run dimension 1; "handlers" for dimension 5, "oplog" for dimension 6, "api" for dimension 7
