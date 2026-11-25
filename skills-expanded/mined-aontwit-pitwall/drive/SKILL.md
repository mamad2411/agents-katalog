---
name: drive
description: Start the agent loop — one task per round until the queue is empty or you stop it (pitwall `drive` playbook). Use when the user runs /pitwall:drive.
user-invocable: true
---

Invoke the `pitwall:pitwall` skill with the arguments `drive $ARGUMENTS`, then follow it — it runs `playbooks/drive.md`.
