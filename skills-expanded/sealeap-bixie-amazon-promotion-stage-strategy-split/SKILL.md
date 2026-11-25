---
name: sealeap-bixie-amazon-promotion-stage-strategy-split
description: "Segment big-event promotion planning by product lifecycle stage (mature, new, clearance) and derive a matching pricing, budget, and offer-stacking approach for each stage. Prevents applying one blanket promotion tactic across products that have different margin and traffic goals. Use for 大促前定产品目标、成熟品新品清货品促销策略差异、大促预算与折扣方式选择. Do not use to adjust live bids in isolation, or to set a clearance price before confirming the loss ceiling."
---

# Amazon 大促产品阶段策略分配

## 目标

Segment big-event promotion planning by product lifecycle stage (mature, new, clearance) and derive a matching pricing, budget, and offer-stacking approach for each stage. Prevents applying one blanket promotion tactic across products that have different margin and traffic goals.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 各阶段的具体毛利提升目标、预算增幅比例与折扣力度均为经验区间，不同类目、不同账户的基准差异很大，必须用自身历史大促数据重新校准，不可直接套用来源给出的数字。
- 广告位中部区间 ACOS 更优的判断依赖当时的竞价环境，竞价格局变化后结论可能反转，需要按当前实时数据复核而非依赖历史经验。
- 清货定价跌破成本涉及现金流和账面亏损双重风险，执行前需与财务口径确认可承受上限，防止连续多批次清货侵蚀整体利润。
- 满减、捆绑等价格工具是否可叠加、如何显示，以平台当前规则与后台预览为准，不得凭经验假设可以叠加。

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

1. 先核实待促销产品当前所处阶段：自然流量与排名是否稳定、是否新上架不久、是否长期滞销，避免用同一套目标套所有产品。
2. 对稳定成熟品，先测算真实毛利结构和上一周期实际毛利率，再设定本次促销的毛利提升目标而非销量目标，并据此反推广告预算上限。
3. 对新品，改用目标词广告转化率、自然流量占比变化、CPC 是否失控这三项过程指标定义成功，而不是只看订单量。
4. 对长期滞销库存，先核算清货底价（采购成本加头程等硬成本）和可承受的最大账面亏损，确认不突破再定折扣力度。
5. 分别为三类产品设计价格工具（满减、会员折扣、清仓直降）与广告结构（核心词卡位、测款分散、低价长尾引流）的组合，避免直接套用统一的降价或加预算动作。
6. 大促结束后按产品分类分别复盘目标达成情况，把结果计入下一次分类阈值的校准依据。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 产品阶段分类表
- 分阶段促销目标与预算方案
- 价格与活动组合清单
- 促销复盘记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
