---
name: ai-product-orchestrator
description: 当需要设计 AI 原生产品、Agent 功能或大模型应用时使用。按 eval → guardrail → agent UX 三个阶段编排，先定义成功标准，再定义风险边界，最后定义交互体验。关键词：AI 产品、AI 原生、Agent 设计、大模型应用、eval、评测、护栏、guardrail、Agent UX、幻觉、提示注入。
metadata:
  module: "AI 原生产品"
  sub-module: "AI 产品全流程"
  type: "orchestrator"
  version: "1.0"
  domain_tags: ["AI", "SaaS", "通用"]
  trigger_examples:
    - "设计一个 AI 客服助手"
    - "给产品加一个 Agent 功能"
    - "怎么评估大模型输出质量"
    - "AI 功能经常胡说，怎么防"
  interaction_mode: "ai_suggest_human_approve"
---

# AI 原生产品编排器

## 核心原则

**先可评估，再可上线；先防坏事，再谈体验。**

AI 产品的质量是概率分布，不是单次结果。没有 eval 就没有版本比较，没有 guardrail 就没有事故边界，没有 Agent UX 就没有可用的纠错路径。

## 编排协议

遵循 [orchestrator-protocol.md](../../../../templates/orchestrator-protocol.md)。阶段顺序与卡口以运行时定义为准。

```bash
node scripts/orchestrate.js init ai-product-orchestrator
node scripts/orchestrate.js next ai-product-orchestrator
node scripts/orchestrate.js gate ai-product-orchestrator --stage <id>
node scripts/orchestrate.js approve ai-product-orchestrator --stage <id> --by <name>
node scripts/orchestrate.js finalize ai-product-orchestrator
```

机器可读定义：[runtime/pipelines/ai-product-orchestrator.json](../../../../runtime/pipelines/ai-product-orchestrator.json)

## 阶段执行计划

### 阶段 1：eval 设计

调用 `ai-eval-design`。输入产品目标、用户任务、失败模式；输出 `output/pm-ai-product/ai-eval-design/eval_plan.json`。卡口：至少 10 条 eval case、指标与回归策略非空、人类确认成功标准。

### 阶段 2：guardrail 设计

调用 `ai-guardrail-design`。消费 eval plan 的 failure_modes；输出 `output/pm-ai-product/ai-guardrail-design/guardrail_spec.json`。卡口：风险分类、工具权限、升级与降级策略均非空。

### 阶段 3：Agent UX 设计

调用 `ai-agent-ux`。消费 eval plan 与 guardrail spec；输出 `output/pm-ai-product/ai-agent-ux/agent_ux_spec.json`。卡口：交互状态覆盖思考/流式/工具/等待人类/错误恢复，成本与延迟预算已定义，人类确认体验取舍。

### 阶段总结（post_pipeline）

```yaml
post_pipeline:
  - action: stage-summary
    output: output/phase-reports/pm/ai-product-orchestrator.md
```

阶段总结必须包含：执行概览、关键发现、决策记录、产出清单、风险与待办、下游衔接。生成失败时基于已完成产物输出部分总结，缺失项标注"数据缺失"。

## 阶段卡口

| 卡口 | 条件 | 未通过处理 |
|------|------|------------|
| eval 计划通过 | eval_plan.json 通过 Schema + 人类确认 | 补齐用例、指标或回归策略 |
| 护栏通过 | guardrail_spec.json 通过 Schema | 补齐风险、权限或降级 |
| 体验通过 | agent_ux_spec.json 通过 Schema + 人类确认 | 补齐状态、预算或反馈 |
| 阶段总结已生成 | output/phase-reports/pm/ai-product-orchestrator.md 非空 | 补充缺失结构项 |

## 人类决策点

| 决策点 | 触发条件 | 决策内容 |
|--------|----------|----------|
| 成功标准确认 | eval 设计完成 | 确认任务成功与失败模式可接受 |
| 风险接受度 | guardrail 设计完成 | 确认高风险场景的拦截与升级策略 |
| 体验取舍 | Agent UX 设计完成 | 确认延迟、成本、透明度之间的平衡 |

## 异常处理

| 异常类型 | 处理策略 |
|----------|----------|
| 无真实 eval 数据 | 使用合成种子并标注 `synthetic_seed`，不得宣称已验证 |
| 模型能力不足 | 降级为“AI 建议 + 人确认”，并记录能力边界 |
| 工具权限冲突 | 默认只读，写操作强制人类审批 |
| 阶段总结生成失败 | 基于已有产物生成部分总结，标注"数据缺失"，不阻塞编排完成 |
