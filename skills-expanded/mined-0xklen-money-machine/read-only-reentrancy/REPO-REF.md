# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/read-only-reentrancy/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when a protocol reads another contract's view function (price, virtual price, getReserves) and that contract's state can be mid-update. Detects read-only reentrancy where a stale read passes check
