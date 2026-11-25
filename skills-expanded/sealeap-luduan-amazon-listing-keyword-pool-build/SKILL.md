---
name: sealeap-luduan-amazon-listing-keyword-pool-build
description: "Build a tiered keyword material sheet for a new Amazon listing by harvesting competitor titles, bullets and reverse-ASIN traffic terms, de-duplicating and ranking them, hand-tagging core, peripheral, same-audience and misleading terms, then expanding core terms into relevant long-tails with search and purchase metrics. Outputs evidence-backed material tables, not a finished listing or a claim about how Amazon matches queries. Use for 新品关键词怎么找、竞品反查关键词整理、核心词周边词长尾词分层、写 Listing 前的词表、五点卖点词汇整理、Search Term 备选词. Do not use to write or overwrite live listing fields, or to treat any third-party search volume as Amazon first-party data."
---

# Amazon Listing 关键词素材库搭建

## 目标

Build a tiered keyword material sheet for a new Amazon listing by harvesting competitor titles, bullets and reverse-ASIN traffic terms, de-duplicating and ranking them, hand-tagging core, peripheral, same-audience and misleading terms, then expanding core terms into relevant long-tails with search and purchase metrics. Outputs evidence-backed material tables, not a finished listing or a claim about how Amazon matches queries.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源把“单数搜索量高于复数”“竞品流量词里出现无关词是算法按相似度匹配”当作结论；本 Skill 只记为待验证假设，词形取舍以当前站点的第三方数据与自身搜索词报告校准。
- 来源建议把常见拼写错误词放进 Search Term；这与当前后台 Search Term 规范可能冲突，先核对当前字段规则，且不得占用核心词位置。
- 来源提到部分类目转化率很高、低搜索量词也值得做，这是经验判断；任何词的价值以上线后搜索词报告的点击与转化为准，不用搜索量单一指标下结论。
- 第三方工具的搜索量、购买量、类目归属均为估算，不同工具口径不能混表；工具不可用或额度不足时记录缺口并停止，不伪造数据。

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

1. 先定产品事实与站点语言：产品是什么、给谁用、核心属性（规格层级/材质/安装方式/尺寸等）、目标站点；语言基础弱时准备翻译工具，但词表的取舍仍要人工逐条过。
2. 选竞品参照物：按自身体量定样本，中大卖看销量领先的 Listing，小卖优先评价数少但销量尚可的 Listing；样本数量以当前类目校准，来源经验值仅作参考。不刻意回避竞品已用词，此阶段目标是“找对词”而不是“找没人用的词”。
3. 逐个收集三类素材到三张表：标题表、五点表、流量词表（第三方反查工具导出的竞品流量词）；流量词表按“关键词/月搜索量/所属类目/月购买量/旺季时间”字段并表，先去重再按搜索量降序，删除无搜索量的词。
4. 人工打标：高度匹配本品的标为核心词；受众相同但指代相邻产品的词与非精准但可用于 Search Term 的词标为周边词；语义指向其他物品的高搜索词（易误导）排除并写明原因；颜色/尺寸/场景修饰词与拼写变体单独记录。低搜索量的尾部也要翻，常能发现表达方式差异（同义写法、单复数、地点词）。
5. 用部分核心词到第三方工具做相关词扩展，导出后按所属类目过滤掉明显无关类目，剔除旺季明显属于过去某一年的一次性词与月购买量为零的词；不用商品数、点击集中度、购买率做筛选依据，它们回答的是竞争问题而不是相关性问题。
6. 把核心词与周边词上传到第三方工具补齐指标（搜索量、购买量、旺季），与长尾表合并成最终素材表；核心加周边控制在可管理规模，长尾保留数百量级，具体以当前类目校准，来源经验值仅作参考。
7. 归纳竞品五点的常见卖点词组（如规格层级、安装方式、材质、易安装、尺寸标注方式、省空间、耐用等，按类目替换）与标题结构（品牌/工艺词/形容词/名词/尺寸/颜色的排列方式）作为写作参考；不理解的行业术语查证后再用，不随意拆改竞品可读的词组。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品的反查流量词、相关词扩展及搜索量/购买量估算，作为词表整理的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 竞品参照物清单（选择理由与体量口径）
- 三张原始素材表（标题/五点/流量词）
- 核心词表与周边词表（含打标理由与指标）
- 高相关长尾词表（按类目与购买量过滤）
- 竞品卖点词组与标题结构归纳
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
