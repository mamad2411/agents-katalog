---
name: sealeap-bifang-amazon-converting-term-discovery
description: "Discover and tier keywords for an Amazon product by combining long-tail expansion, search-suggestion checks, related-term tools and Brand Analytics based converting-term lookups on comparable ASINs, then separate static identity keywords from time-varying traffic terms, group them into manual campaigns and re-check them on a fixed reporting cadence. Use for 出单词怎么找、流量词和关键词的区别、下拉框找词、相关词工具、点击份额转化份额怎么看、关键词分组投放. Do not use to create or edit live campaigns without approval, or to treat third-party share estimates as Amazon first-party data."
---

# Amazon 出单词反查与关键词分层

## 目标

Discover and tier keywords for an Amazon product by combining long-tail expansion, search-suggestion checks, related-term tools and Brand Analytics based converting-term lookups on comparable ASINs, then separate static identity keywords from time-varying traffic terms, group them into manual campaigns and re-check them on a fixed reporting cadence.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的观察周期（数周级初评、更长周期确认）是经验值，以当前广告归因窗与点击样本量校准。
- “点击份额/转化份额过高即红海应避开”是来源对中小卖家的建议；资金与目标不同的卖家结论不同，需结合自身约束判断。
- 第三方反查的份额、排名与搜索量均为估算或对官方数据的再加工，标为 ESTIMATE；官方 Brand Analytics 数据本身有周度口径与站点限制。
- “出单词随时间变化”需用自身账户的搜索词报告验证，不外推为平台规律。

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

1. 固定产品事实与目标购买意图，先写出主词（产品名称级别的词）；主词不确定时用搜索结果页与可比 ASIN 的标题核对，不凭感觉。
2. 四路来源拉词：①以主词做长尾拓展；②在站点搜索框及细分类目下查看下拉推荐词并记录出现频次；③用相关词/同义词工具把功能诉求换一种说法（用途词、场景词）；④对若干可比 ASIN 做出单词反查（基于 Brand Analytics 的周度数据），只保留有点击与转化记录的词。
3. 读份额指标判断竞争：对每个出单词看点击份额、转化份额与前几名 ASIN 的合计占比；占比过高的词意味着被少数 ASIN 垄断，小卖家优先选择份额分散的词，垄断判定的具体比例按当前类目分布校准。
4. 清洗与分层：去掉无意义停用词与他人品牌词，按与产品事实的匹配度打分，再按搜索量层级分成主词、精准长尾、补充词；把“标识产品的静态词”（用于收录与索引）和“带来订单的流量词”（会随时间变化）分别标注。
5. 投放结构：按层级建手动广告组，前期用固定且不激进的竞价；累计足够点击后用广告报告看各词点击与转化，表现差的降价或否定，表现好的独立成组提高精准竞价以稳定位置。
6. 周期校正：设定固定的报告下载与复盘周期，跟踪流量词是否变化、是否出现新出单词并回填清单；每次调整写入变更记录，只在账户内证据支持时改变分层。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取可比 ASIN 的出单词、点击/转化份额与相关词代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 四路来源合并的候选词表（含来源与频次）
- 出单词份额与垄断度读表
- 分层关键词清单（静态索引词/流量词标注）
- 手动广告组结构草案与起始竞价表
- 周期复盘与变更记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
