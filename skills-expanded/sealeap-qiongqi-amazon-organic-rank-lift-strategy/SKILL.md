---
name: sealeap-qiongqi-amazon-organic-rank-lift-strategy
description: "Plan an evidence-gated push for organic rank on a target Amazon keyword by first benchmarking CTR and conversion, then layering top-of-search Sponsored Brands, dedicated Sponsored Products ranking campaigns, and external traffic sources with rank tracking and stop rules. Use for 关键词排名怎么打上去、自然排名不动、排名活动怎么设、站外流量推排名、邮件列表引流. Do not use before CTR and conversion are at or above benchmark, and never for manipulated orders or incentivized reviews."
---

# Amazon 关键词自然排名提升组合策略

## 目标

Plan an evidence-gated push for organic rank on a target Amazon keyword by first benchmarking CTR and conversion, then layering top-of-search Sponsored Brands, dedicated Sponsored Products ranking campaigns, and external traffic sources with rank tracking and stop rules.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 『搜索仍是绝大多数购买入口、AI 购物助手占比较小』是来源引用的比例，随平台演进变化，只作背景不作依据。
- 『平台偏爱站外搜索引擎流量』是来源经验，属待验证假设；站外流量只有在转化率不低于站内时才可能帮助排名，需分渠道跟踪。
- 自然排名抓取受地点、登录态、变体与个性化影响，用固定条件的多次采样取中位数。
- 任何刷单、操纵测评或以奖励换评价的做法不采用；邮件列表的激励只能用于订阅本身。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、产品事实、ASIN/SKU 与目标购买意图
- 本品和可比竞品的关键词、自然位置、广告可见度与采样时间
- 搜索词报告、转化、CPC、订单、利润和 Listing 当前覆盖
- 站点语言、变体、价格、库存与同期促销记录

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先验证前提：用 Search Query Performance 与 Product Opportunity Explorer 把目标词的点击率与转化率和类目基准对比；低于基准先修 Listing、价格与主图，不启动推排名。
2. 把排名机制写成假设：给定搜索词下，点击并购买本品的搜索者占比越高，排名越靠前；据此把所有动作都指向『该词的成交份额』而非泛流量。
3. 占据真正的搜索顶部：用 SB 商品集合或 SB 视频广告投放目标词，落地到商品详情页或含该商品的品牌店页面，让搜索该词的人直接点到并购买。
4. 配套 SP 排名活动：目标词单独建精确活动，抬高搜索顶部加成，竞价策略按抢位需要选择，并给该活动设独立预算与停止线（排名到位或 ACOS 超出承受）。
5. 叠加站外流量：自有邮件列表（合规收集，不以奖励换评价）、同人群的他人列表或联盟合作、在站外搜索引擎投放『Amazon + 自有品牌名』等品牌相关词，再到通用词经内容页/联盟内容间接导流到 Listing。
6. 每日记录目标词自然位置、广告位置、成交份额代理指标与 ACOS；排名上升后逐步降低付费强度，观察自然位置能否保持，回落则恢复上一档。
7. 输出排名推进计划、预算与停止/回退条件。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取目标关键词自然位置、搜索量趋势与竞品排名的第三方代理观测。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- CTR/转化基准对比
- 排名机制假设与观测指标
- 排名推进活动结构草案
- 站外流量渠道清单
- 排名跟踪与回退记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
