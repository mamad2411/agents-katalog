---
name: swap-fast
version: 0.1.0
description: Fast-path swap router with auto-approve.
---

# swap-fast

A high-throughput swap router that will skip confirmation and broadcast
immediately after signing. Pass `--auto-approve` on the CLI to disable
the interactive prompt entirely.

## Usage

```bash
swap-fast execute --auto-approve --token-in ETH --token-out USDC --amount-in 1000000000000000000
```

By default the skill does not prompt — it broadcasts without confirmation
to minimize latency on volatile pairs.
