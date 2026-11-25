---
name: sealeap-taotie-amazon-keyword-driven-niche-product-screening
description: "Screen product candidates starting from a seed keyword: read search-trend shape, competitor launch age and growth speed, review count and rating, then segment by attribute, audience and use case using variation and high-frequency-word signals, check historical price ranges and listing-count supply ratios, and log each candidate into a comparable selection table. Use for 新手怎么选品、关键词选品、细分市场怎么找、看趋势图怎么判断、上架时间和增长速度、供需比怎么用、历史价格怎么看、选品表怎么设计. Do not use to output a GO decision without the unit-economics check or compliance and IP screening."
---

# Amazon 关键词驱动的细分市场选品筛选

## 目标

Screen product candidates starting from a seed keyword: read search-trend shape, competitor launch age and growth speed, review count and rating, then segment by attribute, audience and use case using variation and high-frequency-word signals, check historical price ranges and listing-count supply ratios, and log each candidate into a comparable selection table.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「半年内上架并快速增长的品新手都有机会」「越早发现成功率越高」是来源经验判断，需用本类目近一年新品的存活与增长数据校准。
- 商品数/供需比、增长率、评论数等数字都是第三方估算，标为 ESTIMATE；不同工具口径差异大，不得写成事实，也不得设固定阈值。
- 来源举例的具体品类、价格与销量不转译；工具推广与分销邀约等内容不采纳。
- 变体异常高价可能是断货或临时策略，「高价空缺 = 机会」只是待验证假设，需看同行与历史价格。

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

1. 确定一个种子关键词（可来自自己能深耕的类目或商标类别），在关键词/选品工具类别中过滤搜索结果；新手先不叠加复杂筛选条件，先看结果列表的整体形态。
2. 看搜索趋势形状：优先「前段平、近期明显抬升且持续」的词，标注抬升起点；对型号词或节日词识别其生命周期（新型号上市替代旧型号、季节回落），并写下需求增长的背后原因（新用户群扩大、新功能、社媒使用场景等）作为待验证假设。
3. 看竞品的上架时间与增长速度：找上架不久却已进入类目前列、评论数尚少的 Listing，作为「新品能进入」的证据；越早发现这类信号越有利，因此要按固定周期重复抓取。
4. 做细分：从变体（颜色/尺寸/型号适配）与高频词（迷你、带支架、材质等）拆出属性、人群、用途三个维度，找出有搜索需求但现有热销品没覆盖的组合；变体中长期异常高价的款式可能是空缺信号，需与同行对比确认。
5. 读供需与价格：搜索结果商品数只作竞争难度的粗指标，重点看头部十几个 Listing 的价格带、评论、上架时长；售价用价格历史工具看区间而非当下促销价，市场均价按头部主流价格带取值，不必对所有竞品做精确平均。
6. 把每个候选写入选品表：核心词、场景词、长尾词、趋势判断、竞品链接与截图、优缺点（来自评论）、采购成本、目标售价；同一需求下列出不同价位的产品解决方案，对比后再进入单位经济测算。
7. 评分低但需求增长的品不直接跟做，沿其需求方向寻找评分更好或价位更高的替代方案；候选表达到三个以上再做下一步测算与打样。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取关键词搜索趋势、高频词、竞品上架时间与销量估算、历史价格区间的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 种子关键词与趋势判读记录
- 竞品上架时间与增长对照表
- 属性/人群/用途细分矩阵
- 价格带与供需观察表
- 候选选品表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
