---
name: sealeap-jiaotu-amazon-major-event-readiness-checklist
description: "Build a countdown-driven readiness plan for a major Amazon sales event by pulling the current promotion-tool deadlines, inbound-shipment cutoffs, and pricing-eligibility rules from Seller Central rather than a prior cycle's dates, then tier products by margin for promotion-tool assignment and phase ad budget and safety stock around the event window. Profit and inventory guardrails are calibrated to the account's own margin and sell-through data, not fixed percentages. Use for 大促报名截止核对、活动前库存备货、大促广告预算分阶段、促销工具选择、大促利润红线设置. Do not use to copy a previous cycle's exact deadlines, fee structure, or discount thresholds without reconfirming them for the current event."
---

# Amazon 大促备战节奏与执行清单

## 目标

Build a countdown-driven readiness plan for a major Amazon sales event by pulling the current promotion-tool deadlines, inbound-shipment cutoffs, and pricing-eligibility rules from Seller Central rather than a prior cycle's dates, then tier products by margin for promotion-tool assignment and phase ad budget and safety stock around the event window. Profit and inventory guardrails are calibrated to the account's own margin and sell-through data, not fixed percentages.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的预算分阶段比例与竞价上浮幅度是其经验值，需按自身账户历史大促数据重新校准，不作为固定公式套用。
- 促销工具的费用结构（是否收取入场费、抽成比例、支出上限）会随活动与站点调整，必须在提报前于活动页面重新确认，不沿用以往周期的费率。
- 价格资格规则（当前价与历史价的关系、促销天数如何影响后续参考价）由平台当期规则决定，涉及是否会拉低未来基线价的判断以官方当前说明为准。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 在后台活动中心核对本次大促的提报截止、入仓截止日期、促销工具费用结构（是否有入场费/抽成/上限）以及价格资格规则，全部按当前活动页面记录，不沿用往期日期。
2. 把在售产品按毛利与库存深度分层（如高毛利核心款、走量款、清货款），为每层预先匹配可承受的促销工具组合，避免低毛利产品被安排进高成本促销。
3. 按倒排时间表安排预热、爆发、长尾三个阶段的广告预算与竞价方向：预热阶段以积累数据和曝光为主，爆发阶段集中资源覆盖活动峰值时段，长尾阶段转向对未转化访客的再触达；具体预算占比和竞价幅度以账户历史转化数据校准，不套用固定比例。
4. 按"日均销量×大促预计天数×安全系数"估算各SKU的备货量，安全系数按自身缺货成本与账期能力设定；对可能超储的仓储占用提前设清仓触发线。
5. 设置促销期利润红线：包括价格是否会拉低未来的参考价基线、单件净利是否低于可接受下限、广告花费占销售额比例的上限，任一触碰即触发人工复核而非继续自动执行。
6. 活动前完成账户健康与物流状态复检，并在活动结束后按同一套指标做复盘，区分真实增量与活动期正常波动。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 大促倒排时间表（含官方截止日核对记录）
- 产品分层与促销工具匹配表
- 分阶段广告预算与竞价草案
- 备货安全库存与清仓触发线
- 促销利润红线与活动后复盘记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
