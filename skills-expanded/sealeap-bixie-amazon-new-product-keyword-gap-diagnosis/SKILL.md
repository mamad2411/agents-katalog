---
name: sealeap-bixie-amazon-new-product-keyword-gap-diagnosis
description: "Diagnose why a new listing's traffic isn't growing by comparing organic-to-ad traffic ratios, then close keyword gaps against verified competitor terms in priority tiers. Flags indexing problems separately from weak keyword coverage before any bulk keyword addition. Use for 新品流量起不来、自然流量占比低、判断关键词是否被收录、新品补词优先级排序. Do not use to bulk-add keywords without first checking indexing status, or to replace a direct backend index/rank lookup."
---

# Amazon 新品关键词收录诊断补词

## 目标

Diagnose why a new listing's traffic isn't growing by comparing organic-to-ad traffic ratios, then close keyword gaps against verified competitor terms in priority tiers. Flags indexing problems separately from weak keyword coverage before any bulk keyword addition.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 竞品有而我方没有只是补词的必要条件，不是充分条件——搜索量、相关性与自身供给能力都需要以当前数据复核，不能照单全收竞品词表。
- 自然流量占比、收录状态在不同关键词工具里的口径可能有差异，需用同一数据源做前后对比，不跨源直接比较。
- 补词梯队顺序是一种经验排序，新品期先测哪一档应按当前账户的广告预算与承受能力调整，不是固定公式。

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

1. 导出该 ASIN 最近一段时间的自然单占比与广告单占比，判断是广告占比畸高，还是两者都偏低这两种情形。
2. 若广告占比畸高，优先复查标题、五点、后台关键词字段的收录状态，而非急于加词。
3. 选两三个上线时间相近且表现更好的竞品，导出其关键词榜单做差异对比，列出竞品有、我方未覆盖的词表。
4. 对差异词表逐词核实搜索量量级与本 ASIN 当前的收录、排名状态，只有搜索量达标但未被收录的词才判定为补词机会。
5. 按精准中高搜索量词、长尾词、宽泛大词的顺序分梯队排入补词计划，避免一次性堆词。
6. 补词后按固定周期复查收录与排名变化，用结果反过来验证词表判断是否准确。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取竞品 ASIN 的关键词覆盖与搜索量作为补词优先级排序的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 自然广告流量占比诊断表
- 竞品关键词差异对比表
- 分梯队补词清单
- 补词后收录复查记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
