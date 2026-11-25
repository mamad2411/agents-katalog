---
name: sealeap-bifang-amazon-new-product-ad-conversion-first
description: "Plan and review the launch-phase advertising of a small seller's new Amazon product by starting from a short list of exact-match long-tail terms, treating automatic campaigns only as low-bid discovery, judging each term by click-through and conversion rate rather than ACOS or TACOS, and layering coupons, deals and old-to-new bundles once the product and listing pass a readiness check. Use for 新品广告怎么开、新品转化率低、新品 ACOS 高正常吗、自动广告还是手动广告、新品否词、老品带新品. Do not use to launch or change live campaigns without an approved change table, or to compensate for a product or listing that has not passed readiness review."
---

# Amazon 新品期广告转化优先策略

## 目标

Plan and review the launch-phase advertising of a small seller's new Amazon product by starting from a short list of exact-match long-tail terms, treating automatic campaigns only as low-bid discovery, judging each term by click-through and conversion rate rather than ACOS or TACOS, and layering coupons, deals and old-to-new bundles once the product and listing pass a readiness check.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “少词精准起步、自动广告只做捡漏”是来源对中小卖家的经验策略；不同类目与预算下自动广告的价值不同，以当前账户报告校准。
- 来源解释“多次点击不出单会拉低广告组权重”“词权重上升后建议竞价自然下降”，均为平台算法推断，作为待验证假设，只用账户内前后对比观测。
- “站外折扣比站内 PPC 更划算并对新品链接有额外好处”是来源观点；用同口径成本与归因数据验证，不预设。
- 任何借站外链接直接拉动关键词权重、或以促销换取评论的做法不采用；促销仅用于获取真实销售。

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

1. 准入检查：核对产品事实、主图、标题、五点、价格与同购买意图竞品的差距；任何一项明显落后先修正再投放，广告不用于弥补产品或页面缺陷。
2. 起步结构：从关键词清单中挑少数与产品高度相关、有转化记录的长尾词，只用手动精准匹配起步；同时上架多个新品时明确主推与非主推链接，预算向主推倾斜；每个词的起始竞价与预算写入变更表。
3. 自动广告定位：以低于手动的竞价开启自动广告只做捡漏与拓词；自动广告出现有转化的搜索词后，把它移入手动精准并在自动里加否定；自动广告不承担主要预算。
4. 判定指标：新品期自然流量少，ACOS 与 TACOS 接近属预期，不以两者作为停止依据；逐词看点击率与转化率——点击率差指向主图/标题/价格在搜索结果页的吸引力，转化率差指向价格、评论、页面详情或产品本身；每个词累计足够点击后再判定，样本不足标 NEEDS_EVIDENCE。
5. 否词节奏：新品期否词要慎重，只否定多次点击且与产品事实明显不符的词；对相关但暂未转化的词先降竞价观察，累计点击充足仍无转化且页面无可改点时暂停该词而不是直接否定。
6. 补流量：在利润允许范围内叠加优惠券、会员专享折扣或站外促销，把折扣成本与 PPC 成本放在同一口径下比较；预算紧张时可先不开广泛/词组匹配，把预算留给精准投放与促销。
7. 老带新与扩词：有在售老品时设计组合促销（买老品享新品折扣等）并记录归因；扩词条件是现有词的排名与转化稳定后再逐步增加，每次只加少量词并保留回退。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充同购买意图竞品的关键词、价格与评论代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 新品准入检查表
- 起步广告结构与变更表（词、匹配、竞价、预算、主推/非主推）
- 逐词点击率/转化率判定记录与否词理由
- 促销与老带新组合方案（含成本口径）
- 扩词条件与回退记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
