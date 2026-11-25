---
name: sealeap-feilian-amazon-buyer-segment-price-calibration
description: "Audit whether a reported shift toward value-driven, income-segmented buying behavior actually shows up in the account's own category conversion and price-band data before rebalancing keyword bidding, price bands, and the mix between high-consideration and everyday-replenishment items. Treats third-party consumer-sentiment findings as hypotheses to confirm with the account's own data, not as facts to act on directly. Use for 大促消费分层核实、价格带与关键词匹配复核、选品双轨结构评估、广告加码前的必要性判断、受影响SKU库存与清仓节奏规划. Do not use to assume a reported national consumer-sentiment shift applies to this account's category without checking its own conversion and price-band data first."
---

# Amazon 大促消费分层选品定价校准

## 目标

Audit whether a reported shift toward value-driven, income-segmented buying behavior actually shows up in the account's own category conversion and price-band data before rebalancing keyword bidding, price bands, and the mix between high-consideration and everyday-replenishment items. Treats third-party consumer-sentiment findings as hypotheses to confirm with the account's own data, not as facts to act on directly.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源引用的具体消费支出增减比例、分期付款使用率等数字均为第三方报告统计，抽样口径未知，仅作方向性参考，不能直接套用为本账户的预期变化幅度。
- 消费分层、流量转向比价通道等是来源对宏观现象的归因解读，因果关系未经验证，需用自身流量来源与转化数据独立判断，不作为确定结论直接执行。
- 选品双轨的具体品类方向是来源举例，需按自身供应链与品类竞争格局重新评估适配性，不直接套用来源示例的品类范围。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实与目标购买任务
- 关键词、商品投放、展示和视频的聚合表现
- 受众包定义、资格、站点限制和隐私边界
- 价格、评论、页面、库存与转化基线

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 用自身账户近期转化率、客单价分布与加购/弃购数据，核对价格敏感度上升、消费者更看重性价比等说法是否在本类目、本店铺真实出现，而不是直接采信第三方报告结论。
2. 若确认存在价格敏感度上升迹象，重新核对广告关键词与价格带的匹配度：检查高客单价词是否投向已降价或促销中的Listing，避免出价与实际到手价错配导致点击后跳出。
3. 评估现有产品结构是否同时覆盖高客单价刚需与日常复购刚需两类需求；对只覆盖单一价格带的品类，评估是否需要补充另一价格带的候选款，而非在同价格带内简单加大广告预算。
4. 在决定加大广告投放前，先用小额预算测试当前流量成本与转化是否确因分层现象改变，避免在流量价值实际下降时逆势加码导致投产比恶化。
5. 结合验证到的需求分层结果，提前规划受影响价格带SKU的库存周转与清仓节奏，对判断为需求转弱的产品预留提前促销出清的时间窗口。
6. 若考虑引入分期付款等新促销支付方式，核对其在目标站点的可用性、费用结构与顾客实际到手价，作为可选项测试而非默认执行项。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充同类目下不同价格带竞品的定价分布与相关关键词搜索量变化，作为消费分层假设是否适用于当前类目的交叉验证证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 消费分层现象自查记录（转化率/客单价/价格敏感度）
- 关键词与价格带匹配复核表
- 选品双轨结构缺口评估
- 受影响SKU库存与清仓节奏草案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
