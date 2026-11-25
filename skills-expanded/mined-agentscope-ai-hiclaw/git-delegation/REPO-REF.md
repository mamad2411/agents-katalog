# Repo Ref
- source: https://github.com/agentscope-ai/hiclaw (path: manager/agent/worker-skills/git-delegation/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 将所有 git 操作委托给 Manager 执行。Worker 无法直接访问 git credentials，因此任何需要认证的 git 操作（clone、push、fetch 等）都需要通过此机制委托给 Manager。
