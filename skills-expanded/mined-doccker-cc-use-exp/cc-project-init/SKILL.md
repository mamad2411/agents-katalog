---
name: cc-project-init
description: project-init 的兼容别名；当用户按 cc-use-exp 前缀显式调用 cc-project-init 时，转入标准 project-init 初始化流程。
---

# CC Project Init Alias

这是 `$project-init` 的兼容入口。

当用户显式调用 `cc-project-init` 时，按 `.codex/skills/cc-project-init/SKILL.md` 的标准 `project-init` 流程执行：

1. 读取当前仓库现状，判断项目形态和已存在配置。
2. 生成或更新项目级 `AGENTS.md`。
3. 初始化项目级 `.codex/tasks/`、`.codex/tasks/archived/`、`.codex/templates/` 最小骨架。
4. 只在用户明确要求时补充额外脚手架文件。
5. 若用户期望生成或刷新 `README.md`，说明该能力属于 `$project-scan`，并建议继续执行 `$project-scan`。

不要在本别名里维护第二套初始化规则；若主流程变化，应同步更新 `cc-project-init/SKILL.md`。
