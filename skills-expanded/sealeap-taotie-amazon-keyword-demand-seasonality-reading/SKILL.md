---
name: sealeap-taotie-amazon-keyword-demand-seasonality-reading
description: "Read keyword-research tool output correctly: prefer multi-month search and purchase-rate history over last-month snapshots, interpret search-result counts as a loose competition proxy, spot head terms with low conversion, extract high-frequency modifiers for listing and selling points, and time seasonal product decisions by lead time to the peak. Use for 关键词搜索量准不准、月搜索量怎么算、旺季月份怎么看、购买率是什么、大词转化低正常吗、搜索结果数代表竞争吗、高频词怎么用、季节品什么时候定. Do not use to claim exact search volumes as facts or to select bids from tool data alone."
---

# Amazon 关键词需求与季节性判读

## 目标

Read keyword-research tool output correctly: prefer multi-month search and purchase-rate history over last-month snapshots, interpret search-result counts as a loose competition proxy, spot head terms with low conversion, extract high-frequency modifiers for listing and selling points, and time seasonal product decisions by lead time to the peak.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 购买率、搜索量、搜索结果数均为第三方估算且可能存在计算错误（来源发现过购买率显示与计算不一致），任何结论都要标 ESTIMATE 并可回指来源工具。
- 「大词转化低、卖家转投长尾」是来源对趋势变化的解释，属待验证假设，用本账户搜索词报告验证。
- 旺季月份与转化最好的月份因类目不同，来源举例的月份与增长率不作规律。
- 来源的工具推荐与团购信息不采纳；本 Skill 只描述工具类别与数据口径。

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

1. 拉取候选关键词列表时不按匹配类型预筛，先全量导出再离线筛选；记录工具的搜索量口径（例如翻页计入多次搜索）与数据月份，标注为 ESTIMATE。
2. 用历史趋势替代上月快照：看近一到两年的逐月搜索量与购买率曲线，找出需求最高的月份与转化最好的月份（两者常不同：大促月搜索高但转化未必高），并对比不同年份同月是否结构性下滑。
3. 识别大词：搜索量很大但购买率极低的主词通常不适合作精准投放或排名主攻，把预算优先给购买率高的长尾词；这一判断要用本账户广告数据复核。
4. 把搜索结果数只当作竞争度的粗指标：它与前台实际结果因配送地区、类目筛选而不同，同时看头部 Listing 的评论与价格才能判断进入难度。
5. 从高频词中提取修饰维度（性别、尺码、颜色、款式、材质）：用于 Search Terms 去重布局与卖点排序，只选与本品实际匹配的词，不堆砌。
6. 季节品倒推时间表：从旺季首月减去采购、头程与入库时间得到最晚决策日期；错过则改为准备下一季，不在旺季中途仓促入场。
7. 多工具校准：同一词在不同工具的搜索量可能相差数倍（来源观察到不同来源的工具相差约一半量级），并列保留各家口径，用平台一方数据或公开搜索趋势核对方向，不取无依据的平均值。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取关键词逐月搜索量、购买率、搜索结果数与高频词的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 关键词数据口径记录
- 历史趋势与旺季判读表
- 大词/长尾词分层清单
- 高频词修饰维度表
- 季节品决策时间表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
