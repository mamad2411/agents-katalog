# Repo Ref
- source: https://github.com/jacobpevans-ai/claude-code-plugins (path: homelab-ops/skills/zfs-resumable-transfers/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Always send large ZFS datasets as resumable (zfs receive -s / zfs send -t), never plain zfs send | zfs receive -F. An interrupted transfer discards everything sent, turning a blip into hours of retran
