---
name: sealeap-hundun-amazon-trend-scout-sourcing-validation
description: "Mine overseas social content and comment sections for small, trend-driven, non-seasonal product leads, validate the opportunity by checking seller count, market-wide listing freshness and traffic concentration before committing, then negotiate landed cost in person at the sourcing hub rather than relying solely on online quotes. Use for 从社媒内容找选品灵感、怎么判断一个趋势品还能不能进、新品友好度怎么看、去产地面谈能不能压价、小件高利润品怎么选. Do not use to justify entering a trend already dominated by large sellers with long-tenured listings, or to adopt fake-order promotion as part of the launch plan."
---

# Amazon 社媒趋势选品与货源验证

## 目标

Mine overseas social content and comment sections for small, trend-driven, non-seasonal product leads, validate the opportunity by checking seller count, market-wide listing freshness and traffic concentration before committing, then negotiate landed cost in person at the sourcing hub rather than relying solely on online quotes.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源分享的具体采购单价、利润区间与投资回报比为特定案例的历史数据，不同产品与时期差异很大，不作为通用参考值，需按当前采购与费用重新测算。
- 来源把找人刷单列为推广手段之一，这属于刷单/虚假交易，不采用；产品起量应通过合规广告与自然搜索验证，不使用虚假订单拉动排名。
- 社媒带火的趋势品生命周期不确定，来源给出的具体周期为个案观察；应把生命周期视为待验证假设，用自身上架后的销量与搜索趋势数据持续复核，并提前设定清库存/降价撤退的触发条件。
- 线下面谈压价的效果因供应商与地区而异，属经验判断；仍需通过样品验货与小批量试单验证质量稳定性，不能仅凭一次面谈报价就放大采购规模。

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

1. 从目标市场的头部社媒内容（穿搭、家居、生活方式类）评论区反向挖掘选品线索：找评论中反复出现“这是什么/哪里买”的高互动内容，记录对应的产品类型与关键词，作为需求真实存在的初筛信号。
2. 用三项指标判断市场是否还能进入：同类关键词下卖家数量与整体流量规模是否过大、市场里新上架链接的占比与近期上新速度、是否已有明显的大卖家垄断该词；三项都通过才进入下一步。
3. 到境内批发市场/产地现场比价而非只依赖线上报价：线上询价通常拿到的是统一对外报价，当面沟通更容易拿到分级报价与真实的材质/工艺差异说明；长期做同一品类时，建立线下供应商关系比持续线上比价效率更高。
4. 核算最小可行启动规模：按当前汇率与目标站点费用结构测算采购成本、头程运费、平台佣金后的单件预估毛利与所需启动资金，判断是否在个人卖家可承受的资金和体积重范围内。
5. 用自然流量占比作为推广难度的先行指标：若同类目对照产品明显以自然搜索获取多数订单、广告依赖度低，说明产品本身需求匹配度高；若同类对照产品高度依赖广告仍出单有限，需重新评估选品而不是加大广告预算。
6. 明确该类趋势品的生命周期假设：由社媒内容带热的产品通常有时效性，一旦相关内容热度下降，搜索量可能同步下滑；上线前就设定好预期运营周期与库存节奏，避免按长青款的备货逻辑囤货。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取目标关键词的卖家数量、上新时间分布与自然流量占比等公开代理数据，用于新品友好度与竞争密度核查。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 社媒趋势选品线索清单（来源评论区高频诉求）
- 新品友好度与竞争密度核查记录（卖家数/新品占比/垄断情况）
- 产地现场比价与供应商分级报价记录
- 启动资金与单件毛利测算表
- 产品生命周期假设与库存节奏计划
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
