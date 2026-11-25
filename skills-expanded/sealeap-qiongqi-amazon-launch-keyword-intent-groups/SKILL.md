---
name: sealeap-qiongqi-amazon-launch-keyword-intent-groups
description: "Build a launch or relaunch keyword master list for an Amazon product by reverse-searching organically ranked comparable competitors, filtering to a focused core set, and grouping terms by buyer intent into campaign-ready lists with negations. Use for 新品关键词调研、关键词怎么分组、关键词太多怎么筛、竞品反查关键词、精确广告分组、广泛广告否定词. Do not use for mining an existing product's own search term reports."
---

# Amazon 新品关键词调研与购买意图分组

## 目标

Build a launch or relaunch keyword master list for an Amazon product by reverse-searching organically ranked comparable competitors, filtering to a focused core set, and grouping terms by buyer intent into campaign-ready lists with negations.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 『不要预先穷举成千上万长尾词、要给平台留寻找空间』是来源观点，属待验证假设；关键词覆盖过窄时可放宽过滤条件。
- 第三方反查数据为估算，搜索量与排名受采样时间、变体与个性化影响；筛选阈值不是固定规律，以类目数据与样本校准。
- 按意图分组依赖对产品事实的判断，分组错误会污染活动数据；上线后用搜索词报表核对每组实际触发的搜索词。
- 竞品数量与筛选参数为来源经验值，以当前类目的竞争密度校准。

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

1. 用主搜索词在目标站点搜索并隐藏赞助位，只看自然排名结果；逐个核对，挑选一组与本品『同类且同价值主张』的靠前竞品（来源经验为个位数到十个左右），排除虽同词但用途或客群不同的产品。
2. 用第三方工具反查这组竞品的自然排名关键词，只取自然口径；先看未筛选总量，再设过滤条件：最低搜索量、至少若干个竞品共同排名、竞品排名不超过一定名次，把清单收敛到可管理的核心集合（来源经验为数十到一百多词），阈值按类目数据校准。
3. 逐词标注购买意图/语义核心（场景、材质、尺寸、人群、功能等），同一意图归一组；另拆出竞品品牌词、自有品牌词、明确不相关的否定词，以及偏『逛店』意图、适合用 SB 引到品牌旗舰店的词。
4. 从核心集合里挑出搜索量最大、相关性最高的少数词做单词活动；每个意图组各建一个精确匹配活动，同组共享目标与预算。
5. 广泛匹配活动用同一词表投放，但把已知不相关成分作为词组否定预置进去，给平台留寻找长尾的空间，同时堵住已知浪费。
6. 竞价用起始竞价公式（目标 ACOS × 售价 × 转化率）而非默认建议值，策略默认只降低；广告位加成留空或小幅起步；预算先在活动规划表定总日预算再分配到各活动。
7. 输出关键词主表与活动结构草案，上线后用搜索词报表回流验证分组假设，把实际触发的搜索词回填到对应意图组。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品自然排名关键词、搜索量与排名名次的第三方代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 竞品样本清单
- 关键词主表（按意图分组）
- 否定词与品牌词清单
- 活动结构草案
- 起始竞价与预算分配表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
