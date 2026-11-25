---
name: sealeap-dijiang-amazon-reverse-asin-keyword-mining
description: "Mine keywords by reverse-searching top competitor ASINs through a third-party keyword tool, rank the results by search volume, then triage them into relevance tiers plus a misspelling variant list to build a listing-ready keyword set. Use for 关键词怎么找、反查竞品asin关键词、关键词分级怎么做、backend关键词要不要收录错别词. Do not use to add irrelevant high-volume keywords purely for traffic without matching purchase intent."
---

# Amazon 反查竞品关键词建库

## 目标

Mine keywords by reverse-searching top competitor ASINs through a third-party keyword tool, rank the results by search volume, then triage them into relevance tiers plus a misspelling variant list to build a listing-ready keyword set.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 反查工具给出的“竞品表现排序”“搜索量”均为第三方估算，不是 Amazon 官方一方数据，不同工具口径可能不同，须标注数据来源与采集时间，不与官方后台数据混用推导结论。
- 中相关词库中可能包含“同商品但不同使用目的”（如作为礼物搜索）的场景词，是否收录需结合自身商品是否适配该场景判断，不能仅因搜索量高就收录。
- 竞品选择偏差会直接传导到整个词库：若种子 ASIN 与自身商品定位差异较大（价格带、细分场景不同），反查结果的参考价值会显著下降，需要在种子选择阶段一并核实。
- 错拼词的收录应仅用于后台隐藏关键词等允许自由文本的位置，不应写入面向顾客展示的标题或图片文案中。

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

1. 选定 2-3 个与自身商品定位最接近的竞品 ASIN（同定位而非同类目下任意热卖品），作为反查关键词的种子。
2. 用第三方反查 ASIN 类关键词工具，获取这些竞品当前表现较好的关键词全集，先按工具默认的“竞品综合表现”排序保留一份原始结果，不预先手动删减。
3. 将结果改按搜索量从高到低重新排序，取一个可管理的数量范围作为初始词库，而不是全部收录。
4. 逐词判断与自身商品购买意图的匹配程度，拆分为高相关、中相关（可能是关联需求或礼品等场景）、低相关（明显是找别的商品）三档，低相关词直接排除出候选。
5. 对高相关词库额外跑一次常见拼写变体检测，识别出未被平台自动纠错覆盖、且有一定搜索热度的错别拼写，补充为独立的错拼词表。
6. 最终产出按“高相关-中相关-错拼”分层的词库，用于后续标题/五点/后台关键词等 Listing 位置的分配，分配时优先保证高相关词覆盖，再视位置余量安排中相关与错拼词。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：需要第三方反查 ASIN 关键词、搜索量与拼写变体检测能力，通过关键词类数据连接器获取竞品关键词表现与搜索量估算，作为代理证据使用，不作为 Amazon 官方一方事实。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 竞品种子 ASIN 清单
- 关键词原始反查结果
- 高/中/低相关分级词库
- 错拼变体词表
- 分位置关键词分配方案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
