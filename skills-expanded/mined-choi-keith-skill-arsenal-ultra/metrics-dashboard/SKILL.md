---
name: metrics-dashboard
description: "定义并设计产品指标仪表盘,包含关键指标、数据来源、可视化类型和告警阈值。适用于搭建指标仪表盘、定义 KPI、建立产品分析体系或制定数据监控方案时。"
---

## 产品指标仪表盘

设计一套完整的产品指标仪表盘,包含合适的指标、可视化方式和告警阈值。

### 背景

你正在为 **$ARGUMENTS** 设计指标仪表盘。

如果用户提供了文件(现有仪表盘、分析数据、OKR 或战略文档),先阅读它们。

### 领域背景

**Metrics vs KPIs vs NSM**:Metrics(指标)= 所有可衡量的东西。KPIs = 在较长周期内跟踪的少数关键量化指标。North Star Metric(北极星指标)= 一个以客户为中心的 KPI,是业务成功的领先指标。

**好指标的 4 个标准**(Ben Yoskovitz,*Lean Analytics*):(1) 可理解 —— 形成共同语言。(2) 可对比 —— 能跨时间比较,而不是快照。(3) 比率或速率 —— 比绝对数值更有信息量。(4) 能改变行为 —— 黄金法则:"如果一个指标不会改变你的行为,它就是个坏指标。"

**8 种指标类型**:虚荣 vs 可行动(只有可行动的指标才会改变行为)、定性 vs 定量(是什么 vs 为什么 —— 两者都需要;永远不要停止与客户交谈)、探索性 vs 报告性(通过探索数据发现意外洞察)、滞后 vs 领先(领先指标支持更快的学习循环,例如客户投诉可以预测流失)。

**5 个行动步骤**:(1) 用 4 个好指标标准审计现有指标。(2) 更新仪表盘 —— 确保所有关键指标都是好指标。(3) 识别虚荣指标 —— 谨慎使用它们。(4) 区分领先指标和滞后指标。(5) 挑一个问题,深入挖掘数据。

案例研究和更多细节:Ben Yoskovitz 的 [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)

### 操作指引

1. **确定指标框架** —— 将指标分层组织:

   **北极星指标(North Star Metric)**:最能体现核心价值交付的单一指标

   **输入指标(Input Metrics,3-5 个)**:驱动北极星指标的杠杆

   **健康指标(Health Metrics)**:确保产品整体健康的护栏指标

   **业务指标(Business Metrics)**:收入、成本和单位经济模型

2. **为每个指标定义**:

   | 指标 | 定义 | 数据来源 | 可视化 | 目标值 | 告警阈值 |
   |---|---|---|---|---|---|
   | [名称] | [精确计算方式:分子/分母、时间窗口] | [数据来自哪里] | [折线图 / 柱状图 / 数字 / 漏斗] | [目标值] | [何时触发告警] |

3. **设计仪表盘布局**:

   ```
   ┌─────────────────────────────────────────────┐
   │  NORTH STAR: [Metric] — [Current Value]     │
   │  Trend: [↑/↓ X% vs last period]             │
   ├──────────────────┬──────────────────────────┤
   │  Input Metric 1  │  Input Metric 2          │
   │  [Sparkline]     │  [Sparkline]             │
   ├──────────────────┼──────────────────────────┤
   │  Input Metric 3  │  Input Metric 4          │
   │  [Sparkline]     │  [Sparkline]             │
   ├──────────────────┴──────────────────────────┤
   │  HEALTH: [Latency] [Error Rate] [NPS]       │
   ├─────────────────────────────────────────────┤
   │  BUSINESS: [MRR] [CAC] [LTV] [Churn]        │
   └─────────────────────────────────────────────┘
   ```

4. **设定复盘节奏**:
   - **每日**:运营健康度(错误、延迟、关键流程)
   - **每周**:输入指标和参与度趋势
   - **每月**:北极星指标、业务指标、OKR 进展
   - **每季度**:战略复盘与指标重新校准

5. **定义告警**:
   - 什么阈值触发排查?
   - 通知谁、通过什么渠道?
   - 预期的响应时间是多少?

6. **根据用户情况推荐工具**:
   - Amplitude、Mixpanel、PostHog 用于产品分析
   - Looker、Metabase、Mode 用于基于 SQL 的仪表盘
   - Datadog、Grafana 用于运营健康度监控

逐步思考。将仪表盘规格说明保存为 markdown 文档。

---

### 延伸阅读

- [The Ultimate List of Product Metrics](https://www.productcompass.pm/p/the-ultimate-list-of-product-metrics)
- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [AARRR (Pirate) Metrics: The 5-Stage Framework for Growth](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [The Google HEART Framework: Your Guide to Measuring User-Centric Success](https://www.productcompass.pm/p/the-google-heart-framework)
- [Funnel Analysis 101: How to Track and Optimize Your User Journey](https://www.productcompass.pm/p/funnel-analysis)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm)(视频课程)
