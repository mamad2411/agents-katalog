# Repo Ref
- source: https://github.com/ybbms777/openclaw-claude-code-integration (path: skills/compact-guardian/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 压缩熔断守护。当 memory-lancedb-pro 自动压缩（auto compaction）连续失败 3 次时，熔断机制触发，停止当前 session 的自动压缩并通过 Telegram 通知用户手动 /compact 处理。在记忆压缩失败后，激活此 skill 进行熔断检查。
