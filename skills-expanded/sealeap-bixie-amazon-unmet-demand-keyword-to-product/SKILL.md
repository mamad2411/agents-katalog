---
name: sealeap-bixie-amazon-unmet-demand-keyword-to-product
description: "Identify keywords with rising search volume and click interest but below-benchmark conversion as unmet-demand signals, then run them through AI-assisted product-candidate generation and a market, competitive, and profitability validation gate. Rejects candidates that fail the profit or IP check before sourcing. Use for 找搜索量高转化低的词、选品没方向想从需求反推、AI拓品候选验证. Do not use to place a purchase order directly from the candidate list, or to skip the patent and compliance check."
---

# Amazon 未满足需求选品闭环

## 目标

Identify keywords with rising search volume and click interest but below-benchmark conversion as unmet-demand signals, then run them through AI-assisted product-candidate generation and a market, competitive, and profitability validation gate. Rejects candidates that fail the profit or IP check before sourcing.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 转化率低于基准里的基准本身是一个统计估算值，受价格带划分、时间窗口选择影响较大，判断前需确认基准口径与自身产品是否真正可比。
- AI 生成的产品建议是启发式候选，不能替代正式的专利检索、供应链可行性与合规审查，落地前必须补齐这些独立验证步骤。
- 搜索量上升与点击率高只反映需求信号，不代表已验证的可盈利空间，利润核算未通过前不应视为已确认机会。

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

1. 在广告后台的需求探测类功能里，筛出搜索量环比上升、点击率高于同类目均值、但转化率低于同价位基准的关键词，作为未满足需求的候选池。
2. 对候选词逐个核实转化率基准的可比口径（同价格带、同产品类型），避免把跨品类或跨价位的基准直接套用。
3. 用 AI 拓品工具输入候选词与相关竞品 ASIN，生成细分方向（优化现有产品解决该需求）与互补方向（围绕该需求做配套新品）两类候选。
4. 对候选逐个核实市场趋势、供需比、价格带与头部竞品格局，排除趋势向下或头部垄断过强的方向。
5. 结合 AI 做评论声音、关键词延展与利润核算，任何一项显示不可盈利或强负面反馈的候选直接淘汰。
6. 落地前对入围候选做专利与合规初筛，存在明显风险的候选放弃或转为需要人工复核的待定项。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：核实候选品类的市场趋势、竞品格局与评论声音作为需求验证阶段的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 未满足需求关键词清单
- AI拓品候选分类表
- 市场验证结果表
- 利润与合规核查记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
