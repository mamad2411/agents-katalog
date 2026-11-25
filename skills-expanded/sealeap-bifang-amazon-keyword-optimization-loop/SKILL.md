---
name: sealeap-bifang-amazon-keyword-optimization-loop
description: "Run a five-stage keyword workflow for an Amazon listing: collect candidate terms from several comparable ASINs, screen them by product-fact relevance and observed performance, embed the shortlist into listing copy, raise weight on a few priority terms through controlled advertising, then monitor indexing and rank to decide what to add, cut or roll back. Use for 关键词怎么找、关键词筛选、标题埋词、关键词清单、关键词加权、关键词监控调整. Do not use to rewrite a live listing or change bids without an approved change table and a rank baseline."
---

# Amazon 关键词搜集筛选埋词闭环

## 目标

Run a five-stage keyword workflow for an Amazon listing: collect candidate terms from several comparable ASINs, screen them by product-fact relevance and observed performance, embed the shortlist into listing copy, raise weight on a few priority terms through controlled advertising, then monitor indexing and rank to decide what to add, cut or roll back.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源建议的竞品样本数量是经验值；以候选词能否形成多样本交叉为准，不作为规律。
- “他人品牌词无转化”和“核心大词中小卖家打不起”是来源经验，需以当前账户的搜索词报告与 CPC 校准；品牌词还涉及商标与广告政策，按当前政策处理。
- “官方社媒促销码比站外促销更能拉升关键词权重”是来源主观感受，属待验证假设；只能通过账户内前后对比观测，不外推为平台算法。
- 关键词收录与排名查询受地区、登录态、变体与个性化影响；单次查询不作结论，需同一条件多次采样。

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

1. 先固定对象：marketplace、ASIN/SKU、产品事实（核心功能、规格、适配范围）与目标购买意图；再选取若干个同购买意图、表现稳定的可比 ASIN 作为反查样本，样本数量以候选词能形成多样本交叉为准，只依赖单一 ASIN 的词表视为样本不足并标 NEEDS_EVIDENCE。
2. 搜集：用关键词反查（优先带转化记录的出单词反查）与关键词拓展拉取各样本词表，合并去重后保留每个词的来源 ASIN 数、搜索量代理、点击/转化份额等原始字段形成候选词池；这一步只收集不取舍。
3. 筛选（最耗时的一步）：逐词按三类判断——①与本品事实的匹配度：产品名称级主词必须进标题，他人品牌词一律剔除，含主观最高级或依赖外部条件才成立的宣称词只有在产品事实能长期支撑时才保留；②多样本交叉出现次数；③观测指标（点击/转化份额、垄断度）。用对比视图把相近词放在一起看，再分组为标题必入词、五点/描述补充词、广告候选词，并写下每个剔除词的理由。
4. 埋词：把分组清单交给撰写者（母语撰写者或自己），要求覆盖清单内全部指定词且语句通顺地道；交付后逐词核对覆盖情况，缺词回炉；改动前保存旧版文案作为回退值。
5. 加权：只对少数优先长尾词用手动精准投放拉动；核心大词是否投放按当前账户的 CPC 与盈亏平衡 ACOS 校准而不是默认投放；已完成品牌备案的卖家可评估平台官方的社媒促销码等工具；每次加权动作写入变更记录（对象、旧值、新值、预期）。
6. 监控：改动后在固定采样条件下查关键词收录与自然/广告位置，与埋词前基线比较；目标词持续下滑或收录消失时先回退文案再排查；按周期用数据决定加词、否词与预算/竞价调整，结论只写成账户内证据，不外推为平台规律。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取可比 ASIN 的关键词反查、搜索量与相关词代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 候选词池（含来源 ASIN 数与观测指标字段）
- 分组关键词清单（标题必入/补充/广告候选，含剔除理由）
- 埋词覆盖核对表与旧版文案回退值
- 加权动作变更记录
- 关键词收录与位置监控基线及复盘结论
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
