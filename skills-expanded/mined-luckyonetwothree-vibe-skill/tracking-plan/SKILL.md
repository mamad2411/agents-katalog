---
name: tracking-plan
description: 当需要生成埋点方案时使用。埋点方案自动生成，包含从指标体系反推埋点需求、PRD功能埋点提取、埋点质量检查、PRD一致性校验。关键词：埋点方案、事件设计、属性设计、埋点规范、Tracking Plan、数据采集、加埋点、打点。
metadata:
  module: "产品度量设计"
  sub-module: "埋点方案"
  type: "pipeline"
  version: "2.1"
  domain_tags: ["互联网", "电商", "通用"]
  trigger_examples:
    - "这个功能需要加埋点"
    - "帮我出一份打点方案"
    - "整理一下需要采集哪些数据"
  interaction_mode: "ai_suggest_human_approve"
execution_depth:
  default: standard
  quick_description: "仅输出核心事件列表和埋点清单"
  deep_description: "完整方案 + 数据治理规范 + 隐私合规审计 + 长期演进路线"
---

# 埋点方案自动生成

## 核心原则

1. **全量分析**：对所有可用数据进行系统性分析，不遗漏关键维度
2. **实时感知**：指标体系设计支持实时监控和快速响应
3. **自动归因**：异常波动自动归因到具体原因，减少人工排查
4. **决策规则显式化**：每个告警和升级条件都有明确的量化规则

## 交互模式

**🤖→👤 AI建议，人类审批**

本Pipeline由AI自动生成埋点方案，但关键决策点需要人类审批：
- **必须审批**：埋点业务逻辑正确性
- **必须审批**：隐私合规性
- **建议审批**：埋点优先级调整

## 输入

| 输入项 | 类型 | 必填 | 来源 | 说明 |
|--------|------|------|------|------|
| PRD | string/文件 | 是 | 用户提供 | PRD文档内容（含功能描述、用户流程、核心路径、业务规则） |
| 指标体系 | JSON | 是 | output/pm-metrics-design/metrics-system/metric_system.json | 北极星指标、L1/L2/行动指标 |
| 现有埋点清单 | JSON数组 | ○ | 用户提供 | 已有埋点事件清单 |

详细输入说明见 [references/inputs.md](references/inputs.md)。

## 执行步骤

完整步骤、模板与示例见 [references/steps.md](references/steps.md)。

1. Step 1: 从指标体系反推埋点需求
2. Step 2: 从PRD提取功能埋点需求
3. Step 3: 与现有埋点去重
4. Step 4: 埋点质量检查
5. Step 5: 生成埋点文档
6. Step 6: PRD埋点方案一致性校验

## 输出

**存储路径**：`output/pm-metrics-design/tracking-plan/`

**输出文件**：`tracking_plan.json` + 可读版埋点文档

**输出 Schema**：`schemas/pm/tracking-plan.schema.min.json`

完整字段说明、输出示例与校验规则见 [references/output-and-contracts.md](references/output-and-contracts.md)。

## 质量检查

- [ ] 每个 P0/P1 指标至少有一个对应事件
- [ ] 每个事件有触发条件、属性、关联指标
- [ ] 命名符合 `对象_动作` 规范
- [ ] 核心路径覆盖率 ≥ 0.9，无重复埋点
- [ ] 隐私敏感字段已脱敏或排除

## 决策规则

见 [references/output-and-contracts.md](references/output-and-contracts.md#决策规则)。

## 降级策略

见 [references/output-and-contracts.md](references/output-and-contracts.md#降级策略)。
