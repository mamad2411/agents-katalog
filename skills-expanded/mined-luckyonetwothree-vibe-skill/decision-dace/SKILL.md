---
name: decision-dace
description: 当需要执行数据驱动决策闭环或将数据转化为可执行洞察时使用。DACE循环自动化，Define/Analyze由AI自动执行，Conclude由AI辅助人类决策，Execute由AI追踪执行效果。Analyze阶段融合洞察转化能力，将分析结果转化为故事化洞察、决策建议和决策边界标注。关键词：DACE循环、数据决策、决策闭环、数据驱动、决策框架、决策循环、数据分析闭环、用数据做决策、决策流程、怎么用数据推动行动、数据洞察、洞察转化、决策建议、故事化分析、数据故事、数据看不懂、把数据变成人话、数据说明了什么。
metadata:
  module: "产品度量运营"
  sub-module: "决策闭环"
  type: "pipeline"
  version: "2.0"
  domain_tags: ["通用"]
  trigger_examples:
    - "帮我用DACE方法做一个数据决策"
    - "从数据到行动的完整闭环怎么做"
    - "数据分析了但没人执行怎么办"
    - "这些数据说明了什么，帮我解读一下"
    - "把分析结果变成能讲的故事"
    - "数据太干了，帮我转化成可执行的建议"
  interaction_mode: "ai_suggest_human_approve"
execution_depth:
  default: standard
  quick_description: "仅输出决策建议和关键依据"
  deep_description: "完整分析 + 决策树 + 敏感性分析 + 反事实推理"
---

# DACE循环自动化（含洞察转化）

## 核心原则

1. **Define是方向，Analyze是证据**：没有明确目标的分析和没有证据支撑的决策同样危险
2. **Conclude权在人类，Execute追踪在系统**：AI提供选项和边界，人类做最终决策，系统负责追踪执行效果
3. **闭环才是完整**：DACE缺一不可，没有Execute的Conclude是空谈，没有Analyze的Conclude是赌博
4. **数据是起点，洞察是终点，行动是目的**：没有行动方向的洞察只是数据展示
5. **故事化而非术语化**：将"p=0.001"翻译为"99.9%可信度"，让决策者听懂才能行动
6. **边界标注比推荐更重要**：明确哪些可自动执行、哪些需人类确认，比简单推荐更有价值

## 交互模式

🤖→👤 AI建议人类审批

## 输入

| 输入项 | 类型 | 必填 | 来源 | 说明 |
|--------|------|------|------|------|
| OKR数据 | object | 是 | 用户提供 | 目标与关键结果、基线值与目标值 |
| KR进度 | object | 是 | output/pm-strategy/planning-okr/okr.json | 各KR当前进度与偏差分析 |
| 实验结果 | object | 是 | output/pm-metrics-ops/experiment-execution/experiment_result.json | A/B测试结果、异常检测数据 |
| 分析结果-异常 | object | 是 | output/pm-metrics-ops/analysis-anomaly/anomaly_report.json | anomaly报告 |
| 分析结果-漏斗 | object | 是 | output/pm-metrics-ops/analysis-funnel/funnel_analysis.json | funnel报告 |
| 分析结果-留存 | object | 是 | output/pm-metrics-ops/analysis-retention/retention_analysis.json | retention报告 |
| 业务上下文 | object | ○ | 用户提供 | 产品阶段、团队目标 |
| 历史洞察库 | object[] | ○ | output/pm-metrics-ops/decision-dace/insight_library.json | 避免重复 |

详细输入说明见 [references/inputs.md](references/inputs.md)。

## 执行步骤

完整步骤、模板与示例见 [references/steps.md](references/steps.md)。

1. Step 1: Define（定义）🤖
2. Step 2: Analyze（洞察生成）🤖
3. Step 3: Conclude（决策选项）🤖→👤
4. Step 4: Execute（执行追踪）🤖

## 输出

**存储路径**：`output/pm-metrics-ops/decision-dace/`

**输出文件**：`dace_status.json`、`okr_tracking.json`、`action_log.json`、`dace_cycle_report.md`、`decision_insight.json`、`insight_library.json`

运行机制、输出字段与示例见 [references/runtime-and-output.md](references/runtime-and-output.md)。

**输出校验规则**：见 [references/contracts.md](references/contracts.md#输出校验规则)。

## 质量检查

- [ ] DACE 四阶段均有输入、输出与状态记录
- [ ] 每个决策有选项对比、推荐项与人类确认记录
- [ ] 洞察回写 insight_library，且可追溯到数据来源
- [ ] OKR 追踪项与北极星指标对齐
- [ ] 执行追踪有负责人、截止时间与复盘结论
- [ ] P0 决策未获人类确认时不得进入 Execute

## 决策规则

见 [references/contracts.md](references/contracts.md#决策规则)。

## 降级策略

见 [references/contracts.md](references/contracts.md#降级策略)。
