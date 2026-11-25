---
name: sealeap-qiongqi-amazon-ppc-starting-bid-and-strategy
description: "Derive a starting bid for Amazon Sponsored Products targets from target ACOS, selling price, and unit-session conversion rate, choose a bidding strategy by evidence, and adjust bids and placement modifiers across four performance scenarios. Use for 起始竞价怎么定、建议竞价能不能用、动态竞价选哪种、没曝光怎么办、有点击没转化、广告位加价. Do not use to push bulk bid changes to live campaigns without an approved change table."
---

# Amazon PPC 起始竞价与竞价策略选择

## 目标

Derive a starting bid for Amazon Sponsored Products targets from target ACOS, selling price, and unit-session conversion rate, choose a bidding strategy by evidence, and adjust bids and placement modifiers across four performance scenarios.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 起始竞价公式假设广告流量的转化率与整体流量一致，新品或促销期该假设可能不成立，需用广告报表的实际转化率复核。
- 『建议竞价与最优竞价关系松散』『无曝光可能是平台判定相关性不足或产品太新』是来源观点，属待验证假设；先排除预算耗尽、库存、Listing 可售状态等硬原因。
- 动态『提高和降低』允许平台把竞价上调到原值的一倍以上（以当前平台规则为准），费用可能超出预期；使用时设日预算上限与观察期，找到可用竞价后回切只降低。
- 来源举例的 ACOS 数值、调价幅度与广告位加成比例均为经验值，一律以当前账户盈亏平衡 ACOS 与样本量校准，不作为固定阈值。

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

1. 先取三项一方数据：本 ASIN 的目标 ACOS（用当前毛利与盈亏平衡 ACOS 校准）、买家实际支付的成交价、Business Report 里的 Unit Session Percentage；缺任一项标 NEEDS_EVIDENCE，不用控制台建议竞价或默认值顶替。
2. 用『目标 ACOS × 售价 × 转化率』算出起始竞价，再与控制台建议竞价区间对照：建议区间只反映类目竞争度，不当作最优值；起始值以自算结果为准并记录所用假设。
3. 按证据选竞价策略：默认动态『只降低』；新目标拿不到曝光且不知合理出价时短期用『提高和降低』，找到可用竞价后切回只降低；仅在确认要抢占高竞争词排名且预算可承受时用固定竞价。竞价只决定能否进入竞拍，不等于实际 CPC。
4. 上线后先看首轮结果二分：几乎无单说明竞价偏低；出单很快但日预算早早耗尽时，若 ACOS 在目标内直接加预算，否则视为竞价偏高小幅下调。
5. 积累样本后按四种情形分流：ACOS 高于目标→先判断搜索词与产品相关性（不相关否定、部分相关小幅降价、高度相关先查 Listing 与价格）；ACOS 明显低于目标→小幅加价放量；无曝光→先加价，仍无曝光则把该词拆成独立活动，排除同组大词吃掉曝光；有点击无转化→用平均转化率折算『预期出一单所需点击数』，样本已够则降价或否定。
6. 打开活动的 Placements 页按搜索顶部/搜索其余位置/商品页面对比 ACOS 与转化率，只给表现最好的位置小幅加成；需要冲排名的活动才单独抬高搜索顶部加成，并设停止线。
7. 每次调价用小步幅度（以当前账户 CPC 波动与样本量校准），记录对象、旧值、新值、样本量与观察窗口，输出待批准变更表；获批后执行并回读实际 CPC 与曝光变化，再决定下一轮。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 起始竞价计算表
- 竞价策略选择记录
- 四情形调价建议清单
- 广告位加成建议
- 待批准变更表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
