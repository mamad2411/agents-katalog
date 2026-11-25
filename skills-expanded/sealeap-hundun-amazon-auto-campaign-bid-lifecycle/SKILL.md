---
name: sealeap-hundun-amazon-auto-campaign-bid-lifecycle
description: "Structure an automatic Sponsored Products campaign with a naming and portfolio convention that scales across many products, then match its bid strategy — dynamic up-and-down, fixed, or dynamic-down-only — to the listing's lifecycle stage (new, growing, mature) using observed CPC ranges and organic-share trends as evidence, deferring negative keywords and negative product targeting until enough real search-term and click data exists. The stage-to-bid-strategy mapping and any organic-rank-lift effect from sustained ad placement are treated as account-level hypotheses, not guaranteed platform mechanics. Use for 自动广告竞价策略怎么选、新品期出价多少合适、什么时候用固定竞价、否定词和否定词组区别、要不要否定竞品ASIN. Do not use to pre-emptively add negative keywords before any real search-term data exists, and do not assume a specific daily-budget number is safe for all accounts without checking current context."
---

# Amazon 自动广告竞价阶段与否定词

## 目标

Structure an automatic Sponsored Products campaign with a naming and portfolio convention that scales across many products, then match its bid strategy — dynamic up-and-down, fixed, or dynamic-down-only — to the listing's lifecycle stage (new, growing, mature) using observed CPC ranges and organic-share trends as evidence, deferring negative keywords and negative product targeting until enough real search-term and click data exists. The stage-to-bid-strategy mapping and any organic-rank-lift effect from sustained ad placement are treated as account-level hypotheses, not guaranteed platform mechanics.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 竞价策略与产品阶段的对应关系（新品期动态、成长期固定、成熟期只降）是来源账户内观察到的经验模式，不是所有类目/竞争强度下都适用，需要以当前账户实际测试结果为准。
- “持续稳定占据某关键词广告位会带动自然排名上升”是待验证的算法假设，不能作为确定性因果结论对待，只能作为观察现象持续跟踪。
- 日预算的自然月合计上限、否定商品的判断阈值等具体数值均为来源经验值，需要用当前账户的实际数据重新校准。
- 否定词组存在误伤相关搜索词的风险，使用前应先看清该词组会覆盖哪些相邻词，避免过度否定导致有效流量被一并屏蔽。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 广告活动命名与分组：不使用系统默认的时间戳命名，改用“产品名+广告类型”的命名规则；用广告组合把同一产品下的自动、手动等广告类型都归到一起，便于按产品维度做优化和看数据。
2. 起量条件与预算：确认 listing 已在售、有可售库存、有购物车按钮后再开广告；新品期日预算从小额起步，先跑出曝光、点击与首批出单词等数据，不宜一开始就给到较大预算。
3. 竞价策略按阶段匹配：新品期（尚不知道有效竞价区间）用动态提高/降低竞价，配合第三方关键词工具查到的核心词 CPC 参考区间，设置一个区间中段偏上的起始竞价去探索；成长期（已摸到大致能出单的竞价水平、排名进入类目前列）改为固定竞价，把出价卡在已验证有效的区间内做精准控制；成熟期（自然流量占比明显提高）改为只降不升的动态竞价，控制花费。
4. 否定词时机：广告刚起量、还没跑出真实搜索词数据时不做否定；等有了实际点击/搜索词数据后，再逐条判断哪些词与产品不相关或转化差，优先用否定精确而不是否定词组，因为否定词组可能连带屏蔽掉本来相关的周边搜索词。
5. 否定商品定向：当自己的广告持续在某个明显性价比更高（价格更低、评论/评分更好）的竞品详情页下曝光但多次点击不出单时，可以把该 ASIN 加入否定商品，避免继续在无转化机会的位置花钱；不要在没有实际点击数据支持的情况下预判性否定。
6. 提交前核对：广告组合、开始/结束时间、日预算数值（尤其警惕多输入一位数导致预算被放大一个数量级）、竞价策略、投放商品、匹配方式是否都设置正确。
7. 提交后预期管理：广告通常需要一定延迟才会在前台产生曝光，短时间内看不到展示不代表配置有误，先等待再排查。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取目标核心关键词的历史CPC区间等第三方代理数据，用于校准新品期起始竞价范围。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 广告活动命名与组合结构规范
- 分阶段竞价策略对照表（新品期/成长期/成熟期）
- 否定词/否定商品判断记录
- 提交前检查清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
