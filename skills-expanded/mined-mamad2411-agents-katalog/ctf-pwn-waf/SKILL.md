---
name: ctf-pwn-waf
description: Use when pi needs the local pwn_waf toolset for AWD PWN traffic capture, traffic forwarding, or defensive wrapper deployment around a pwn service. Trigger on mentions of pwn_waf, AWD PWN defense, catch mode, forward mode, or ptrace-based traffic logging for a pwn binary.
---

# Local Assets

- Tool root: wherever the `pwn_waf` source tree is cloned (build with `make`).
- Docs: `doc.md`, `README.md`
- This directory is source-based and centered around `make`-built modes such as `catch`, `i0gan`, `forward`, and `forward_multi`.

# Workflow

- Confirm competition rules or lab authorization before suggesting use.
- Identify the protected pwn binary path and a writable log directory first.
- Adjust the Makefile values before compiling a specific mode.
- Prefer `catch` for observation and use defensive/forwarding modes only when the user explicitly wants them.

# Common Commands

```bash
make
make catch
make i0gan
make forward
make forward_multi
```

# Notes

- `catch` logs interactions.
- `i0gan` is a stronger defensive mode.
- `forward` and `forward_multi` relay attacker traffic to other targets; treat these as sensitive.
