# Repo Ref
- source: https://github.com/cai-aa/cae-agent-hub (path: MCP/CST/vendor/cst-runtime-cli/skills/cst-runtime-optimization/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户要求使用 CLI/runtime 执行 CST 参数优化循环、S11 指标迭代、多轮仿真对比时调用此 Skill。本 Skill 依赖 cst-runtime-cli 提供基础设施，不携带 runtime scripts，所有 CLI 调用走 base skill 的 uv run python -m cst_runtime 入口。
