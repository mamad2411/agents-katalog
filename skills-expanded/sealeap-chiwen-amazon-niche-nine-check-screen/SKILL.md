---
name: sealeap-chiwen-amazon-niche-nine-check-screen
description: "Run a nine-checkpoint screen on a candidate product niche — long- and short-term demand trend, a competition-density ratio, brand concentration among top listings, fulfillment-method mix, price-band distribution, listing-age composition, and new-entrant share with its review/rating threshold — before committing to sourcing. Produces a structured multi-signal read instead of a single-metric judgment call. Use for 新类目值不值得进、选品前系统性验证、判断类目是否有新卖家机会、避免只看销量就选品. Do not use as the sole gate for a sourcing decision without also checking unit economics, IP/compliance risk, and supplier feasibility."
---

# Amazon 选品九维交叉验证

## 目标

Run a nine-checkpoint screen on a candidate product niche — long- and short-term demand trend, a competition-density ratio, brand concentration among top listings, fulfillment-method mix, price-band distribution, listing-age composition, and new-entrant share with its review/rating threshold — before committing to sourcing. Produces a structured multi-signal read instead of a single-metric judgment call.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 竞争密度指标的计算方式和分档区间是来源给出的一种经验方法，实际参考的搜索量与结果数口径因数据源而异，需用当前数据源重新校准，不代入来源数字。
- 品牌集中度、自营占比、价格带、新品占比等具体百分比均为示例性观察，不代表当前市场真实分布，每次调研需重新拉取当时数据。
- 新品门槛判断（评论数量级、评分线）会随类目审核政策和平台质量标准变化，只作为相对比较的参考方向，不作为固定达标线。
- 本方法覆盖需求与竞争维度，不包含利润测算、供应链可行性与知识产权排查，需配合其他环节才能形成完整选品决策。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 拉取候选类目的长周期（如近5年）与短周期（如近1年）搜索或销量趋势，筛掉长期走平或明显衰退的类目，短周期中警惕季节性过强、压货风险高的品类。
2. 用「周期搜索量 ÷ 头部竞争结果数」之类的比值构造一个竞争密度参考指标，具体区间需用当前市场与数据源重新校准，不套用固定分档。
3. 统计类目 Top 结果中的品牌集中度：品牌数量、前几名品牌各自份额，判断是否有品牌垄断大半市场，垄断度越高新卖家切入越难。
4. 统计 FBA 与平台自营占比，自营占比显著偏高的类目通常意味着平台既是裁判又是选手，需谨慎评估能否与之竞争。
5. 分析价格带分布，确认主流可接受价格区间，结合客单价判断是冲动消费型还是需要决策思考的品类，据此设计定价与推广策略。
6. 统计 Top 结果中不同上架时间的产品占比，识别市场是快速迭代还是存在长生命周期常青款，判断新品切入的节奏空间。
7. 核算新品（如近半年上架）在 Top 结果中的数量占比与销量占比，同时核对达到该销量所需的评论数量级与平均评分门槛，综合判断新品实际进入门槛高低。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取候选类目 Top 结果的销量趋势、品牌与履约分布、新品评论数据，作为九项指标计算的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 长短周期趋势筛选记录
- 竞争密度与品牌集中度评估表
- 价格带与上架时间结构分析
- 新品机会与门槛核对记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
