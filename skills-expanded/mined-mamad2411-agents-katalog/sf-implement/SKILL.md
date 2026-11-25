---
name: sf-implement
description: 根据已批准的 SpecForge tasks 执行实现；用于 implementation ready，且需要按任务边界、技术选型、UI/技术设计、验证计划落地代码并记录实现证据时。
---

# sf-implement

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

`sf-implement` 负责把已批准 tasks 落成真实代码、命令和证据。实现完成的定义是：代码、task 状态、验证记录、`changed-files.md` 和真实 git diff 五者一致。本技能不批准 `code_review` gate。

## 必读

- `references/implementation-execution-rules.md`：任务边界、失败优先验证、脚手架、UI / PC 规范、diff 对账和报告规则。
- `.specforge/core/workflows/stages/implementation/SKILL.md`：内部实现母本。
- `.specforge/core/artifacts/templates/implementation-plan.md`
- `.specforge/core/artifacts/templates/implementation-report.md`
- `.specforge/core/artifacts/templates/changed-files.md`
- `.specforge/core/standards/workflow.md`
- `.specforge/core/standards/engineering.md`
- 需要实现 UI 时读取 `.specforge/core/standards/design.md`；若 `ui-design.md` 声明采用 PC 端业务系统规范，还要读取 `.specforge/core/standards/pc-ui-design-spec.md`。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/instructions.mjs apply
```

2. 如果 implementation 不是 ready，停止，上游 artifact 或 gate 尚未就绪。
3. 生成实现产物：

```bash
node .specforge/core/scripts/create-artifact.mjs implementation
```

4. 读取 `work.yaml`、`01-spec/tasks.md`、适用的 `requirements.md` / `gap-report.md` / `ui-design.md` / `technical-design.md`、`02-spec-review/spec-review-v1.md`、`.specforge/wiki/00-index.md` 和任务 / 技术设计引用的相关 wiki。
5. 运行：

```bash
git status --short --untracked-files=all
```

记录本次开始前已有改动；不要覆盖、回滚或登记无关改动为本次成果。

## 执行序列

### A. 先写实现计划

1. 从 tasks 建立任务执行图：task -> batch -> `_Trace:_` -> `_Files:_` -> `_Boundary:_` -> `_Verification:_` -> `_Rollback:_` -> risk。
2. 从 `technical-design.md#0. 影响面与读取计划` 和相关 wiki 建立上下文边界：入口路径、关键符号 / 路由、上游 / 下游、测试位置和运行命令。
3. 实现前只沿上述边界读取代码；不得为了“保险”重新全量扫描仓库。
4. 若任务边界、验证方式、回滚信息不足以指导实现，停止并退回 `sf-tasking` 或 `sf-spec-review`。
5. 若存在 `[NEEDS TECH DECISION]`、`[NEEDS DEPENDENCY DECISION]`、关键 `unknown`，停止并退回 `sf-tech-design` 或 `sf-spec-review`。
6. 写 `03-implementation/plan.md`。

### B. 准备实现基线

1. 新项目、新前端、新后端或新模块，优先使用 technical design 选中的脚手架 / 官方 CLI / 模板。
2. 跑通依赖安装、构建 / typecheck / dev server / service 启动中的适用项。
3. 对行为变更，先写或定位会失败的测试 / 检查 / Playwright 用例，再写生产代码。确实不能失败优先时，先在 report 写原因、风险和替代证据。
4. 脚手架、配置初始化、文档记录、删除死代码等不直接表达业务行为的任务，可以先做结构性准备，但必须有对应验证或对账证据。

### C. 按任务小步实现

1. 每次编辑前确认目标文件在 `_Files:_` / `_Boundary:_` 或 approved UI / technical design 范围内。
2. UI 实现必须追溯到 `ui-design.md` 的页面地图、状态矩阵、Visual Style Brief、Pencil `.pen` 和导出截图。
3. PC 端业务系统规范被采用时，HTML / CSS / 组件样式必须使用 `pc-ui-design-spec.md` token，不接受 UI 库默认主题或临时改值。
4. 技术实现必须追溯到 `technical-design.md` 的 API、数据、安全、配置、运行、可观测性和验证策略。
5. 每完成一个 task，运行对应快速验证或写明不能运行的原因；task 状态只能是 `DONE`、`DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_SPEC`。

### D. 持续维护证据

1. 更新 `03-implementation/report.md`：task 状态、实现策略、验证、偏离、风险、code review 提示。
2. 更新 `03-implementation/changed-files.md`：每个真实变更文件、task、批准边界、风险和验证方式。
3. 收尾时运行：

```bash
git status --short --untracked-files=all
git diff --name-only
git diff --stat
```

4. 真实 diff、report、changed-files、tasks 不一致时先修证据或停止，不能进入 code review。

## 停止条件

| 条件 | Return path |
|---|---|
| implementation 未 ready 或 spec_review 未批准 | 停止：上游 gate 未通过 |
| tasks 的核心字段不足以指导实现 | 停止：任务边界不足 |
| 需要修改 `_Boundary:_` 外文件 | 停止：超出批准范围 |
| 存量项目任务需要先全仓查找才能知道改哪里 | 停止：退回 `sf-tasking` / `sf-tech-design` / `sf-steering` 补 wiki 和边界 |
| technical design 仍有关键 `unknown` 或未确认技术 / 依赖决策 | 停止：技术决策未确认 |
| UI 原型、Pencil 截图或 PC 规范 token 缺失但实现依赖它们 | 停止：UI 设计缺失 |
| 快速验证失败且无法在当前 task 范围内修复 | 停止：说明原因，等待用户决策 |

## 完成标准

- `03-implementation/plan.md`、`report.md`、`changed-files.md` 已填写。
- tasks 中完成项有代码、验证或可信 N/A、变更文件登记和状态说明。
- technical design `yes / no / unknown` 影响面对账清楚。
- 属于本 work item 的真实 git diff 均已登记；无关已有改动已排除并说明。
- 没有把 `DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_SPEC` 描述成已完成。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不批准 `code_review` gate。
- 不扩大到未写入 tasks、`ui-design.md` 或 `technical-design.md` 的范围。
- 不顺手修无关问题；需要时新开 work item。
- 不自动安装 / 同步外部 Agent 技能副本，除非用户单独明确要求。
- **不在修复 bug 时顺手改动范围外的代码**（如把同步调用改成 async、修改无关方法签名）；范围外改动必须新开 work item。
- **编辑 Python 文件后，如果自动格式化工具（Prettier 等）修改了缩进，必须立即检查并还原**；Python 缩进有语义，格式化工具可能破坏逻辑结构。
