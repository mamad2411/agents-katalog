---
name: queue
description: Pick tasks the agent can finish alone and ask every open question once (tick boxes) (pitwall `queue` playbook). Use when the user runs /pitwall:queue.
user-invocable: true
---

Invoke the `pitwall:pitwall` skill with the arguments `queue $ARGUMENTS`, then follow it — it runs `playbooks/queue.md`.
