---
name: plan-review
description: "用户触发 /ezfl:lock，或要求工程评审 / 锁定计划 / review architecture / tech review，或描述了一个非平凡变更（>3 文件、新增组件、跨模块改动）且处于编码前阶段时必须使用本 skill。以工程经理视角对计划/提案做对抗式评审（架构、数据流、边界情况、测试覆盖、性能），目标是找漏洞而非走过场。**不要**用于：简单 bug 修复 / 单文件改动 / 纯文档配置改动 / 已经在编码中要求'评审已写好的代码'（那是 code review，不是 plan review）。"
---

# Plan Eng Review

<HARD-GATE>
禁止修改提案材料（proposal.md / design.md / specs/ / tasks.md）——本 skill 仅做评审，结论写入 review-report.md。当存在未消化的 Critical / Important 问题时禁止把 STATUS 标记为 DONE。critical-tier 变更禁止跳过 Outside Voice（cross-review-agent）。
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: lock — 使用 easy-flow:plan-review skill。`

## Overview

工程经理模式的计划/提案评审 skill。在写代码之前，锁定架构、数据流、测试覆盖、性能。以"找漏洞而非走流程"为目标，以"一问一议"的方式与用户交互逐项落实。**宿主中立**（subagent 启动方式由 `./references/host-adapters.md` 按宿主分发）；**模型可配置**（跨模型交叉评审用的 subagent 模型在 `config.yaml: challenger.model` 由用户声明，不在 agent 文件 frontmatter 中硬编码）；**业务工作流解耦**——本 skill 只接受"提案材料路径 + 输出路径"作为输入，业务概念由调用方（如 easy-flow lock 链）按 `./references/caller-contract.md` 履约。

## 配置加载

进入 skill 后首先读项目根 `config.yaml`（缺失则全部走 `config.example.yaml` 给出的默认值，跳过加载并在评审报告开头记一行"使用默认配置"）。可配置项摘要：`challenger.{enabled, model, prompt_mode, share_user_decisions}` / `scope_challenge.{max_files, max_new_services}`。配置缺失**不阻断**。

## 流程总览

```
读 config → Step 0 范围挑战 → Section 1-4 顺序评审 → Outside Voice → 必需输出 → 写 review-report.md
```

每个阶段的"做什么"在对应 policy 文件，本 SKILL.md 仅承载入口、HARD-GATE 锚点与跨阶段衔接。

## Step 0：范围挑战（Scope Challenge）

`read_file ./policies/scope-challenge.md` 并按其执行：6 个子节（已有代码盘点 / 最小改动集 / 复杂度检查 / 搜索检查 / TODOS 交叉引用 / 完整性检查）。复杂度命中阈值（默认 8+ 文件 或 2+ 新服务）→ 主动 `ask_followup_question` 提议 scope reduction，等待用户答复后继续；未命中 → 直接进 Section 1。

**关键铁律**：一旦用户接受/拒绝 scope reduction，**完全 commit**——后续评审节绝不再重提缩减建议。

## Section 1-4：四节评审

`read_file ./policies/four-section-review.md` 并按其执行四节顺序评审：架构 → 代码质量 → 测试 → 性能。

**STOP 规则**：每节内"一问一议"——每个发现单独发起一次 `ask_followup_question`，**不打包**（详见 `./references/output-format.md` 第 3 节）。只有当本节所有问题都已被用户决策（A/B/C 之一，或显式跳过）后，才进入下一节。

测试评审完整方法论（7 步法、E2E vs Unit 决策矩阵、回归测试铁律、ASCII 覆盖率图）见 `./references/test-review-methodology.md`，是本 skill 最重的一节。

## Outside Voice — 独立交叉评审

四节评审完成后,**必须先询问用户是否进入交叉评审**,并基于本次变更的实际复杂度给出建议:

```
通过 ask_followup_question 询问:

🔍 主评审已完成。是否启动 Outside Voice 独立交叉评审?

建议: <根据 openspec 四件套中的改动范围与任务复杂度判断>
  - 涉及多模块/跨层架构/高风险接口变更/任务数≥5 → "强烈建议(变更范围大、复杂度高)"
  - 单模块变更/中等任务量 → "建议(有一定复杂度,交叉评审有助于发现盲区)"
  - 纯配置/文档/单文件小改动 → "可跳过(变更简单,交叉评审收益有限)"

A. 启动交叉评审
B. 跳过,直接完成 lock
```

用户选 B → 在 review-report.md Completion Summary 标注 `Outside Voice: skipped (user decision)`，跳到"必需输出"节。
用户选 A → 继续下方启动流程。

通过宿主原生 subagent 机制启动一个独立的 challenger，用与主评审**不同的模型**对提案材料做第二次评审。详细启动方式、输入构造、可信度门禁：先 `read_file ./policies/outside-voice.md` 并按其中规定执行。

challenger 先 `read_file ./references/host-adapters.md` 并按其中规定通过宿主原生 subagent 机制直接派发 `cross-review-agent`（由 session-start 注册到宿主 agent 目录，无需经 selector 选择）。

### 宿主不支持 subagent 时的行为

直接跳过 Outside Voice 节，在 review-report.md 的 Completion Summary 标注 `Outside Voice: not run (host lacks subagent capability)`。**不再支持 inline 降级**——同 context 注入 challenger prompt 的独立性已被实证不可靠，效果优先原则下宁可不跑也不假跑。

## 必需输出

**强制前置**：写 review-report.md 前必须 `read_file templates/review-report-template.md`，并输出 `[easy-flow lock] 已 read_file templates/review-report-template.md`。**禁止**未读模板就写报告。

先 `read_file ./references/output-format.md`。评审完成后，以下章节缺一不可（详细格式见其中规定）：

1. **NOT in scope** — 显式推迟的工作清单
2. **What already exists** — 现有代码盘点
3. **Failure modes** — 失败模式表 + critical gap 清单
4. **Worktree 并行化策略** — 仅在多条独立工作流时产出，否则一句话"顺序实施，无并行机会"
5. **Completion Summary** — 评审完成摘要表
6. **STATUS** — 四选一（DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT）

**Unresolved Decisions**：用户跳过/打断/未答某 `ask_followup_question` 时**绝不静默默认某选项**，在 Completion Summary 末尾单列「未解决的决策」章节（详见 `./references/output-format.md` 第 7 节）。

**Escalation**：任务尝试 3 次失败 / 安全敏感不确定 / 范围超出可验证能力 → STOP 并升级，使用 STATUS: BLOCKED 或 NEEDS_CONTEXT 格式。**烂工作比没工作糟。** 详见 `./references/output-format.md` 第 8 节。

## 调用方契约

本 skill 是通用提案评审器，不绑定任何特定工作流。调用方（如 easy-flow lock 链）需履行的契约（输入路径列表 / 输出报告章节顺序 / 修改约束 / Constitution Compliance 由调用方追加 / STATUS 硬门禁信号）见 `./references/caller-contract.md`。
