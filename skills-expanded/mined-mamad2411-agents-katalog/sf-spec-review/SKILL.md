---
name: sf-spec-review
description: 审查 SpecForge 规格；用于随时 review 已存在的 PRD、requirements、ui_design、technical_design、tasks 等 spec，或在 ready artifact 为 spec_review 时执行实现前 gate。
---

# sf-spec-review

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

`sf-spec-review` 审的是“规格包能不能进入实现”，不是代码实现质量。它只指出 PRD、requirements、UI design、technical design、tasks 的缺口和退回路径；不顺手重写 spec，不实现代码。

## 模式

| 模式 | 触发 | Gate |
|---|---|---|
| Artifact Review | 用户要求 review 某个已存在 artifact，例如 requirements、UI design、tech design、tasks | 不更新 gate |
| Gate Review | ready artifact 为 `spec_review`，或用户明确要求执行实现前门禁 | 更新 `spec_review` gate |

## 必读

- `references/spec-review-gate-rubric.md`：Artifact / Gate Review 执行细则、必审范围、finding 分级、退回路径。
- `.specforge/core/workflows/stages/spec-review/SKILL.md`：内部规格审查母本。
- `.specforge/core/artifacts/templates/spec-review.md`：写入骨架。
- `.specforge/core/standards/workflow.md`、`product.md`、`design.md`、`engineering.md`。
- `.specforge/core/profiles/README.md`：涉及技术选型和 profile 偏离时读取。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/artifact-graph-status.mjs
node .specforge/core/scripts/instructions.mjs
```

2. 如果用户明确要求 review 某个已有 artifact，进入 Artifact Review。
3. 如果 ready artifact 是 `spec_review`，或用户明确要求执行 `spec_review` gate，进入 Gate Review。
4. Gate Review 需要生成审查产物：

```bash
node .specforge/core/scripts/create-artifact.mjs spec_review
```

## 执行序列

### A. 选择 Review 范围

1. Artifact Review：只审用户指定 artifact 和必要上下游证据。
2. Gate Review：读取 `work.yaml`、workflow schema、components flags，按 `references/spec-review-gate-rubric.md#Gate Review 必审范围` 计算必审 artifact。
3. 不要因为文件存在就审，也不要因为文件不存在就自动跳过；Gate Review 以 schema 和 components 为准。

### B. 做完整性和追踪检查

1. 建立 artifact availability matrix。
2. 建立 traceability matrix：用户目标 / PRD / requirements / UI / technical design / tasks / verification 是否贯通。
3. 任一必审 artifact 缺失、确认标记缺失或关键 `[NEEDS ...]` 未闭环时，不得批准。

### C. 做分 artifact 质量审查

按 `references/spec-review-gate-rubric.md#分项审查清单` 检查：

- PRD / brief：为什么做、给谁做、MVP、非目标、成功指标、候选功能是否经用户确认。
- Requirements：可观察行为、AC、边界、权限、失败路径、非目标。
- UI design：Pencil `.pen`、截图、保存后重读、状态矩阵、视觉 review。
- Technical design：影响面、技术/依赖/工具链确认、版本事实、核心决策 review、规则基准和验证策略。
- Tasks：核心字段、条件字段、来源覆盖、验证任务、Playwright 证据要求。

### D. 写 findings 和决定

1. Findings 必须按 `P0 / P1 / P2 / P3` 排序，绑定文件或章节。
2. 每个阻断 finding 必须写 `Return to`：`sf-brainstorm`、`sf-prd`、`sf-requirements`、`sf-ui-design`、`sf-tech-design` 或 `sf-tasking`。
3. Artifact Review 写 `02-spec-review/<artifact>-review-v<N>.md`，并说明不更新 gate。
4. Gate Review 写 `02-spec-review/spec-review-v1.md`。

### E. 更新 gate

Gate Review `APPROVED` 时：

```bash
node .specforge/core/scripts/gate.mjs spec_review APPROVED --evidence 02-spec-review/spec-review-v1.md
```

Gate Review `REQUEST_CHANGES` 或 `REJECTED` 时：

```bash
node .specforge/core/scripts/gate.mjs spec_review REQUEST_CHANGES
node .specforge/core/scripts/gate.mjs spec_review REJECTED
```

## 判定表

| 条件 | 状态 |
|---|---|
| 没有可审查 evidence 文件 | 停止，不得批准 |
| 必审 artifact 缺失 | Gate Review 必须 `REQUEST_CHANGES` |
| 用户确认缺失：MVP、UI 方向、技术选型、依赖、工具链、核心技术设计 review | `REQUEST_CHANGES`，退回对应 `sf-*` |
| 有 UI 影响但没有 Pencil `.pen`、截图、保存后重读或状态矩阵 | `REQUEST_CHANGES`，退回 `sf-ui-design` |
| technical design 存在关键 `unknown` 或 `[NEEDS ... DECISION]` | `REQUEST_CHANGES`，通常退回 `sf-brainstorm` / `sf-tech-design` |
| tasks 缺核心字段或无法追溯到需求 / 设计 / 验证 | `REQUEST_CHANGES`，退回 `sf-tasking` |
| 只有 P2 / P3，且残余风险已记录 | 可 `APPROVED` |

## 完成标准

- Artifact Review：review 文件存在，包含 scope、findings、是否可进入下一阶段和 return path；不更新 gate。
- Gate Review：`spec-review-v1.md` 有明确 decision；`APPROVED` 时 gate 状态与 evidence 路径一致；未批准时 gate evidence 保持 `null`。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不用“看起来没问题”批准 gate。
- 不在 review 阶段顺手补 PRD、requirements、UI design、technical design 或 tasks。
- 不审 implementation diff；代码实现质量交给 `sf-code-review`。
- 不因为赶进度降低用户确认、Pencil 证据、技术选型确认或任务验证要求。
