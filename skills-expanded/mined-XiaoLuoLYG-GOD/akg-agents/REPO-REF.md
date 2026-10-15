# Repo Ref
- source: https://github.com/XiaoLuoLYG/GOD (path: jiuwenclaw/jiuwenclaw/resources/agent/jiuwenclaw_workspace/skills/akg-agents/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: 代理执行 AKG 算子任务。先检查固定仓库与分支；若 `~/.akg/check_env.md` 不存在则强制 `FULL_SETUP=true`；忽略所有 `akg_cli` 检查和使用；后端代码生成直接执行 `run_workflow.py --workflow kernelgen`。
