# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/unchecked-low-level-calls/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when a contract uses .call/.delegatecall/.send and does not check success, or uses transfer/send assumptions. Ensures every low-level call's return is handled and reverts on failure.
