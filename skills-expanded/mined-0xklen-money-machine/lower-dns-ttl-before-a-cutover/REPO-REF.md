# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/lower-dns-ttl-before-a-cutover/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when moving a service to a new IP, load balancer, or provider. Drop the record TTL at least one old-TTL in advance so cached answers expire by the time you flip, then raise it back after the chang
