---
name: sealeap-qiongqi-amazon-sp-audience-bid-adjust
description: "Test Amazon Sponsored Products audience bid adjustments (brand purchasers, high-purchase-likelihood shoppers, cart or click non-buyers) as an evidence-gated layer on existing targeting, comparing audience-segment ACOS against the campaign baseline before scaling. Use for SP 受众竞价、受众加价怎么设、再营销受众、高购买意向受众、加购未购买受众、受众层 ACOS 对比. Do not use as a replacement for keyword or product targeting, or to scale modifiers without segment-level data."
---

# Amazon SP 受众竞价调整分层测试

## 目标

Test Amazon Sponsored Products audience bid adjustments (brand purchasers, high-purchase-likelihood shoppers, cart or click non-buyers) as an evidence-gated layer on existing targeting, comparing audience-segment ACOS against the campaign baseline before scaling.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 『受众层 ACOS 优于整体』在来源多个活动中成立，但存在与原目标人群重叠的蚕食可能，属待验证假设，需要增量检验。
- 受众口径由平台定义且可能更新（回溯周期、人群定义），以控制台当时的说明为准。
- 加成幅度与来源报告的 ACOS 数字为经验值，以当前账户盈亏平衡与样本量校准。
- 『平台偏好更大投放弹性、精确匹配预算占比不宜过高』是来源判断，不作为规律，仍以账户数据决定精确/广泛预算比例。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实与目标购买任务
- 关键词、商品投放、展示和视频的聚合表现
- 受众包定义、资格、站点限制和隐私边界
- 价格、评论、页面、库存与转化基线

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 确认账户是否已有该功能：新建 SP 活动到竞价调整区查看是否出现『为平台构建的受众提高竞价』选项；没有则记录为不可用，不臆测替代方案。
2. 理解它是叠加在现有投放（自动/关键词/商品定位）之上的竞价层而非独立定向：受众只改变对特定人群的出价，广告位仍是搜索顶部/其余位置/商品页。
3. 按目的选受众：已购买本品牌者=复购/再营销；近期购物行为显示高购买可能者=拉新首选；点击或加购未购买者=挽回；每个活动先只开一个受众便于归因。
4. 初始加成用小幅起步（来源经验为两三成量级，仅作参考），观察期后按受众层数据逐步上调，不一次拉到上限。
5. 把受众层的花费、销售额、ACOS 与活动整体对比；受众层持续优于整体才加码，持平或更差则回退到上一档或关闭。
6. 对『受众层只是把本来也会买的人提前触达』做增量检验：对比开启前后活动整体销量、ACOS 与自然销量是否同步改善，而不只看受众层 ACOS。
7. 输出受众测试记录与待批准的加成变更表。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 受众功能可用性核查
- 受众选择与假设说明
- 受众层 vs 整体对比表
- 增量检验结论
- 待批准加成变更表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
