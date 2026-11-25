---
name: spot-graph
description: 为当前 Git 仓库启用 CodeGraph，成功提交后自动增量刷新代码图谱。Use when explicitly asked to enable, refresh, or disable post-commit graph updates.
---

在目标 Git 仓库内运行本技能目录下的 `scripts/graph.mjs`。

- `$spot-graph` 或 `/spot-graph` 运行 `node "<本技能目录>/scripts/graph.mjs"`。首次从 npm 获取固定版本的 CodeGraph，将运行时放在 Git 元数据目录，初始化图谱，再安装本地 `post-commit`。重复运行可刷新图谱并更新受管 hook。
- `$spot-graph --off` 传入 `--off`，仅移除内容仍由 Spotter 管理的 hook，保留图谱。
- 主工作树的提交会刷新启用时选定的图谱，包含尚未提交的文件改动。成功时静默，失败时提示，Git 提交仍然保留。
- 遇到已有 `post-commit`、自定义 `core.hooksPath` 或 Git 链接工作树时，报告脚本的提示。项目自管的 hook 应直接调用可信位置的 CodeGraph 安装。

收尾遵循公共规则「统一收尾」：显式调用时报告实际已启用、已刷新或已停用的结果；正常完成无需额外操作。异常时说明失败步骤、图谱与 hook 的实际状态，以及最直接的处理操作，不把初始化失败说成启用成功。提交后自动刷新的成功静默行为保持不变。
