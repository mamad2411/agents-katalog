---
name: sealeap-chongming-amazon-fba-startup-capital-template
description: "Build a first-product FBA startup capital budget by separating upfront cash outlays (seller plan, research tooling, first inventory batch, product identifiers, inbound freight, pre-shipment inspection, launch ad budget, optional trademark) from fees deducted at the point of sale, recomputing every line from current rate cards and the seller's own quotes. Produces a low/high range with the assumption behind each line and a sensitivity check instead of a universal figure. Use for 做 FBA 要多少钱、启动资金测算、首批货预算怎么算、第一个产品要投多少、哪些费用先掏钱哪些从销售额扣、资金够不够起步. Do not use to quote a universal startup figure, or to replace the seller's own supplier, freight and inspection quotes."
---

# Amazon FBA 首单启动资金测算模板

## 目标

Build a first-product FBA startup capital budget by separating upfront cash outlays (seller plan, research tooling, first inventory batch, product identifiers, inbound freight, pre-shipment inspection, launch ad budget, optional trademark) from fees deducted at the point of sale, recomputing every line from current rate cards and the seller's own quotes. Produces a low/high range with the assumption behind each line and a sensitivity check instead of a universal figure.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的月费、工具订阅价、每公斤运费、验货费、日预算和总额区间均为特定时点的经验值，本 Skill 不保留任何金额；一律按当前费率卡、工具官网价与货代/验货商报价重算。
- 来源建议新手只做单一主站点、把采购单价压在低区间并先订几百件，这是风险偏好而非规律；批量应由需求预估和断货成本推导，站点选择要看产品合规与竞争。
- 来源认为商标可以等销售稳定后再注册；实际上品牌备案关联多项功能与保护，是否推迟属于取舍，需与产品生命周期和侵权风险一起评估。
- 来源把学习培训类支出排除在测算之外；本 Skill 同样不评估此类支出，也不把任何付费培训作为起步前置条件。

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

1. 先固定测算对象：目标站点、首个产品的采购单价区间、计划首批数量、包装后的单件重量与尺寸、是否需要第三方验货；缺任一项标 NEEDS_EVIDENCE，不用行业均值代填。
2. 把支出分成两栏：上架前必须现金支付的（专业卖家月费、选品/关键词工具订阅、首批货款、每个产品一枚 GTIN/UPC、头程运费、首批验货费、上线期广告预算、可选的商标注册），以及出单后从销售额扣除的（平台佣金、FBA 配送费、月度仓储费）；后一栏不计入启动现金，只进入单位经济测算。
3. 首批货款 = 采购单价 × 首批数量；首批数量按“一个推广周期内不断货”倒推（预估日销 × 补货周期 + 安全库存），来源的固定件数区间只作参考；同时给出低配（低单价、小批量）与高配（高单价、足量）两个方案。
4. 头程按货代对当前重量/体积/运输方式的实际报价填写，不用“按货值百分比”粗算；产品带电、含液体或超尺寸时单独询价并确认可运可入仓。
5. 验货费只在首批或更换供应商时计入；广告预算按计划日预算 × 上线观察天数估算；商标/品牌备案费用列为可选项，并写明推迟注册会失去品牌备案相关功能（A+、品牌保护等）的机会成本，由卖家决定先后。
6. 汇总低/高两档总额，标出占比最大的三项与每项对应的假设（单价、件数、重量、日预算），再做敏感性检查：单价或件数按一定幅度（如 ±20%）变化时总额变化多少。
7. 把测算与单位经济（售价、佣金、配送费、预计退货率）联动核对：若首批货款按目标毛利率无法在计划周期内回收，先调整产品或批量，而不是放大预算。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 启动资金分项表（上架前现金 vs 出单后扣除）
- 首批数量与货款推导（低配/高配两档）
- 头程与验货报价记录（按当前实际报价）
- 低/高两档总额与三大占比项的假设清单
- 敏感性检查与回收周期核对结论
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
