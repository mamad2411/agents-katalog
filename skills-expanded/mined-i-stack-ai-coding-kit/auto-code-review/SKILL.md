---
name: auto-code-review
description: 用户显式触发的跨模型代码审查工作流。仅当用户明确说 `/auto-review`、`使用 auto-code-review`、`启动跨模型代码审查`，或明确要求“审查并修复”时使用；普通代码生成、修改完成或含糊的“看看代码”不自动触发。默认只读审查，只有用户明确要求 `--fix` 或“审查并修复”才允许主 agent 修改代码。
locale: zh-CN
supported_locales: [zh-CN]
experimental_locales: [en-US]
# i18n/en-US/ 镜像为 experimental/generated（未校验锚点，不对外承诺 en-US 支持）
# 待补齐 sha256 锚点 + 规则 ID 对齐后再声明 en-US。
---

# Auto Code Review

## 强制入口

命中本 skill 时，必须完整阅读 [references/auto_code_review.md](references/auto_code_review.md) 并按其中条款执行。

- 不得以 preamble、Cursor 规则摘要或其它二次摘要代替详规全文。
- 未获得当前请求中的显式授权时，不得探测 reviewer CLI、调用 reviewer 或创建审查归档。
- 运行前置依赖（不随 skill 同步包分发，需宿主环境另行提供）：`env/review.json`（模板 `env/review.json.example`）、项目内 `.auto-review-config.json`、以及 `AUTO_REVIEW_*` 环境变量。配置加载优先级与字段含义见 `AGENT-BRIEF.md` 与 `docs/auto-code-review.md`。

## 九条核心规则

- [ACR-001] **显式授权门**：只有用户明确触发本 skill 才进入审查；代码修改完成本身不是触发条件。配置只能控制能力是否可用，不能代表当前请求已授权。
- [ACR-002] **范围可追溯**：优先审查当前请求中可精确追踪的变更；无法证明范围时，先让用户选择 staged 或 worktree，不得把 `git diff HEAD` 冒充为“本轮修改”。
- [ACR-003] **reviewer 只读**：reviewer 始终只读运行，只输出审查意见，不修改文件。
- [ACR-004] **写权限分层**：默认 `review-only`，主 agent 只仲裁并报告；只有用户明确指定 `--fix` 或“审查并修复”时，主 agent 才可修复并再次审查。
- [ACR-005] **MAX_ROUNDS=3**：`review-only` 只运行一轮；`review-and-fix` 最多运行 3 轮。未收敛时输出 deadlock，不假装通过。
- [ACR-006] **授权后闭环**：显式启动后，执行 review → archive → sync → merge；历史召回已由全局 `historical-recall` 负责，本处不再内联 recall。归档写入 `.plan-reviews/`，且仅属于已授权的审查会话。
- [ACR-007] **可配置 reviewer**：允许配置 reviewer、轮次和单模型降级；`AUTO_REVIEW_ENABLED=false` 是能力级禁用开关，`true` 不构成用户授权。
- [ACR-008] **单模型降级需显式允许**：默认不做同模型自审；只有配置明确允许时才降级，并在日志中标注可信度降低。
- [ACR-009] **执行包与 quorum 证明**：调用 reviewer 前必须生成同一份 review package；每轮必须记录 selected reviewers、Expected reviewer count、raw 输出路径、合法 verdict 和通过/未通过原因。只有同一轮所有 selected reviewers 都输出合法 `VERDICT: APPROVED` 才能通过；缺失 reviewer、缺失 raw、超时或非法 verdict 一律按未通过处理。`review-only` 模式不得声明 gate 已通过，只能报告 reviewers approved, no code changes made。

## 模式

- `/auto-review`：只读审查，不修改工作区。
- `/auto-review --fix`：审查、由主 agent 修复已采纳问题、再次审查。
- 普通实现请求：不触发本 skill。

## 与相邻 skill 的分工

| Skill | 分工 |
|---|---|
| `plan-grill` | 盘问并锁定 PLAN.md（Act 1） |
| `cross-model-review` | 显式审查 PLAN.md（Act 2） |
| **auto-code-review** | 用户显式启动的代码实现审查（Act 3） |
| `engineering-discipline` | 约束主 agent 的工程改动 |
| `cognitive-reasoning` | 约束审查结论的证据与置信度（GR-011~013） |

## 工作流

```text
实施完成 → 用户显式触发 → 选择范围/模式 → 生成唯一 review package 并冻结 selected reviewers → reviewer 只读审查
                                                                                    ├─ review-only：报告并归档（不声明 gate 通过）
                                                                                    └─ review-and-fix：修复 → 再审查 → 归档
```
