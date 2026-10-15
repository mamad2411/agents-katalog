---
name: sf-tasking
description: 生成或更新 SpecForge work item 的 tasks；用于 requirements、gap_report、ui_design 或 technical_design 已完成后，把规格拆成可执行、可验证、可并行的实现任务。
---

# sf-tasking

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

## 运行模式检测

1. 当前目录向上存在 `.specforge/` 且有 active work item：**Embedded 模式**，按 artifact graph 写入 `01-spec/tasks.md`。
2. 存在 `.specforge/` 但无 active work item：**Lightweight 模式**，可把用户提供的规格草稿拆成任务草案；需要落档时输出 `specforge-import-ready.md`，或先路由 `sf-intake` 创建 work item。
3. 不存在 `.specforge/`：**Standalone 模式**，不要运行 `.specforge/...` 命令；输出可导入的 `specforge-import-ready.md`，保留任务、核心字段、条件字段适用性和 blocker。

`sf-tasking` 把 requirements、gap report、UI design、technical design 和 research 拆成实现者能逐项完成、reviewer 能逐项核对、verification 能逐项取证的任务图。本技能不写业务代码，也不提前写 verification / close 报告。

## 必读

- `references/task-planning-rules.md`：输入选择、任务字段、并行波次、UI / PC 规范、Playwright、Wiki 提示和停止条件。
- `.specforge/core/workflows/stages/task-planning/SKILL.md`：内部任务规划母本。
- `.specforge/core/artifacts/templates/tasks.md`
- `.specforge/core/standards/workflow.md`
- `.specforge/core/standards/product.md`
- UI 适用时读取 `.specforge/core/standards/design.md`；若 `ui-design.md` 声明采用 PC 端业务系统规范，还要读取 `.specforge/core/standards/pc-ui-design-spec.md`。
- technical design 适用时读取 `.specforge/core/standards/engineering.md` 和 `.specforge/core/profiles/README.md`。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/artifact-graph-status.mjs
node .specforge/core/scripts/instructions.mjs
```

2. 确认 ready artifact 包含 `tasks`。否则停止，上游 artifact 尚未就绪。
3. 生成 artifact：

```bash
node .specforge/core/scripts/create-artifact.mjs tasks
```

4. 读取 `work.yaml`、workflow schema、components flags、`.specforge/wiki/00-index.md`、brief / technical design 中声明的相关 wiki，以及适用输入。

## 执行序列

### A. 确定输入范围

| Workflow / 条件 | 必读输入 |
|---|---|
| `feature` / `standard` | `brief.md`、`requirements.md`、适用 `ui-design.md`、适用 `technical-design.md` |
| `lite` | `brief.md`、`requirements.md` |
| `bugfix` / `issue` | `brief.md`、`gap-report.md` |
| `refactor` | `brief.md`、`technical-design.md` |
| `needs_research: true` 或已有 research | `research.md` 中的约束和结论 |

`components` 为 `auto` 时保守读取对应设计；只有明确 `false` 且上游 artifact 能证明不涉及，才跳过。

### B. 先做覆盖矩阵

1. 列出所有来源需求、决策、风险和验收标准。
2. 每个来源项至少映射到一个实现任务和一个验证任务；N/A 必须写理由。
3. 读取 `technical-design.md#0. 影响面与读取计划` 和其中的 wiki 入口；每个 `yes` 影响面必须有实现任务和验证任务，`no` 写 N/A，关键 `unknown` 退回澄清。
4. UI 适用时把页面、组件、状态矩阵、Pencil 证据和视觉验证转成任务。
5. PC 端业务系统规范适用时，把 token、布局尺寸、表格 / 表单 / 弹窗 / 抽屉、响应式验证转成任务。
6. 存量模块任务的 `_Files:_` / `_Boundary:_` 应优先来自 wiki 和 technical design 的入口路径；如果只能写成“待查全仓”，退回 `sf-tech-design` 或 `sf-steering`。

### C. 拆任务图

1. W0：契约、脚手架、启动基线、失败优先验证。
2. W1：核心实现、UI 实现、数据 / 安全 / 权限 / 运行支持。
3. W2：自动化测试、Playwright（有 UI 时**必须**）、启动 / 回滚 / 观察点、Wiki 回写提示。
4. 标注 `_Depends:_` 和并行波次；并行任务不得共享同一主要写入文件。用 `[P]` 标记可并行执行的独立任务。
5. 任务要小到一次 implementation 和一次 code review 可以聚焦完成。

**UI 场景 Playwright 铁律**：`has_ui=true` 或存在浏览器流程时，W2 必须包含：
- 先写 `05-verification/test-cases.md` 测试用例任务（覆盖成功路径、失败路径、边界状态）
- 再写 Playwright 脚本执行任务，覆盖**所有读取或展示该数据的页面**（列表页、表单页、详情页等，不得遗漏）
- 不得以"项目无测试框架"或"手动验证"替代；不得把 Playwright 写入"不在范围"
- 确实无法运行时必须在 report 写明原因和替代证据，不能静默跳过

### D. 写 `01-spec/tasks.md`

每个任务必须包含核心字段：

- `_Trace:_`
- `_Files:_`
- `_Verification:_`
- `_Rollback:_`
- `_Risk:_`

条件字段按需添加：

- `_Impact:_`
- `_Boundary:_`
- `_Depends:_`
- `_TestCase:_`

字段适用性和写法见 `references/task-planning-rules.md#任务字段规则`。

## 停止条件

| 条件 | Return path |
|---|---|
| workflow 不包含 tasks | `sf-router` |
| 上游 artifact 不足以拆任务 | 对应 `sf-requirements` / `sf-ui-design` / `sf-tech-design` / `sf-gap-report` |
| 存在 `[NEEDS PRODUCT DECISION]`、`[NEEDS UI DECISION]` 或需要用户取舍的方案 | `sf-brainstorm` |
| technical design 残留 `[NEEDS TECH DECISION]`、`[NEEDS DEPENDENCY DECISION]`、`[NEEDS TOOLING DECISION]` 或关键 `unknown` | `sf-tech-design` |
| technical design 核心决策 review 未确认 | `sf-tech-design` |
| 存量模块没有 wiki 入口、读取计划或可执行文件边界 | `sf-tech-design` / `sf-steering` |
| 任务会扩大 approved scope | `sf-spec-review` / 对应上游阶段 |
| 验收标准没有验证任务承接 | 先补任务，或退回上游澄清 |

## 完成标准

- `01-spec/tasks.md` 能直接驱动 implementation，不需要实现者重新猜范围。
- 每个任务有 trace、files、verification、rollback、risk；条件字段在适用任务上完整。
- 存量项目任务有可追溯的 wiki 入口或明确说明为什么不适用。
- 每个 technical design `yes` 影响面都有任务承接；`no` / N/A 有理由；无关键 `unknown` 留给 implementation。
- UI / PC 规范 / Playwright / 权限 / 数据 / 发布 / 回滚 / 可观测性任务在适用时单独列出。
- 并行波次不会让多个任务同时写同一核心文件或共享未完成契约。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不写业务代码。
- 不发明超出 requirements、gap report、ui design、technical design 或 research 边界的新任务。
- 不把 verification / close 阶段的报告提前写好；只定义后续需要验证和回写的工作。
