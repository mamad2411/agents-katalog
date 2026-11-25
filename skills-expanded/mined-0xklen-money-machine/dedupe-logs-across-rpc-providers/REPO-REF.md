# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/dedupe-logs-across-rpc-providers/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when ingesting from several RPC providers in parallel. Keys every log on block_hash, tx_hash and log_index so the same event arriving twice collapses to one row instead of double-counting.
