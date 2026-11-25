---
name: sealeap-tianlu-amazon-order-drop-multifactor-diagnosis
description: "When order volume drops during a period with multiple concurrent changes (an external ad-channel disruption, a tightened compliance review cycle, and warehouse or inbound congestion), evaluate each candidate cause against its own account-specific evidence — external traffic-source records, category-specific compliance notices actually received, and FBA inbound or receiving status — before assigning weight to any single factor. Produces a per-factor evidence table rather than a single narrative cause. Use for 单量或流量断崖下滑排查、多因素同时变化时的归因分析、备货与广告结构应对措施制定. Do not use to attribute a drop to one popular narrative (such as a single ad-channel change) without checking the account's own traffic-source, compliance-notice, and inbound-status evidence first."
---

# Amazon 单量下滑多因素归因

## 目标

When order volume drops during a period with multiple concurrent changes (an external ad-channel disruption, a tightened compliance review cycle, and warehouse or inbound congestion), evaluate each candidate cause against its own account-specific evidence — external traffic-source records, category-specific compliance notices actually received, and FBA inbound or receiving status — before assigning weight to any single factor. Produces a per-factor evidence table rather than a single narrative cause.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 站外广告渠道暂停、合规审查升级、仓库爆仓是来源对某一时段现象的观察总结，三者是否同时对本账户成立、各自贡献多大权重必须用自身账户证据核实，不能整体套用。
- 来源提到的关店数量、占比等统计数字来自第三方或个案观察，未核实统计口径与样本范围，不能作为本账户风险概率的依据。
- 聚焦高转化词、缩减高 ACOS 词等广告调整建议需要以账户自身的盈亏平衡 ACOS 与转化数据校准，来源未给出可迁移的固定阈值。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、广告归因窗与业务报告时间窗
- 广告订单、总订单、会话、自然位置、TACOS 与贡献利润
- 价格、优惠、库存、Buy Box、Listing 和评论变更日志
- 查询、广告位和投放对象的相关性证据

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先核实下滑的时间点、幅度与影响范围（哪些站点、哪些 ASIN、自然单还是广告单或两者都降），排除数据口径或统计窗口错位造成的假下滑。
2. 核对账户自身的外部引流渠道是否在同期确实出现过投放中断或暂停，用自身投放记录而非传闻判断是否受影响，并核对受影响渠道占该账户流量的实际比例。
3. 核对账户所在类目是否收到过官方的合规审核通知或后台资料补充要求，未收到通知的类目不应假设自己也受合规收紧影响。
4. 核对计划入仓/在途货件在目标仓库的实际接收与上架状态，确认是否存在入仓受阻、上架延迟导致的库存断货或可售库存下降，作为物流因素是否成立的证据。
5. 对三类候选因素分别打分（是否有本账户直接证据支持、影响的产品或流量占比），按证据强度排序后再决定优先应对哪一项，而不是同时全面出击。
6. 针对证据确认成立的因素分别执行对应动作（如物流方面错峰发货备战后续大促、广告方面按订单分布收紧高 ACOS 词、合规方面按通知要求补充资料），并设定下一次复核下滑是否缓解的时间点。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：如需判断下滑是账户自身问题还是同类目大盘现象，可用第三方类目趋势数据连接器核对同期大盘走势作为参照证据，不单凭主观归因或个案传闻。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 下滑现象核实记录（时间/幅度/范围）
- 三因素证据核对表（渠道/合规/物流各自的账户证据与占比）
- 证据强度排序与优先应对结论
- 分因素应对动作清单与复核时间点
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
