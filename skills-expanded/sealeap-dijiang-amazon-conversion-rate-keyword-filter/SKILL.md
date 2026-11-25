---
name: sealeap-dijiang-amazon-conversion-rate-keyword-filter
description: "Filter and prioritize keywords by historical conversion rate and market-concentration signals rather than raw search volume alone, manually verify each candidate phrase against live search results for genuine relevance, and split the surviving list into primary listing/PPC terms versus backend-only indexing terms. Use for 大词好还是长尾词好、关键词该放正文还是后台、怎么判断一个词值不值得砸广告. Do not use to treat any third-party conversion-rate or market-availability metric as an Amazon-confirmed fact — treat it as a vendor-specific estimate."
---

# Amazon 转化率优先关键词筛选

## 目标

Filter and prioritize keywords by historical conversion rate and market-concentration signals rather than raw search volume alone, manually verify each candidate phrase against live search results for genuine relevance, and split the surviving list into primary listing/PPC terms versus backend-only indexing terms.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 转化率、市场集中度、动销效率等指标均来自第三方工具的历史估算，口径与算法不透明，属于前台观测代理指标，不等同于平台内部真实成交数据。
- 固定的转化率或集中度分界百分比是来源给出的个人经验值，需按自身类目重新校准，不同价格带、不同类目的合理区间差异很大。
- 人工核验搜索结果相关性会受个性化、地域与登录状态影响，同一账号多次核验结果可能有差异，建议多次或换环境交叉确认后再下结论。

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

1. 建立候选词池时不要默认搜索量越大越该用，改为同时纳入该词的历史成交转化率与市场集中度（该细分需求中头部几家卖家吃掉了多少比例的成交量）两个维度，与按搜索量排序取词的常见做法形成对照，两种口径可以并行比较，不必二选一。
2. 优先保留转化率较高、且头部卖家集中度不算太高的词，而不是只看绝对搜索量大小；转化率与集中度的具体分界线按自身类目与竞争格局设定，不套用某个固定百分比。
3. 对第三方工具给出的预计需要多少动销量才能自然进入首页一类效率指标，只作为在多个候选词之间比较相对难度的参考，不当作精确可实现的承诺。
4. 汇总出候选词表后逐词到搜索结果里人工核验：实际搜索该词组时排在前面的商品是否真的与自己商品是同一类，若结果里大量是不相关商品，说明这个词字面相关但购买意图不匹配，标记为仅索引不主推。
5. 把通过人工核验、转化与集中度表现俱佳的词标记为主力词，用于Listing正文与广告重点投放；把相关性不足或效率指标较差、但仍有一定关联的词标记为仅后台索引，只放入后台关键词字段。
6. 定期用同一套口径复核主力词清单，因为转化率与集中度会随季节、竞品变化而改变，不作为一次性结论长期沿用。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选关键词的历史成交转化率与市场集中度等第三方估算指标，作为按搜索量排序之外的补充筛选证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 转化率与市场集中度双维度候选词表
- 逐词搜索结果相关性人工核验记录
- 主力词/仅索引词分层清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
