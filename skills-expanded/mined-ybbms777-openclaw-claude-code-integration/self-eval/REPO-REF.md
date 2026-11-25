# Repo Ref
- source: https://github.com/ybbms777/openclaw-claude-code-integration (path: skills/self-eval/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 自我评估钩子。每次 session 结束时自动检查三种异常情况（用户纠正/工具重试失败/上报规则触发），有任一情况则写入 reflection 记忆到 LanceDB。无异常则静默退出。
