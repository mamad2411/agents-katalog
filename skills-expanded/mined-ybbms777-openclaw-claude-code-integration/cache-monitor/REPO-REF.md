# Repo Ref
- source: https://github.com/ybbms777/openclaw-claude-code-integration (path: skills/cache-monitor/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 追踪静态层文件 hash，检测 prompt cache 失效。注册为 PreAgentStart 钩子，每次 session 启动时自动运行。有变更时输出警告，无变更静默通过。
