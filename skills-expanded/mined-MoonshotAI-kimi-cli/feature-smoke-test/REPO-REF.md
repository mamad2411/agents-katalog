# Repo Ref
- source: https://github.com/MoonshotAI/kimi-cli (path: .agents/skills/feature-smoke-test/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 针对 Kimi Code CLI 的新增或变更功能，规划并执行可重复的端到端冒烟测试。从 git diff 推断功能边界，读取相关文档和代码，设计测试 prompt，以 --print 非交互模式运行本地 CLI，检查进程退出码和 session 产物，总结预期与实际行为之间的差异。发现问题时自动启动多路并行探查以定位根因。
