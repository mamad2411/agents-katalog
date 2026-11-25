---
name: sealeap-qiongqi-amazon-campaign-profit-optimization
description: "Run a recurring, profit-oriented optimization pass over Amazon auto, keyword, product-targeting, ranking, Sponsored Brands video, and Sponsored Display campaigns using placement modifiers, negations, revenue-per-click bid calibration, and creative or variation pruning. Use for 广告活动怎么优化、自动广告优化、ACOS 太低要不要加价、广告位加成怎么调、视频广告素材淘汰、变体广告关停. Do not use for initial campaign structure design or for unapproved bulk edits."
---

# Amazon 广告活动分类型利润优化例行

## 目标

Run a recurring, profit-oriented optimization pass over Amazon auto, keyword, product-targeting, ranking, Sponsored Brands video, and Sponsored Display campaigns using placement modifiers, negations, revenue-per-click bid calibration, and creative or variation pruning.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 『自动活动如今也能成为利润主力』是来源在其账户内的观测，不同类目差异大，需用本账户自动活动的 ACOS 与销量占比验证。
- 广告位加成幅度、观察窗天数与创意条数均为来源经验值；以当前账户样本量与盈亏平衡 ACOS 校准。『一次性大幅加成无效』属待验证假设。
- 按 CTR 关停变体会减少该变体的广告曝光，可能影响其自然表现与库存周转，关停前确认变体销量来源。
- 收入/点击反推竞价假设未来转化率与历史一致，新品、季节波动与促销期需缩短观察窗重新校准。

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

1. 先定观察窗：样本足够时用近一个月量级的数据，样本不足则拉长；同时用更长窗口（如年初至今）核对各广告位 ACOS 是否稳定一致，波动大则先不动。
2. 自动活动按序做四件事：用搜索词报表否定不相关词与不相关 ASIN；在 Bid Adjustments 按广告位（搜索顶部/搜索其余/商品页）对比 ACOS，只给最优广告位小幅加成、次优更小幅；按收入/点击反推竞价；在广告组 Ads 页按 CTR 关停明显拖后的变体，保留高 CTR 变体去争取点击。自动活动的紧密/宽泛/同类/关联四种匹配若表现差异大，拆成独立活动单独控竞价。
3. 理想竞价 = 该对象（活动/广告组/投放目标）的销售额 ÷ 点击数 × 目标 ACOS，即『每次点击带来的收入 × 愿意付出的比例』；ACOS 远低于目标视为竞价偏低、错失销量，同样按公式上调，而不是只处理高 ACOS。
4. 关键词与商品定位活动：在广告组 Targeting 页逐个投放目标按公式校准竞价，匹配类型分活动管理以保留控制权；排名类活动的评判以目标词排名与成交变化为主，ACOS 只作预算停止线。
5. SB 视频与 SD：广告位加成选项少（仅『搜索顶部以外』与受众加成），优化重心在投放目标竞价与创意；同一活动装入数条创意做拆分测试，按 ACOS 与点击率关停落后创意，并持续用新创意挑战当前胜者。
6. 每轮改动记录对象、旧值、新值与预期，下一轮先回读是否达到预期，未达预期回退到上一值；高复购的消耗型产品用长期 ACOS 而非单次 ACOS 评判。
7. 输出待批准变更表与本轮优化日志；线上写入需用户明确授权。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 活动类型优化清单
- 广告位加成建议
- 理想竞价计算表
- 创意与变体淘汰名单
- 待批准变更表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
