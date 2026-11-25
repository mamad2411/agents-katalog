---
name: sealeap-taowu-amazon-fba-fbm-margin-estimate
description: "Estimate per-unit profit and margin for a candidate product before the first purchase order using Amazon's fee calculator with the seller's own price, landed cost, packaging, inbound freight and fulfillment assumptions, then compare FBA against FBM and test the result against a pre-set margin floor and a demand estimate. All inputs are recorded with source and date so the sheet can be re-run when fees change. Use for 利润率怎么算、FBA 费用计算器怎么用、FBA 和 FBM 哪个划算、下单前算毛利、头程分摊到单件、目标利润率定多少. Do not use to make a final sourcing decision without verifying current fee schedules, and do not treat third-party sales estimates as facts."
---

# Amazon FBA/FBM 下单前利润测算

## 目标

Estimate per-unit profit and margin for a candidate product before the first purchase order using Amazon's fee calculator with the seller's own price, landed cost, packaging, inbound freight and fulfillment assumptions, then compare FBA against FBM and test the result against a pre-set margin floor and a demand estimate. All inputs are recorded with source and date so the sheet can be re-run when fees change.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源把“低于对标价格就能排第一/拿 Buy Box”当作前提；Buy Box 由多因素决定，价格只是其中之一，作为待验证假设处理。
- “首单为估算月销两倍”“FBA 使销量提升某个百分比”是来源经验值；按当前品类周转、资金和仓储成本校准，来源比例仅作参考。
- 第三方月销估算与官方计算器的费率都可能过时或口径不同；每次测算记录工具版本、日期与站点，费率变动后重跑。
- 本 Skill 不给出具体运费或费用数字；头程与派送成本一律按当前费率与承运商报价核对后填入。

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

1. 先设定本业务的目标利润率下限（按资金成本、广告占比、退货率和运营成本反推），并写明该下限适用的价格带和运营模式；来源的目标区间只作参考。
2. 选定对标 Listing 与售价：记录可比竞品的售价、评分、评论量与 Buy Box 情况，确定自己的定价假设并说明理由（同价、略低或差异化）；不要默认“更低价就能拿到 Buy Box”。
3. 估算月销量：记录对标 ASIN 与类目排名，用第三方估算工具得到月销区间并标为 ESTIMATE；同时用评论增速或多工具对照校准量级。
4. 在官方费用计算器中按对标 ASIN 或产品尺寸重量填写 FBM 列：售价、向顾客收取的运费、单件包装材料、单件寄送成本、客服成本；再填 FBA 列：售价与单件头程（总运费按当前承运商报价除以件数）；两列共用单件采购成本（订单总额除以件数，含样品与杂费）。
5. 读取单件利润与利润率并与下限比较：低于下限先检查定价、采购报价、包装与头程假设能否改善，不能改善则放弃；同时核对计算器使用的费用版本与生效日期。
6. 决定 FBA 还是 FBM：在利润差之外，把订单量级、退货与客服负担、自发货时效和仓储费一起纳入判断；量大且人手有限时通常接受一定利润差换取 FBA，但以自己的量和成本为准。
7. 用估算月销与保守的 FBA 增量假设推算月利润，并写明订单数量、资金占用与再下单触发点；输出可复算的测算表，费用或汇率变化时重跑。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取对标 ASIN 的价格、评论、排名与第三方月销估算作为测算输入。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 目标利润率下限及其依据
- 对标 Listing 与定价假设记录
- 月销量估算区间（工具、口径、日期）
- FBA 与 FBM 单件利润对比表（全部输入项、来源与日期）
- 采购决策结论与再下单触发点
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
