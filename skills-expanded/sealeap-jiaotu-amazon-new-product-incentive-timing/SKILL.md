---
name: sealeap-jiaotu-amazon-new-product-incentive-timing
description: "Check the current new-listing incentive program's eligibility window, covered fee categories, and effective dates directly in Seller Central before relying on them, then sequence product launches, inbound shipments, and early ad spend to fall inside the verified relief window. Assumes incentive terms and caps are read fresh each cycle rather than carried over from a past program. Use for 新品扶持政策核对、上新节奏规划、测款成本压缩、入仓时间安排、新品广告金申领资格确认. Do not use to assume a past cycle's discount rates, caps, or eligible categories still apply without checking current Seller Central terms."
---

# Amazon 新品扶持窗口期上新节奏规划

## 目标

Check the current new-listing incentive program's eligibility window, covered fee categories, and effective dates directly in Seller Central before relying on them, then sequence product launches, inbound shipments, and early ad spend to fall inside the verified relief window. Assumes incentive terms and caps are read fresh each cycle rather than carried over from a past program.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源列出的具体折扣比例、返还金额上限与免仓储天数是特定周期的活动条件，会随政策版本调整或到期，一律以当前后台与官方公告为准，不作为长期费率假设。
- "对新父ASIN认定更严格、对铺货/跟卖不友好"是来源的解读，实际资格判定逻辑未公开，只能在提报或申请后以系统实际反馈为准，不能反向猜测规则细节。
- 淡季/窗口期与上新节奏的最优搭配因品类、供应链周期而异，来源给出的季节性建议是启发而非结论，需按自身品类的供应与竞争节奏校准。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 打开卖家后台官方公告与资格页面，核对当前新品激励计划是否存在、覆盖哪些站点/类目、生效与到期日期，以及父ASIN创建时间等资格判定口径；口径以后台展示为准，不沿用旧周期的印象。
2. 逐项确认本次可叠加的减免类型（佣金、入库运费、仓储费、配送费、广告金返还等）及其各自的时间窗口长度和上限，记录在同一张表里以避免窗口错位导致优惠部分落空。
3. 按验证到的免仓储/低佣金窗口长度倒推上新与入仓节点：优先让最先消耗窗口期的动作（如入仓、开广告）集中在窗口开始后尽快发生，避免窗口期内出现空转。
4. 若计划里包含广告金或费用返还类激励，核对其发放条件（是否自动发放、是否需要达到花费门槛、返还是否有单产品上限），并在广告排期里预留验证发放到账的检查点。
5. 对候选新品做优先级排序：优先安排有稳定供应、能在窗口期内维持真实动销的产品，避免为蹭补贴而上架跟卖或无差异化产品导致后续不符资格判定。
6. 设定窗口到期前的复核动作：提前核对费用是否恢复标准费率、库存是否需要在到期前完成周转，避免窗口结束后仓储/佣金成本忽然上升打乱盈亏预期。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 新品激励资格与窗口核对记录
- 多项减免叠加与到期时间线表
- 上新/入仓/开广告节点排期草案
- 窗口到期前复核清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
