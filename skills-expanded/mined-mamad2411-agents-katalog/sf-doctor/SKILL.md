---
name: sf-doctor
description: 检查 SpecForge 仓库健康度；用于用户问当前状态、下一步、是否可继续、结构是否健康，或任何自动推进前。
---

# sf-doctor

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

检查项目状态并给出下一步，不修改产物。

## 启动

运行：

```bash
node .specforge/core/scripts/doctor.mjs
```

必要时补充：

```bash
node .specforge/core/scripts/instructions.mjs
node .specforge/core/scripts/status.mjs
node .specforge/core/scripts/artifact-graph-status.mjs
```

## 内部技能母本

状态汇总和下一步判断前，读取 `.specforge/core/workflows/stages/status/SKILL.md`。状态字段、blocker 解释和路由建议以内置母本为准。

## 关联标准

- `.specforge/core/standards/workflow.md`：状态判断读取顺序、ready / blocked / done 和 gate 状态解释。

## 输出

- 是否接入 SpecForge。
- active work item 数量。
- 当前 stage。
- gate 状态。
- ready artifact 或 blocker。
- 下一步建议路由到哪个子技能。
- `Route` / `Reason` / `Blockers` 必须优先引用脚本输出；不要只根据聊天上下文猜下一步。

## 完成标准

- doctor 通过时，给出下一步子技能。
- doctor 失败时，列失败项和修复方向。
- 如果 doctor 通过但 status 显示 blocker，说明这是流程阻断而不是仓库损坏，按 blocker 的 route 返回修正。

## 不做

- 不修改产物。
- 不批准 gate。
