---
name: secure-review
description: "Security review subagent: reads session findings and the AP-* catalogue, produces a structured security assessment. Cannot write or edit files — a reviewer that can edit is not a reviewer. Invoke with /secure-review."
agent: security-reviewer
context: fork
user-invocable: true
disallowedTools: [Write, Edit, MultiEdit]
---

# Security review — /secure-review

Invokes the `security-reviewer` subagent in a forked context.

The reviewer reads the current session findings and the AP-* catalogue;
it does **not** modify any files.

## What the reviewer checks

- Open blockers and errors from session `findings.json`.
- Changed files for patterns that static tools miss (logic flaws, auth, trust boundaries).
- Mapping correctness: every finding references a valid `AP-*` entry.
- Suppressions added this session — each must have a substantive reason.
- Dependency changes — new packages against the AP-AGENT-009 policy.

## Output

The reviewer produces a Markdown report:

```
## Security Review — <timestamp>

### Open findings  (<N> blockers, <M> errors)
...

### Patterns not caught by tools
...

### Suppressions review
...

### Verdict
APPROVE / REQUEST_CHANGES — <one-sentence reason>
```

The report is printed to the conversation; no files are written.

Details for any AP-* ID: `reference/<ID>.md`
