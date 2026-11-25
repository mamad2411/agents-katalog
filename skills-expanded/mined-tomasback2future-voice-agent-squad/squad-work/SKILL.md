---
name: squad-work
description: Onboard or resume in one step — squad go does init/register/claim/AC/mailbox.
argument-hint: ""
allowed-tools:
  - Bash
  - Read
paths:
  - ".squad/**"
disable-model-invocation: true
---

Use this auto-pick entry only for an explicitly authorized general work session.
A dedicated Dispatcher, assigned Worker, Deployer, Reviewer or Investigator must
follow its own assignment and ownership contract; do not run this command merely
because Squad is installed. The rule is the same for Muse, Claude and Codex.

For an authorized general work session, run the orchestrator:

```bash
squad go
```

`squad go` is idempotent. It will:

1. Run `squad init --yes` if `.squad/` is absent.
2. Register your session as a fresh agent (auto-derived id) if not already registered.
3. Find the top of the ready stack, claim it atomically, and print its acceptance criteria.
4. Flush any unread chat into your context.

If a claim is already held by your agent, `squad go` resumes it — re-prints AC and re-flushes mailbox.

After the command returns:

- Read the printed AC line by line; the contract is that exact list.
- Address any mention from the mailbox flush BEFORE writing code.
- Invoke the `squad-loop` skill and proceed from step 4 (work the item) onward.

If the output says `no ready items`, ask the user what they want done; then file an item and re-run `squad go`.
