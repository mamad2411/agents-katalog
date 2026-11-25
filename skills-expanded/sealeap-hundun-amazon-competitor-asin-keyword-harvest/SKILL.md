---
name: sealeap-hundun-amazon-competitor-asin-keyword-harvest
description: "Build a seed keyword list by reverse-looking-up search terms from a curated set of visually or functionally similar competitor ASINs in the same sub-category, then manually vet each returned term by checking whether the actual top-ranked results for that term resemble the target product, judging ambiguous cross-shopping terms case by case. Relies on third-party reverse-ASIN keyword data as a proxy signal, not an Amazon first-party source. Use for 怎么找关键词、竞品反查关键词、关键词相关性怎么判断、变体多的产品关键词太少怎么办. Do not use the raw exported list without the manual relevance pass, and do not treat search-volume figures from third-party tools as exact platform data."
---

# Amazon 竞品ASIN反查关键词甄别

## 目标

Build a seed keyword list by reverse-looking-up search terms from a curated set of visually or functionally similar competitor ASINs in the same sub-category, then manually vet each returned term by checking whether the actual top-ranked results for that term resemble the target product, judging ambiguous cross-shopping terms case by case. Relies on third-party reverse-ASIN keyword data as a proxy signal, not an Amazon first-party source.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 反查出的关键词数量、搜索量等均为第三方代理数据，与平台一方数据可能存在口径差异，只作为方向参考。
- 相关性判断以“该词当前排名靠前的结果是否与自身产品相似”为准，同一关键词的排名结果会随时间、地区、个性化等变化，此判断存在时效性，需要定期复核。
- 保留跨购买意图的边缘关键词是一种权衡（可能带来不够精准的点击），需结合自身预算和转化数据决定取舍尺度，不是非黑即白的规则。

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

1. 从目标细分类目的榜单中，人工挑出与自己产品在外观/功能上高度相似的一批竞品 ASIN，控制在可管理的数量内，明显不像的直接不选。
2. 用第三方反查关键词工具，把这批 ASIN 批量粘贴进行反查，并开启按变体扩展的选项以覆盖同一 listing 不同颜色/尺寸变体下的搜索词，服装等多变体品类尤其需要。
3. 逐条核对返回的关键词：搜索该词看实际排名靠前的结果是否与自己的产品相似；相似则保留为相关词，明显是其他品类/用途的产品则标记删除。
4. 对介于两可之间的词（搜索的产品类型不完全一样，但可能存在跨购买意图），按是否可能带来有效转化自行判断去留，不必强求完全同款才保留。
5. 在导出之前先完成删除与清理，而不是导出后再回头清洗，减少后续整理的工作量。
6. 导出清理后的关键词表，用于后续 listing 文案（标题、五点、后台关键词）的词汇覆盖。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：通过第三方反查工具获取竞品ASIN关联的搜索词、搜索量与相关度等代理数据，用于扩充候选关键词库。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 高相似度竞品ASIN候选清单
- 反查关键词原始导出表
- 人工相关性甄别后的干净关键词表
- 待复核的边缘关键词清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
