---
name: sealeap-fenghuang-amazon-startup-cost-pnl-review
description: "Build a startup cost ledger and a monthly unit-economics P&L for a first Amazon FBA product (US marketplace by default), separating one-off setup spend from recurring platform fees, then run a retrospective on the costliest avoidable decisions such as freight mode and listing photography. Use for 做亚马逊要花多少钱、启动成本清单、首批货算不算赚钱、月度利润怎么算、新品半年复盘. Do not use as a tax or accounting opinion, or to project revenue for a product that has no sales data."
---

# Amazon 新品启动成本与月度 P&L 复盘

## 目标

Build a startup cost ledger and a monthly unit-economics P&L for a first Amazon FBA product (US marketplace by default), separating one-off setup spend from recurring platform fees, then run a retrospective on the costliest avoidable decisions such as freight mode and listing photography.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源的启动费用与月度金额是个案，不能当预算基准；不同类目、体积、价格带的费用结构差异极大。
- 「专业图片能多卖多少」在来源里是事后估算、无对照组；只能作为假设，需用主图对比或前后数据验证。
- 商标不是开店前置条件，但品牌备案与 A+ 依赖它；申请周期与费用以当前官方渠道为准，本 Skill 不评估可注册性。
- 「越早开始越好」是动机层面的观点，不等于跳过需求验证；不采用任何测评操纵。

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

1. 列一次性启动支出：调研工具订阅、设计与包装、主体注册、商标申请、条码申请、样品、首批生产、头程运输、验货、账户月费；每项标注「必需 / 可延后 / 可省」。
2. 按月建 P&L 表：收入、销量、产品成本、类目佣金、FBA 配送费、月费、广告花费、仓储费（含入库配置类新增费用）、退货损失；同一表内统一站点与货币口径。
3. 区分「首月不完整」与「结构性亏损」：首月样本小不下结论；从第二个月起看毛利率、广告花费占销售额比例与自然单占比的走势，以当前账户数据校准，不套用来源比例。
4. 复盘头程：比较空运、海运、快递与不同货代的报价，把「因为赶时间没比价」记为可避免损失；后续批次至少拿三家报价再决定。
5. 复盘 Listing 图片：自制图与专业图的转化差异只能间接推断；若怀疑图片拖累转化，用单变量方式更换主图并观察点击率与转化率变化。
6. 记录平台徽章、季节性节点（如节日送礼定位）对自然销量的影响，作为下一批备货量与推广节奏的输入。
7. 输出「可避免错误」清单与对应改进动作，每条写明证据来源与预计影响范围。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 启动成本清单
- 月度 P&L 表
- 费用结构走势记录
- 可避免错误清单
- 下一批次改进动作
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
