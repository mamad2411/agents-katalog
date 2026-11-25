# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/drain-in-flight-requests-on-prestop/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when rolling restarts drop requests because the pod leaves endpoints and dies too fast. Adds a preStop drain hook that waits for load-balancer propagation before the process exits.
