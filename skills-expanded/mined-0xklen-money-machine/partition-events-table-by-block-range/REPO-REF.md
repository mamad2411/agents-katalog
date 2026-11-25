# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/partition-events-table-by-block-range/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when an events table outgrows a single Postgres relation. Partitions by block range so queries prune to a few partitions and old ranges detach for archival instead of slow row deletes.
