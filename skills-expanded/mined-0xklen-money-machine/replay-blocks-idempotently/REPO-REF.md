# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/replay-blocks-idempotently/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when blocks must be processed more than once after a reorg, restart or bug fix. Makes every derived write an upsert keyed on chain identity so reprocessing a block changes nothing.
