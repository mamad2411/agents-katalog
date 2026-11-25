---
name: sealeap-tianlu-amazon-deal-event-submission-readiness
description: "Prepare and execute a limited-time-deal submission end to end: clarify the traffic goal, pass a listing-health gate, verify current backend eligibility thresholds, plan inventory lead time, coordinate advertising before/during/after the event, and review post-event ranking and conversion impact. Eligibility thresholds are platform-current and must be reverified at submission time. Use for 秒杀/限时促销活动提报准备、Listing健康度预检、活动库存与广告节奏规划、活动复盘. Do not use to submit a listing that fails the health check, or to treat threshold numbers from past experience as current requirements."
---

# Amazon 秒杀活动提报预检

## 目标

Prepare and execute a limited-time-deal submission end to end: clarify the traffic goal, pass a listing-health gate, verify current backend eligibility thresholds, plan inventory lead time, coordinate advertising before/during/after the event, and review post-event ranking and conversion impact. Eligibility thresholds are platform-current and must be reverified at submission time.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 提报所需的评论数量、星级、价格与销量等具体门槛数字会随类目、站点与平台政策调整，文中数值仅为该时点参考，提报前必须以后台实时提示为准。
- 活动对排名与自然流量的拉动效果因产品所处生命周期阶段、类目竞争与活动量级不同而有很大差异，不能假设每次活动都能获得同等比例的权重提升。
- 多轮活动之间的间隔期运营与广告调整策略需要结合账户实际数据校准，不存在对所有账户通用的固定节奏。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 提报前先明确本次活动要解决的具体问题——是帮助已有一定基础的产品突破流量瓶颈，还是帮助新品期产品快速打开曝光——不同目标对应不同的Listing准备重点与活动后评估标准。
2. 对拟提报的Listing做健康度检查，至少覆盖主图合规与卖点清晰、标题五点与描述的关键词完整性、A+完成度、类目节点准确性、变体结构是否正常、透明计划/侵权风险排查，任一项不达标先整改再提报。
3. 在后台提报页面核对当前显示的资格门槛（评论数量、星级、活动价格与近期最低成交价的关系、日销水位、变体子ASIN数量上限等），以提报页实时数值为准，不沿用以往活动的经验门槛。
4. 按活动量级（如短时爆发型的Lightning Deal，还是持续多日型的Best Deal/Deal of the Day）测算所需备货量并预留充分的入仓划拨提前期，避免活动开始后因断货被取消资格或影响后续排名。
5. 规划活动期间及前后的广告配合策略，把活动当作阶段性流量与权重积累的一部分，明确活动开始前、进行中、结束后各阶段的预算与竞价调整方向。
6. 活动结束后复盘转化率、排名与自然流量的变化，对照活动前的水平判断权重积累是否达到预期，未达预期时排查是提报条件、库存断档还是广告配合不足导致。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 活动目标与Listing健康度检查记录
- 提报资格实时核对表
- 备货与入仓时间表
- 活动前中后广告配合计划
- 活动复盘报告
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
