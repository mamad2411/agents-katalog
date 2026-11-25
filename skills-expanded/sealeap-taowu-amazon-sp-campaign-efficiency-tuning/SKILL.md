---
name: sealeap-taowu-amazon-sp-campaign-efficiency-tuning
description: "Review a Sponsored Products account top-down—time trend of spend versus ACOS, keyword versus product targeting efficiency, then per-target spend, orders and ROAS—to propose pauses, match-type tightening and bid reductions as staged experiments with rollback. Every threshold is calibrated to the account's own break-even ACOS and sample size. Use for SP 广告优化、ACOS 太高怎么降、哪些投放对象该暂停、商品投放和关键词投放哪个好、按 ACOS 比例降 bid、周末要不要停广告. Do not use to change bids, pause targets or alter budgets on live campaigns without explicit approval, and do not use for Sponsored Brands or DSP structure."
---

# Amazon SP 广告分层效率优化

## 目标

Review a Sponsored Products account top-down—time trend of spend versus ACOS, keyword versus product targeting efficiency, then per-target spend, orders and ROAS—to propose pauses, match-type tightening and bid reductions as staged experiments with rollback. Every threshold is calibrated to the account's own break-even ACOS and sample size.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “周末效率差”“工作日中段出单多”是来源账户的观察，属待验证假设；按当前账户多周数据校准，不作为通用规律。
- “商品投放比关键词投放高效数倍”来自个位数订单的小样本，不构成结论；投放类型优劣按当前账户同期同口径数据判断。
- 来源的固定阈值（某花费无单即停、ROAS 低于某值即删、目标 ACOS 区间）均需以当前账户的盈亏平衡 ACOS 与目标利润校准，来源经验值仅作参考。
- bid 除以 ACOS 比例的系数法假设 CPC 与 ACOS 线性同比缩放，竞价市场并不保证这一点；只作为降 bid 的起点，必须设置曝光与订单的停止线并回读。

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

1. 统一口径后拉取活动层的日级花费与 ACOS 曲线（同站点、同时间窗、同归因窗），标出异常日和按星期几的规律；异常日先排查库存、价格、Buy Box、竞价改动和大促，再考虑是否为需求周期。
2. 若按星期几的效率差异在多周重复出现且样本足够，把分时段/分日降预算或暂停做成单变量实验：写清基线、观察窗、成功与回退条件，而不是凭一两天数据停投。
3. 进入广告组层，对比关键词投放与商品投放（竞品详情页位）的花费、订单、ROAS 和订单量：效率高但量小的投放类型不能替代放量投放，新品期与成熟期的预算分配按账户证据决定。
4. 进入投放对象层做剪枝：先看有花费无订单的对象，花费超过按目标 CPA 或单件贡献利润换算出的上限即暂停；再看有订单的对象，ROAS 低于账户盈亏线的暂停，处于盈亏线与目标之间的先查竞价与广告位再决定，高于目标的优先保证预算。
5. 检查匹配类型：只投 Exact 是控制流量精准度的一种做法；用搜索词报告验证 Broad/Phrase 带来的搜索词是否偏离购买意图，偏离的加否定或收紧，仍在出单的保留作为词发现渠道。
6. 需要整体降 ACOS 时，可把“当前 ACOS ÷ 目标 ACOS”作为缩减系数，把现有 bid 或平台建议 bid 除以该系数得到新 bid 草案；按投放对象逐条列出旧值、新值，并预告曝光会下降。
7. 改动后用曝光、点击、CPC、订单和 ACOS 做回读：曝光跌到无法出单或订单量下滑超出承受线时回退；只在指标稳定后再进行下一轮剪枝，避免连续多变量改动。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 活动层时间趋势异常清单（异常日、星期规律、已排除的干扰因素）
- 投放类型效率对比表（关键词投放 vs 商品投放）
- 投放对象剪枝与调价草案（对象、旧值、新值、依据、审批状态）
- 匹配类型与否定词建议
- 回读指标与回退条件
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
