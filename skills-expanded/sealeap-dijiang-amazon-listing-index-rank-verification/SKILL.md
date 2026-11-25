---
name: sealeap-dijiang-amazon-listing-index-rank-verification
description: "After integrating researched keywords into listing fields, verify indexing status for each exact target phrase and establish a rank-tracking baseline, so that keyword or PPC underperformance can be diagnosed as an indexing gap versus a genuine ranking problem rather than assumed. Use for 关键词写进标题为什么还搜不到、backend关键词怎么分配、A+页面要不要放文字、怎么验证关键词有没有被索引. Do not use to claim a specific ranking position or timeline as guaranteed — indexing confirms eligibility only, not position."
---

# Amazon 关键词索引与排名验证闭环

## 目标

After integrating researched keywords into listing fields, verify indexing status for each exact target phrase and establish a rank-tracking baseline, so that keyword or PPC underperformance can be diagnosed as an indexing gap versus a genuine ranking problem rather than assumed.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 关键词工具反查出的竞品词表与索引、排名检查结果均为第三方或平台前台观测，可能受账号、地域、时间点影响，不等同于平台内部真实排序依据。
- 已索引只代表该词有资格参与匹配，不代表能获得可见排名，两者需分开记录，不要混用同一个结论。
- 后台关键词字段的长度限制与加强型内容的索引规则均随平台迭代变化，以当前后台实际提示为准。

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

1. 选词来源上明确区分转化导向的电商专属关键词工具与通用搜索引擎的SEO工具：后者反映的是信息类搜索意图，与电商平台上的交易类搜索意图不同，选词与验证都只用电商平台自身或专门针对该平台的数据源。
2. 把筛选后的关键词分配进标题、五点、描述与后台关键词字段时遵守两条纪律：同一个词在可读的前提下出现一次即可完成索引，不需要重复堆砌；越靠前的位置权重通常越高，把最短、最相关、优先级最高的词组放在标题最前部。
3. 标题、五点、描述里放不下的长尾词移入后台关键词字段，注意该字段存在长度上限（以当前后台实际限制为准，不套用某个固定字符数），已在可见文案中出现过的词不要在后台重复浪费额度。
4. 如果品牌已开通加强型内容页面，确保每一处视觉素材旁边都配有可被抓取的文字说明，不要做成整屏纯图片：图片本身通常不被搜索引擎索引，配套文字才能让这部分内容也计入索引与站外搜索引擎收录。
5. Listing发布或改动后，逐条核对目标关键词的精确短语是否已被索引，而不是只确认组成该短语的单个词被索引，确认口径为该完整词组作为一个短语是否命中，避免误判。
6. 对已确认索引成功的核心词建立排名跟踪基线，记录起始自然位置，后续无论是自然优化还是广告投入，都对照这个基线判断是否真的带来排名变化，而不是凭感觉认为有在动。
7. 若某个目标词迟迟未被索引，先复查该词是否确实以完整短语形式出现在任一被索引字段中，再考虑是否是词本身相关性不足，不要跳过索引核查直接归因为不相关。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取目标关键词当前的自然排名快照与索引状态，作为发布后验证的第三方前台观测证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 关键词分配到各Listing字段的清单（含前台文案词与后台专用词）
- 索引核查记录（逐词组、逐字段）
- 排名跟踪基线与后续变化记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
