---
name: squad-tick
description: Tick the squad team — surface mentions and file conflicts. Address mentions BEFORE continuing other work.
argument-hint: ""
allowed-tools:
  - Bash
paths:
  - ".squad/**"
disable-model-invocation: true
---

Run:

```bash
squad tick
```

Read the output carefully. If there are unread mentions, address them BEFORE continuing whatever you were doing. A missed heads-up can waste the next hour.

For each mention:
- If it asks a question: post a direct answer via `squad ask @<sender>` or `squad say --to <thread>`.
- If it flags a conflict: pause your current work, look at the file in question, and resolve before continuing.
- If it is a `fyi`: acknowledge briefly if action is needed, otherwise note and continue.

If `tick` reports stale claims (yours), heartbeat them or release them depending on whether you are still working on them.
