---
name: sealeap-dijiang-amazon-supplier-quote-margin-ceiling
description: "Use Amazon's revenue/fee calculator together with a target net-margin threshold to reverse-solve the maximum acceptable landed unit cost, then use that ceiling to accept, negotiate, or reject supplier quotes, keeping unit cost strictly separate from operating expenses to avoid double-counting. Use for 供应商报价怎么判断能不能接受、用计算器反推成本上限、FBA费用怎么算、利润和到手货款对不上. Do not use to publish a specific margin percentage or fee rate as a fixed rule — always recompute from the current fee schedule and the account's own numbers."
---

# Amazon 供应商报价成本上限测算

## 目标

Use Amazon's revenue/fee calculator together with a target net-margin threshold to reverse-solve the maximum acceptable landed unit cost, then use that ceiling to accept, negotiate, or reject supplier quotes, keeping unit cost strictly separate from operating expenses to avoid double-counting.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的具体费率、天数与目标利润率均为示例，实际成交费构成、长期仓储触发周期与档位随类目、时间与平台当期规则变化，一律以下单前的当前费率表与计算器结果为准。
- 用月销高、评论少的竞品作为定价参照，反映的是这批样本当前的表现，不代表自己上架后一定能达到同等转化，仍需结合自身listing质量预期调整。
- 计算器给出的是估算值，实际到手金额还受退款、平台促销参与与阶段性费率调整影响，只作为决策参考而非最终对账依据。

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

1. 用官方收益计算器时优先手动填入供应商提供的真实包装尺寸与重量（单位统一换算），而不是直接套用平台上某个看起来差不多的竞品数据，因为尺寸重量直接决定履约费档位。
2. 定价前不要只看头部竞品当前售价，改用第三方插件或数据源按月销达到一定量、同时评论数较低筛出的一批同类商品，取其价格区间作为新品上市阶段更现实的可达定价参考。
3. 把计算器给出的成交费（通常有按比例与最低固定值两种取高的计费方式，具体比例与档位以当前费率表为准）、履约费、仓储费（旺季通常上浮，具体幅度按当前档位核实）加总，得到该定价下每单位的平台总成本。
4. 设定自己账户当前愿意接受的净利率目标，不套用来源中的固定比例作为普适规则，用定价减去平台总成本再减去目标净利润，反推出每件商品从下单到入仓全部到岸成本（含货款、头程运费、支付通道手续费）所能占用的最高额度。
5. 拿到供应商报价后，把货款、头程运费、支付手续费加总与上一步算出的成本上限直接比较：超过上限就先议价或换供应商，不因为只超一点点就默认接受。
6. 核算周期利润时，把工具、课程、账户级订阅等经营性支出计入损益表而非单件成本，并检查是否把已经支付过一次的选品或首批货款在回款到账时重复计成本，这是常见的对不上账的原因。
7. 若计划走自发货而非平台仓配，改用包材计算与头程运费查询类工具分别估算包装成本与末端配送成本，同样代入上述上限公式复核是否仍然划算。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充同类目在指定销量与评论区间下的价格分布，校准新品上市阶段更现实的定价参考。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 目标定价下的平台费用拆解表
- 目标净利率下的最高可接受到岸成本上限
- 供应商报价接受、议价或淘汰的判定记录
- FBM自发货成本估算对照（如适用）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
