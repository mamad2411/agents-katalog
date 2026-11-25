# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-kjuhwa-skills-hub/stale-singleton-lock-cleanup/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Detect a stale Electron SingletonLock symlink by reading its PID target and checking process liveness with kill -0. Remove the lock if the owning process is gone. Prevents silent launch failures after
