---
name: sealeap-chiwen-amazon-fba-replenishment-formula
description: "Calculate a per-SKU replenishment quantity from three inventory buckets (sellable FBA stock, inbound-transit stock, and domestic-warehouse stock) plus a recency-weighted sales-velocity estimate, covering the combined production-and-freight lead time plus a safety-stock buffer. Falls back to the weighted current sales rate instead of a competitor-benchmarked target whenever confidence in reaching that target is low. Use for FBA补货算多少、库存三部分怎么合并统计、防止断货又不压货、搭建库存全景表动态调整. Do not use for one-off promotion-driven demand spikes without first adjusting the sales-velocity input, and do not use as a substitute for a stockout or overstock post-mortem."
---

# Amazon FBA补货量加权测算

## 目标

Calculate a per-SKU replenishment quantity from three inventory buckets (sellable FBA stock, inbound-transit stock, and domestic-warehouse stock) plus a recency-weighted sales-velocity estimate, covering the combined production-and-freight lead time plus a safety-stock buffer. Falls back to the weighted current sales rate instead of a competitor-benchmarked target whenever confidence in reaching that target is low.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 近7天/近30天的加权比例、安全库存天数、目标达成把握的判断线均是来源给出的经验参数，需按当前SKU的销量波动性与供应链稳定性重新设定，不代入固定数字。
- 对标竞品或行业目标销量的数据存在统计口径与延迟误差，只作为预期销量的待验证参考输入，不能替代自身实际销售数据。
- 该公式未覆盖旺季峰值、平台仓容限制、头程延误等突发变量，下单前需结合当前物流与仓储状态做人工复核。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、库存阶段、补货与到仓时间
- 断货或备货前后的销量、流量、广告、自然位置和转化基线
- COGS、头程、仓储、平台费、退货和清仓成本
- 可比产品的成熟度、销量区间和需求趋势

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 建立单 SKU 的库存全景表，实时拆分统计在售（已入FBA仓可售）、在途（已发货未到仓）、本地（待打包发出）三类库存，并汇总为当前总库存。
2. 计算加权现有销量：近7天日均销量与近30天日均销量按不同权重加权，近期权重更高，具体权重比例需按当前品类波动性校准，不固定套用单一比例。
3. 如需对标目标销量（如对标竞品或行业水平）提升备货，先评估达成该目标的把握；把握明显不足时直接采用加权现有销量作为预期销量，避免过度乐观备货。
4. 用「生产周期 + 头程运输时效」作为覆盖天数乘以预期销量得到周期消耗量，再加上安全库存（按加权现有销量的一段天数设定，天数按缺货成本与资金占用成本权衡确定）。
5. 本期采购量 = 周期消耗量 + 安全库存 − 当前总库存（在售+在途+本地）；结果为负数时说明短期无需补货，记录复核时间点而非强行下单。
6. 按固定周期重新跑一遍全景表与测算结果，根据实际到货和销量偏差动态调整下一期参数，不依赖一次性静态计算。
7. 库存明显高于预期消耗时评估促销去库存，库存逼近断货线时评估提高广告曝光或加快头程，两类信号都应触发人工复核而非仅靠自动化跑数下单。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：反查竞品或行业销量水平，作为目标销量预估环节的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- SKU库存全景表（在售/在途/本地/总库存）
- 加权销量与预期销量测算记录
- 本期采购量计算结果
- 动态调整触发记录（促销/提竞价预警）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
