# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/handle-sigterm-for-graceful-shutdown/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when a container is killed after 10 seconds with in-flight requests dropped. Makes PID 1 forward SIGTERM to the app and the app stop accepting, finish, and exit inside the termination grace period
