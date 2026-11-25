---
name: pipeline-0to1
description: >-
  NeonForge 本仓的 0→1 阶段流水线推进器（ADR-026）：9 段＋横切审计/经验沉淀，
  工件冻结为唯一接口、出口闸红不放行、闸结果记 .handoff。当开始新一段、段内产出
  工件、段出口过闸、或需要判断「现在在哪段/下一步做什么」时使用。只管推进与拦截，
  不替段内技能干活（各段有自己的执行技能，见段表）。仅适用于 NeonForge 仓——正文绑
  ADR-026、docs/decisions、docs/audits、.handoff 与段6 闸这套布局，别的仓没有即不适用。
  NOT for: 段内干活本身（写阶段契约用 stage-spec、拆计划用 writing-plans、执行计划用
  executing-plans、跑阶段 DoD 门禁用 stage-gate）——本件只判「现在在哪段、能不能放行」。
slug: pipeline-0to1
version: 1.0.0
displayName: pipeline-0to1
---

# Pipeline 0→1（本仓限定）

全文权威＝`docs/decisions/026-pipeline-0to1-and-stage-isolation.md`（ADR-026）。本件是推进机制的操作面；与 ADR 冲突时以 ADR 为准并回报用户。

## 段表与执行技能

| 段 | 产出物（冻结工件） | 出口闸 | 执行技能 |
|---|---|---|---|
| 0 问题定义与范围 | 问题陈述＋goals/non-goals＋术语种子 → `docs/neonforgeV1.0.0/` | **用户裁定** | ddd-scope, problem-statement |
| 1 产品定义 | 产品轴裁定→L0 母本 → 新树 | **用户裁定**＋独立审计 | write-spec, prd-development, positioning-* |
| 2 领域战略设计 | 子域＋上下文地图＋通用语言表 → 新树 | **用户裁定**＋独立审计 | ddd-discover/subdomains/contexts/context-map |
| 3 领域战术设计 | 聚合/不变量/事件目录 → 新树 | AI 自查＋独立审计 | ddd-aggregates/domain-interactions/model-review |
| 4 计划制定 | 计划＋stage-spec → `docs/design/`、`docs/design/stage-specs/` | AI 自查＋独立审计 | writing-plans, stage-spec |
| 5 详细设计 | 接口/契约/时序（落进计划工件） | AI 自查＋独立审计 | codebase-design, architecture-patterns |
| 6 实现落地 | 代码＋单测 | 双 tsc＋L1＋lint＋脱敏闸 | executing-plans；可派外部 agent（agent-dispatch） |
| 7 测试验收 | DoD 逐条执行结果 | **用户裁定**（stage-gate PASS 前提） | ddd-qa-chain, stage-gate, verification-before-completion |
| 8 部署发布 | 版本号＋CHANGELOG＋tag | AI 自查（建设后置：详设排在段7 首次 PASS 后） | version-management |

横切A 独立审计：每段出口，按 `agent-dispatch` 派异构执行者，报告→`docs/audits/`，结论回用户。
横切B 经验沉淀：随时；段出口必查 `.handoff` 状态是否更新。

## 推进流程

1. **定位当前段**：`handoff view`（next/status 槽）＋新树工件现状。拿不准→问用户，不猜。
2. **段开工检查**：上一段闸已绿（handoff 记录或闸命令现场重跑）；红→停，报用户。
3. **段内作业**：只用本段执行技能；产出写进本段工件文件。**禁止跨段作业**——发现上游工件有错：停下，报告，回退到上游段改工件、重过闸，不在本段就地打补丁（ADR-012/026 铁律②）。
4. **段出口**：
   - 冻结工件（commit；声明前先 `git show --stat`＋逐条 grep 核 diff——p000161）；
   - 跑本段出口闸，留新鲜命令证据；
   - 需独立审计的段→派审计（agent-dispatch），报告落 `docs/audits/`；
   - 闸结果＋审计结论经 handoff CLI 写入（禁手改 `.handoff/`）；
   - 用户裁定档（0/1/2/7＋全部审计结论）→汇报并**等裁定**；AI 自查档→报告备案后放行。
5. **放行**：闸绿＋（如需）用户裁定通过 → 下一段开工。

## 拦截条件（见到即停）

- 上一段闸红或未记录，却要开下一段；
- 讨论态结论未落工件就被引用（「我们刚才说过」不算输入——铁律①）；
- 实现段出现设计变更需求（走回退，不走就地改）；
- 同一回溯路径第 3 次触发 → 标记「需人工介入的架构决策」，报用户。

## 小修补（无豁免通道，用户 2026-10-05 改判）

一切变更一律走流水线。小修补（typo、脱敏、格式、依赖小版本）从**段6 进入**：免上游段工件，但段6 闸（双 tsc＋L1＋lint＋脱敏）＋横切B 记录（handoff）照走，闸红一样不放行。

## 追溯矩阵约定

段1 起维护贯通核对：产品轴裁定 → L0 条目 → 上下文/聚合 → stage-spec DoD → 测试用例。载体＝`docs/tests/coverage-matrix.md` 扩展列＋新树内引用，不另建文件。每段出口审计必查上游引用无悬空。
