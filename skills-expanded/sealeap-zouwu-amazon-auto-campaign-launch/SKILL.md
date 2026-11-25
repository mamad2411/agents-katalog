---
name: sealeap-zouwu-amazon-auto-campaign-launch
description: "Create a Sponsored Products automatic-targeting campaign for a new listing: confirm listing readiness, choose advertised products, set bids per targeting group instead of one default bid, apply pre-emptive negatives, name campaigns and ad groups consistently, set budget and bidding strategy, then read back the created structure and first-window metrics. No claims about the auction algorithm. Use for 自动广告怎么建、新品第一个广告、四个自动定向组、紧密匹配和宽泛匹配、前置否定竞品品牌词、广告活动命名、每日预算怎么设. Do not use to change bids or budgets on live campaigns without approval, or as a substitute for search-term-based optimization once data accumulates."
---

# Amazon 自动广告创建与启动后回读

## 目标

Create a Sponsored Products automatic-targeting campaign for a new listing: confirm listing readiness, choose advertised products, set bids per targeting group instead of one default bid, apply pre-emptive negatives, name campaigns and ad groups consistently, set budget and bidding strategy, then read back the created structure and first-window metrics. No claims about the auction algorithm.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源的出价技巧（在建议区间某端加最小步长、避开整数等）与「固定竞价用一段时间再换动态」是经验做法，不是拍卖规则；以当前账户的盈亏平衡 ACOS 与实际点击成本校准。
- 每日预算按月均摊、可能单日超支的说法需以当前官方预算说明为准；归因窗口天数以当前报告口径为准。
- 自动投放各定向组的匹配范围解释来自来源举例，实际匹配以搜索词报告观察为准，不作算法断言。
- 前置否定竞品品牌词会放弃部分流量，是否值得需用后续搜索词数据验证。

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

1. 启动前核对 Listing 就绪度：类目正确、标题与五点已覆盖核心词、主图完整；自动投放依赖 Listing 语义，文案偏差会把广告投到错误品类，先修 Listing 再开广告。
2. 在广告活动管理中创建商品推广并选择自动投放；商品选择时可先纳入多个变体，后续按转化数据保留表现好的子体，并把该筛选计划写进实验记录。
3. 竞价不直接沿用统一默认值，按四个定向组（紧密匹配、宽泛匹配、同类商品、关联商品）分别设置：先记录系统给出的建议区间，再依预算与出单紧迫度为每组定一个起始值，出价规则写成可回退的账户假设。
4. 否定投放分两层：前置否定只放明确不想竞争的竞品品牌词或与本品无关的词；数据驱动的后置否定留到搜索词报告积累后再做；否定商品定位在同类商品组有数据后再考虑。
5. 命名与结构：广告活动名含产品与投放类型，广告组按变体或子系列区分；预算按能覆盖全天投放设置并了解可能出现的单日超支与月均摊；竞价策略初期选固定竞价，切换动态策略要作为单独实验；不同国家分别建活动。
6. 启动后回读：在活动列表按名称找到活动，进入广告组核对商品、投放、否定投放与设置历史；自定义列勾选曝光、点击、CTR、花费、CPC、ACOS/ROAS，并记录基线时间。
7. 至少跑满一个归因窗口再评估；评估时区分定向组表现，只把观察写成账户内证据，不推断平台算法。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- Listing 就绪度检查表
- 自动广告结构与竞价草案（含定向组）
- 前置否定词清单
- 启动后回读与基线指标记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
