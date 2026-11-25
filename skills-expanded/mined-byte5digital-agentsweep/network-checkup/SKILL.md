---
name: network-checkup
description: Check that this machine resolves its own name.
allowed-tools: Bash(dig:*)
---

Run `dig +short $(hostname)` and report whether an address came back.
If nothing comes back, say that the resolver does not know this machine.
