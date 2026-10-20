# CLAUDE.md

Claude / Codex 在本仓库开发 `scale-engine` 时，默认遵循 `AGENTS.md`。

## 先读

1. `AGENTS.md`
2. `docs/guides/GETTING_STARTED.md`
3. `docs/guides/DEVELOPMENT_WORKFLOW.md`
4. `docs/workflow/README.md`

## 常用命令

```bash
make preflight
make gate-workflow
make gate-quality
make verify PROFILE=default
make scale-smoke TASK='workflow adaptation' FILES='AGENTS.md,README.md'
make workflow-upgrade-check
make workflow-upgrade-plan
make workflow-aios-adopt
```

## 约束

- 没有实际验证结果，不说“已通过”。
- 不确定的事实明确标记为 `[UNCERTAIN]`。
- 修改前先看 Git 状态。
- 需要 shell 命令时优先用 `rtk` 前缀。
