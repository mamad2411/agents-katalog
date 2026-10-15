---
name: sf-code-review
description: 执行 SpecForge code_review gate；用于 implementation 完成后，对照 approved spec、tasks、implementation report、changed files 和真实 diff 审查实现是否满足规格、工程规则、安全边界和验证要求。
---

# sf-code-review

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

`sf-code-review` 审查实现是否符合已批准 spec、任务边界、工程规则和安全边界。审查重点是缺陷、回归、越界、漏测和证据缺口，不是代码风格偏好。

## 必读

- `references/review-gate-rubric.md`：diff 对账、spec compliance、外部 `code-reviewer` 使用、finding 分级和 gate 决策。
- `.specforge/core/workflows/stages/code-review/SKILL.md`：内部代码审查母本。
- `.specforge/core/artifacts/templates/code-review.md`：写入骨架。
- `.specforge/core/standards/workflow.md`、`.specforge/core/standards/engineering.md`。
- `.specforge/core/skills/ORCHESTRATION.md`：外部 code review 参考边界。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/artifact-graph-status.mjs
node .specforge/core/scripts/instructions.mjs
```

2. 确认 ready artifact 为 `code_review`，再生成审查产物：

```bash
node .specforge/core/scripts/create-artifact.mjs code_review
```

3. 如果 ready artifact 不是 `code_review`，停止并按 `instructions.mjs` route 处理；不要提前批准 code_review gate。

## 必读证据

按 workflow 读取适用 spec：

| Workflow / 条件 | 必读规格 |
|---|---|
| `feature` / `standard` / `lite` | `requirements.md`、`tasks.md`，适用的 `ui-design.md` / `technical-design.md` |
| `bugfix` / `issue` | `gap-report.md`、`tasks.md` |
| `refactor` | `technical-design.md`、`tasks.md` |
| 有 required `spec_review` gate | `spec_review` 必须为 `APPROVED`，并读取 evidence |

无论 workflow 如何，都必须读取：

- `03-implementation/report.md`
- `03-implementation/changed-files.md`
- `.specforge/wiki/00-index.md` 和本次 work item 引用的相关 wiki（用于核对长期边界、模块事实和 wiki 回写影响）
- 当前 `git status --short --untracked-files=all`
- `git diff --name-only`
- `git diff --stat`
- 关键文件 diff、测试输出、启动验证、迁移、回滚或人工验证证据

## 执行序列

### A. Gate 和证据完整性

1. 检查 required 上游 gate 是否已批准。
2. 检查 `implementation` artifact：`plan.md`、`report.md`、`changed-files.md`。
3. 对比真实 git 状态和 `changed-files.md`，未登记文件、登记但无 diff、未追踪文件都要解释。

### B. 任务覆盖和三向对账

1. 对照 `tasks.md` 每个完成任务的 `_Trace:_`、`_Files:_`、`_Verification:_`、`_Rollback:_`、`_Risk:_`。
2. 每个完成任务必须能追溯到真实 diff 或可信 N/A，以及验证证据或可信 deferred 理由。
3. 每个真实 diff 文件必须能追溯到 approved spec、task `_Boundary:_` 或 implementation report 中的批准偏离说明。
4. 对存量模块，检查真实 diff 是否仍落在 wiki / technical design 指定的入口、模块和上下游边界内；不为 review 临时全仓扫描来补齐边界。
5. `changed-files.md`、implementation report、真实 git diff 三者不一致时，先记 finding，不靠口头解释通过。

### C. Spec Compliance 先行

1. feature / standard / lite：对照 requirements、适用 UI design、technical design。
2. bugfix / issue：对照 gap report 的根因、修复策略和回归测试。
3. refactor：对照 technical design 的行为不变边界和回归策略。
4. 若实现与 approved spec 不一致，优先记录 P0 / P1，不用代码风格建议冲淡主要风险。

### D. 外部 `code-reviewer` 联动

`sf-code-review` 仍是唯一 code_review gate 入口。需要补充安全、性能、正确性、可维护性或测试覆盖检查维度时，按 `references/review-gate-rubric.md#外部 code-reviewer 联动` 读取本地 `.specforge/core/skills/quality/code-reviewer/SKILL.md`。

- 不调用任何外部 code-reviewer agent，包括 `code-reviewer` 和 `superpowers:code-reviewer`。
- 只能读取本地 `.specforge/core/skills/quality/code-reviewer/SKILL.md` 和相关 `rules/*.md`，由 `sf-code-review` 自己完成审查。
- 先读 `code-reviewer/SKILL.md` 总览。
- 只在对应风险存在时读取相关 `rules/*.md`：SQL 注入、XSS、N+1、错误处理、命名、类型标注。
- 第三方输出只能转成 `04-code-review/code-review-v1.md` 中有文件、行号、影响和修复方向的 finding；不要复制外部模板标题。

### E. Code Quality / Risk Review

按顺序审查：

1. 安全、权限、输入校验、日志脱敏、secret。
2. 数据、迁移、回滚、兼容性。
3. API、后台任务、并发、幂等、配置默认值。
4. UI 状态、无障碍、截图或浏览器证据。
5. 新依赖、新脚手架、新环境变量。
6. 测试、启动验证、观察点和 wiki 影响。

### F. 写 review 和更新 gate

1. 写 `04-code-review/code-review-v1.md`，包含输入证据矩阵、diff 摘要、任务覆盖、spec compliance、风险检查、findings 和 decision。
2. `APPROVED` 时：

```bash
node .specforge/core/scripts/gate.mjs code_review APPROVED --evidence 04-code-review/code-review-v1.md
```

3. `REQUEST_CHANGES` 或 `REJECTED` 时：

```bash
node .specforge/core/scripts/gate.mjs code_review REQUEST_CHANGES
node .specforge/core/scripts/gate.mjs code_review REJECTED
```

## 判定表

| 条件 | 状态 |
|---|---|
| 真实 diff 超出 tasks 边界，且没有 approved spec 依据 | `REQUEST_CHANGES` 或 `REJECTED` |
| diff 触碰 wiki 未覆盖的长期模块边界，且 technical design / tasks 未说明 | `REQUEST_CHANGES` |
| `changed-files.md`、implementation report、真实 diff 不一致且缺少可信解释 | `REQUEST_CHANGES` |
| technical design 的 `no` 影响面出现未经批准代码改动 | `REQUEST_CHANGES` |
| technical design 的 `unknown` 被直接实现 | `REJECTED` 或退回 spec |
| required 测试、启动、迁移、权限或安全证据缺失 | `REQUEST_CHANGES` |
| 引入 secret、敏感日志、越权路径、危险默认配置或未受控外部调用 | `REJECTED` 或 `REQUEST_CHANGES` |
| 只有 P2 / P3，且残余风险和 verification 提示清楚 | 可 `APPROVED` |

## Finding 分级

| 等级 | 含义 | gate 影响 |
|---|---|---|
| `P0` | 错误交付、数据 / 权限 / 安全事故、生产不可恢复或明显违背 spec | 必须 `REJECTED` 或 `REQUEST_CHANGES` |
| `P1` | 进入 verification 前必须修复的功能、边界、测试或安全缺口 | 必须 `REQUEST_CHANGES` |
| `P2` | 可进入 verification，但需要明确跟进或补证据 | 可批准但记录残余风险 |
| `P3` | 非阻断的可维护性建议 | 不阻断 |

## 完成标准

- `04-code-review/code-review-v1.md` 有明确 decision。
- `APPROVED` 时 gate 状态与 evidence 路径一致。
- `REQUEST_CHANGES` / `REJECTED` 时 gate 状态已更新，evidence 保持 `null`。
- `REQUEST_CHANGES` / `REJECTED` 时 findings 已明确列出需修复的问题和对应文件。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不用“看起来没问题”批准 gate。
- 不在 review 阶段顺手修实现。
- 不因为个人风格偏好阻断，除非违反 approved spec、项目规则或工程风险底线。
- 不让外部 `code-reviewer` 替代 SpecForge 的 diff、tasks、implementation report 和 gate 对账。
