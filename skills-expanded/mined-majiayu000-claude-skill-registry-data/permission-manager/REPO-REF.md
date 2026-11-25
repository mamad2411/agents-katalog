# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: data/permission-manager/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 管理Claude Code的全局工具权限配置，自动将MCP命令或其他工具添加到allowedTools中，避免每次使用时都需要手动批准。工作流程：确认用户需要添加的命令 -> 确认添加级别(默认全局~/.claude.json) -> 执行添加 -> 验证并提醒重启。
