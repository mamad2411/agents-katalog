---
name: brain-check
description: Health check for this agent's brain. Use at session start when something feels off, before a critical task, or when $user says brain check, health check, is everything up, status. One brain_status call, reported as a table.
---

## Brain check

1. `brain_status()`.
2. Report:

```
Agent: <name> — Brain Check
Stores:      <each store in `stores`> OK/DOWN (<detail>)
Recall:      vectors <rows> rows, <pending> waiting, worker <up/down> · judge <model> · fell back to keywords <count>× in 7 days (<latest>); only the parts `brain_status` returns
Knowledge:   <pages> pages, <raw> raw, <issue_count> lint issues → <first three>
Context:     <tokens> always-loaded tokens (<per-file breakdown>)
Session:     last start <id> · last close <id> · unclosed: yes/no
Pending:     <n> decisions waiting for $user, or the `executive_state` note when that file cannot be read
Secrets:     <secrets_masked> indexed record(s) hold what looks like a credential (only when present)
Traits:      <grown>/12 grown · <trait: value/n> for each defensible signal that moved the wrong way
Status:      HEALTHY | DEGRADED | CRITICAL
```

3. Rules: any store down → **CRITICAL**, tell $user not to proceed until it is back (a store that is a service: restart it, then `/mcp`). Lint issues, `unclosed: yes` or anything in `attention` → **DEGRADED**, say what to fix (`/distill --lint`, read the unclosed session file, or the reason recall fell back to keywords). `secrets_masked` → tell $user to rotate those credentials and remove them from the files: recall masks them, the files still hold them. Context tokens above the number recorded in `vault/facts.md` → say by how much and what grew.
