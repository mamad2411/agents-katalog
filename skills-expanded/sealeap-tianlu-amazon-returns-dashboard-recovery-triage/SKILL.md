---
name: sealeap-tianlu-amazon-returns-dashboard-recovery-triage
description: "Use Amazon's returns-insights dashboard to triage which ASINs drive disproportionate returns and negative-review risk, configure differentiated self-serve return/refund rules by cost profile, and evaluate whether high-value returned inventory should route through an official grade-and-resell recovery channel. Recovery economics and alert thresholds are platform-set and category-dependent. Use for 退货控制面板功能落地、退货率与差评预警排查、退款规则配置、回收转售项目评估. Do not use to bypass legitimate customer return rights or to configure refund rules as a way to suppress valid complaints."
---

# Amazon 退货看板与回收分流

## 目标

Use Amazon's returns-insights dashboard to triage which ASINs drive disproportionate returns and negative-review risk, configure differentiated self-serve return/refund rules by cost profile, and evaluate whether high-value returned inventory should route through an official grade-and-resell recovery channel. Recovery economics and alert thresholds are platform-set and category-dependent.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 面板具体功能模块、预警阈值与回收转售项目的收益模型由平台当前设置决定，会随政策调整，操作前以面板实时显示为准，不套用固定比例。
- 自主设置退款规则的适用类目、金额上限与欺诈防控机制以官方当前说明为准，配置前先确认是否存在被滥用的风险敞口。
- 回收转售项目的净回收率因品类、损耗与费用结构差异很大，不能假设对所有产品都有正向收益，需按品类分别测算后再决定是否加入。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、库存阶段、补货与到仓时间
- 断货或备货前后的销量、流量、广告、自然位置和转化基线
- COGS、头程、仓储、平台费、退货和清仓成本
- 可比产品的成熟度、销量区间和需求趋势

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 打开退货控制面板，按退货量与退货率对全部ASIN排序，逐条查看退货率明显偏高的ASIN对应的主要退货理由，判断是页面描述不符、尺码材质问题还是物流损坏等系统性原因。
2. 核对面板中差评比例等绩效预警指标当前的触发口径，对已触发或接近触发预警的ASIN，优先安排页面内容或包装的针对性调整，而不是等账号健康度页面另行提醒。
3. 对低客单价、退货处理成本高于商品价值的品类，评估开启部分退款无需退货或仅退款等自主设置规则，按FBA/FBM分别配置，并记录规则生效范围与例外情况。
4. 对高客单价或退货量大的ASIN，核实当前是否符合加入官方回收转售类项目的条件，评估净回收率与回收费用后再决定是否加入，不假设所有品类收益一致。
5. 利用面板资源中心提供的标准处理流程与场景化建议，对照本账户高频退货场景建立自己的处理模板，而不是逐单临时判断。
6. 定期复查面板数据，确认已调整的页面内容、包装或退款规则是否实际降低了对应ASIN的退货率与差评比例，未见改善的项目重新诊断原因。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- ASIN退货诊断排序表
- 退款规则配置记录
- 回收转售评估与决策记录
- 复查跟踪表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
