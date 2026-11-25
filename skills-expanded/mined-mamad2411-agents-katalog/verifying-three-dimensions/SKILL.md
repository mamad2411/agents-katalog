---
name: verifying-three-dimensions
description: Use when verifying a forge change — analyze Completeness / Correctness / Coherence three dimensions with concrete prose evidence (file:line / spec:Requirement-id), instead of degenerate "tests pass" binary
---

# forge verifying-three-dimensions

> 本 skill 走 `forge:writing-skills` 协议开发。v4 OpenSpec alignment 简化:删反加固 marker fence / ack 协议,保留三维 prose check 方法论。

## Overview

forge v3 之前的 verify 阶段曾试图把"测试 pass + log_hash"二值判定升级为带 marker fence 的 verify_findings 数组(严重度 + ack 协议),v4 BREAKING 后回退到 OpenSpec 风格:**三维 prose check 直接呈现给用户,marker 不持久化 finding 字段**。

测试 pass 不等于实施完整 — spec 里没被测试覆盖的 Requirement 完全不会被发现。本 skill 提供三维度方法论让 verify 阶段产出可观察、可操作的 prose findings。

## Methodology

**REQUIRED BACKGROUND**:必须先懂 `forge:verification-before-completion`(证据先于声称的纪律)。

核心论点:

- "测试 pass 不等于 spec 覆盖 — 没测试覆盖的 Requirement 完全无声音失败"
- 三维度协议参考 OpenSpec `verify-change.ts` 第 4-7 步:Completeness / Correctness / Coherence 三组检查项,各有自动 + LLM 路径

## When to Use

- `/forge:verify <change-id>` slash command 调用本 skill
- AI agent 主体在写 `.verify-passed` v2 marker 前的 prose 评估阶段
- 手动 review 一个 change 实施完整度(三维度作为 checklist)

## When NOT to Use

- 写 `forge plan`(那是 `forge:writing-plans`)
- 写新 skill(那是 `forge:writing-skills`)
- code review(那是 `forge:receiving-code-review` 或 `/forge:review` slash)

## 三维度协议

| 维度             | 检查项                                                                  | 自动 / LLM     |
| ---------------- | ----------------------------------------------------------------------- | -------------- |
| **Completeness** | task 完成度(checkbox 计数)                                              | 自动           |
|                  | spec 覆盖度(每个 Requirement 在 codebase 有实施证据)                    | 自动 + LLM     |
|                  | task 标 [x] 但 git diff 反向 0 改动(fake completion)                    | 自动(git diff) |
| **Correctness**  | requirement 实施映射(file:line)                                         | LLM(本 skill)  |
|                  | scenario 覆盖(WHEN/THEN/AND 条件在 code 或 test 中体现)                 | LLM(本 skill)  |
| **Coherence**    | design 决策追溯(design.md `## Decision:` / `## Approach:` 段是否被实施) | LLM(本 skill)  |
|                  | 代码 pattern 一致性(命名 / 目录 / 风格 vs 项目惯例)                     | LLM(本 skill)  |

### 主流程

每次 verify 必须**三维度全跑**,不允许跳维度:

1. **Completeness**:
   - 看 `forge validate` 输出的错误(spec-files-missing / coverage_gap 类)
   - 对 spec 每个 Requirement,grep codebase 找实施证据;完全无证据 → 报告"spec Requirement 无实施证据"
   - 对 tasks.md 标 [x] 但 git diff 反向 0 改动:跑 `git diff <previous-base>..HEAD -- <expected-path>` 验证,报告"fake completion"
2. **Correctness**:
   - 对 spec 每个 Requirement,定位实施 file:line
   - WHEN/THEN/AND scenario 在 test 或 code 中找证据;找不到 → 报告"scenario 未覆盖"
3. **Coherence**:
   - design.md `## Decision:` / `## Approach:` 段提到的关键词,grep codebase 比对;实施偏离决策 → 报告"design 决策被偏离"
   - 命名 / 目录 / 风格比对项目惯例;偏离 → 报告"pattern 不一致"

### 输出形式(v4 BREAKING)

三维度 findings **以 prose 形式直接呈现给用户**(对话内 + 必要时改 code 或 spec)。**不写 marker 内 fence 字段**:v4 `VerifyMarker` schema 只 5 个字段(`schema` / `verified_at` / `verified_by` / `pause_decisions?` / `created_by_tool_version?`),无 `verify_findings` / `evidence` 数组。

主代理决策:

- **若发现 Completeness/Correctness 重大问题** → **不写 .verify-passed**,abort 让用户先改 code / 改 spec / 重派 subagent
- **若仅 Coherence 偏离**(命名 / 风格) → 报告给用户,用户决定改不改;不改时仍可写 .verify-passed,但需在对话内显式记录"已知 coherence 偏离 N 项,用户确认接受"

## Prose 标定 example

### Example 1 — Completeness/spec-coverage(blocker)

> specs/auth/spec.md Requirement #3 'refresh rate limit' 在 src/auth/ 0 个 file 提及 'rate-limit' / 'rateLimit' / 'throttle' 关键词。
>
> **Recommendation**:在 src/auth/rate-limit.ts 实现 sliding-window 限流,或修订 spec 移除 #3。
>
> **决策**:blocker — abort verify,user 必须改 code 或改 spec 后重跑。

### Example 2 — Correctness/requirement-mapping(blocker)

> specs/auth/spec.md Requirement #2 'expiry window 默认 24h' 在 src/auth/refresh.ts:42 实现为 `expiryHours = 12`(与 spec 不一致)。
>
> **Recommendation**:改 `expiryHours = 24`,或修订 spec 改默认值。
>
> **决策**:blocker — semantics 不一致直接影响行为,abort verify。

### Example 3 — Coherence/design-traceability(blocker 或 可接受)

> design.md `## Decision: 选用 sliding-window 限流` 在 src/auth/ 实施为 fixed-window(`rate-limit.ts:15` 用 expiryAt + bucket 模式,sliding-window 关键词 0 命中)。
>
> **Recommendation**:实施 sliding-window(按 design 决策),或修订 design.md 改决策为 fixed-window 并写理由。
>
> **决策**:由 user 判 — 若行为符合 spec、仅 design 决策语义偏离,可接受写 .verify-passed(并在对话内记录);若 user 认为应严格遵守 design 决策,blocker。

### Example 4 — Coherence/pattern-consistency(通常接受)

> src/auth/login.ts:23 函数名 `doLogin` 与项目 7 个 handler 文件(src/handlers/)统一 `handleXxx` 命名风格不一致。
>
> **Recommendation**:rename `doLogin` → `handleLogin`。
>
> **决策**:nice-to-have,通常接受写 .verify-passed,把 rename 留给下次 refactor / 加进本 change tasks.md 立刻改。

### Example 5 — Completeness/task-completion(blocker)

> tasks.md#task-4 '加 rate-limit middleware' 标 [x] 但 `git diff HEAD~1 -- src/middleware/` 无相关改动。
>
> **Recommendation**:完成 task-4 实施,或把 task-4 改回 [ ] 然后重跑 /forge:apply。
>
> **决策**:blocker — fake completion 直接违反 verification-before-completion,abort verify。

### Example 6 — Correctness/scenario-coverage(通常接受)

> specs/auth/spec.md Scenario 'expired token retry' 的 WHEN/THEN/AND 在 tests/auth/refresh.test.ts 仅覆盖 happy-path,边缘 case(token 刚过期)无 test。
>
> **Recommendation**:加 tests/auth/refresh.test.ts:'expired-token retry edge case'。
>
> **决策**:nice-to-have — 主流程已覆盖,可接受写 .verify-passed,把加测试留下次 change。

## forge-specific 反向 AI 偷懒倾向

v4 删了 marker fence 与 ack 协议,但 AI 偷懒倾向不变。本 skill 仍承担如下纪律:

### 1. 三维度必须全跑

不允许跳维度。即使 Completeness 全 pass 也必须跑 Correctness + Coherence(典型借口:"测试都过了,看着没问题")。

### 2. 证据必须具体

每条 prose finding 必须含 file:line / spec:Requirement-id / design.md 段落标题;**禁止 vague "could be reviewed" / "consider checking X"**。Vague 等于无效。

### 3. 主代理不能"知道问题但仍写 verify-passed"

若三维度发现 Completeness 或 Correctness 重大问题 → 必须 abort verify,让 user 改 code 或改 spec 后重跑。AI 不允许自决"这条不严重所以照写 .verify-passed"。

Coherence 偏离(命名 / pattern / design 决策)可由 user 判定接受。**user 接受时必须在对话内显式记录**(不写 marker fence,但留对话 audit)。

### 4. fake completion 是 blocker

tasks.md 标 [x] 但 git diff 反向 0 改动是直接违反 verification-before-completion 纪律,无论 user 怎么说都 abort verify。让 user 把 task 改回 [ ] 然后跑 `/forge:apply`。

## 红旗清单 — STOP and Start Over

| 想法                                                        | 现实                                                                                                     |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| "测试都 pass 了,跳 Correctness/Coherence"                   | 测试 pass 只覆盖被写出来的 test。spec 里没测试覆盖的 Requirement 完全 silent。**跳维度 = 重走第 1 维度** |
| "这个 Requirement 在 codebase 没找到,但应该不重要"          | spec 列了 Requirement 但 codebase 0 命中是 blocker — abort verify 让 user 改 spec 或改 code              |
| "vague 'consider reviewing X'"                              | 没有 file:line 的 recommendation 等价无效。重写带具体证据                                                |
| "这条 Correctness 问题我自己判定不严重,照写 .verify-passed" | Correctness/Completeness 重大问题不能 AI 自决接受;abort 让 user 决                                       |
| "三个维度合并写成一段总论"                                  | 三维度必须各自显式呈现(让 user 能逐维度判),合并 = 模糊                                                   |
| "时间紧,只跑 Completeness"                                  | 跳维度是 baseline AI 的典型失败模式。本 skill 存在的全部理由就是挡这个                                   |
| "task 标 [x] 但 git diff 空,user 说没事就行"                | fake completion 是直接违反 verification-before-completion;abort 不妥协                                   |

**全部触发表示:回归三维度协议,从 Completeness 开始**。

## 配套引用

- `skills/_shared/scope-category-guidance.md`:决策表区分 "本 change 立即改" vs "跨 change Out of Scope / Future Work / Non-Goal"
- `src/core/markers/types.ts:VerifyMarker`:v4 marker schema(只 5 字段,无 fence)
- OpenSpec `verify-change.ts`(上游参考):三维度方法论的原始版本

## Bottom Line

**verify 不只是测试 pass — 是三维度 prose 评估**。

三维度发现的 Completeness / Correctness 重大问题是 blocker(abort verify);Coherence 偏离由 user 判定。v4 不在 marker 持久化 finding,但纪律靠 prose 报告 + 主代理 STOP 协议保证。
