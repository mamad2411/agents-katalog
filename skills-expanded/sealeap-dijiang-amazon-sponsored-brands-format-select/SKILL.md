---
name: sealeap-dijiang-amazon-sponsored-brands-format-select
description: "Select the right Sponsored Brands ad format (product collection, store spotlight, or video) and landing destination (product versus storefront) based on brand-registry eligibility, available creative, and whether a cohesive store page exists, and treat the placement-level automated-bidding control as a distinct mechanic from Sponsored Products placement adjustments. Use for 品牌广告怎么选广告类型、落地页选商品还是店铺、店铺广告视频怎么做、品牌广告的位置出价怎么设. Do not use to launch Sponsored Brands before brand registry and a registered trademark are confirmed active."
---

# Amazon 品牌广告形式与落地页选择

## 目标

Select the right Sponsored Brands ad format (product collection, store spotlight, or video) and landing destination (product versus storefront) based on brand-registry eligibility, available creative, and whether a cohesive store page exists, and treat the placement-level automated-bidding control as a distinct mechanic from Sponsored Products placement adjustments.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 品牌广告的位置出价机制与自动出价选项以当前广告后台界面与官方帮助文档为准，来源中的描述是创作者自身理解，可能已随平台迭代变化。
- 店铺页面是否足够成体系值得作为落地页是主观判断，建议用实际转化数据而非视觉印象做最终确认。
- 不同广告类型对素材规格（比例、时长、文件大小）的要求会更新，创建前以广告后台当前提示为准。

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

1. 开始设置前先确认账号已完成品牌备案且关联商标处于有效注册状态，这是该广告类型的准入前提，未满足则先回到备案流程。
2. 按当前有的素材与推广目标选广告类型：需要直接展示多款商品做对比或组合推荐时用商品组合类型；希望强调品牌故事或引导逛店铺时优先用视频或店铺聚焦类型；不确定就先用商品组合做最小可行测试。
3. 落地页在跳转到具体商品与跳转到店铺首页或子页之间选择时，只有店铺页面本身已经做成主题清晰、货架结构合理的成品页面才选店铺落地，否则宁可先跳转到商品页，避免用一个粗糙的店铺页面拉低广告转化。
4. 若制作视频素材，同时准备横版与竖版两种比例分别用于对应位置，不要只做一种比例硬套所有位置。
5. 该广告类型下的位置自动出价开关是把预算在搜索结果顶部与其余位置之间做倾斜，其调整方向与商品推广广告的位置加价机制并不相同，首次使用时先小幅度测试并观察花费与转化变化，再决定加大倾斜幅度。
6. 上线后按广告类型与落地页分别查看花费与转化数据，表现明显落后的广告类型或落地页先暂停或替换素材，不要用同一套素材长期跑所有位置。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 广告类型与落地页选择决策记录
- 横版/竖版视频素材清单
- 位置出价倾斜测试记录与分位置转化数据
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
