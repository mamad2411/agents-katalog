---
name: sealeap-dijiang-amazon-sourcing-cost-arbitrage
description: "Compress landed product cost through a combination of cross-platform wholesale price comparison via a local sourcing agent, counter-seasonal ordering timing, smaller-factory relationship building, and negotiated delivered-duty-paid shipping terms, each verified against the current supplier's own quote rather than a generic benchmark. Use for 采购成本太高怎么办、1688和跨境B2B平台怎么比价、反季下单要注意什么、要不要用采购代理、DDP运费怎么谈. Do not use to bypass supplier vetting or skip quality inspection just to chase the lowest price."
---

# Amazon 跨境采购降本策略组合

## 目标

Compress landed product cost through a combination of cross-platform wholesale price comparison via a local sourcing agent, counter-seasonal ordering timing, smaller-factory relationship building, and negotiated delivered-duty-paid shipping terms, each verified against the current supplier's own quote rather than a generic benchmark.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源中给出的具体折扣比例、每件降价金额与个案收益数字均为不可验证的个案说法，一律不作为可复制的预期收益，实际压价幅度需以自己拿到的报价单为准。
- 使用本地采购代理引入了额外的信任与信息不对称风险（无法直接核实其转达的报价与实际成交价是否一致），应通过多方比价与阶段性验货交叉验证代理的可信度，不能单方面依赖代理的一面之词。
- “反季下单更便宜”“小厂更愿意让价”均为来源经验总结的一般规律，不同品类、不同工厂的产能周期和议价空间差异很大，需按具体供应商的实际排产情况验证，不构成保证。
- 到岸完税类运输条款要求供应商具备相应的清关与物流履约能力，并非所有供应商都能可靠执行，采用前必须先核实其过往履约记录，否则可能出现货物滞留或额外费用。

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

1. 对已在面向海外买家的 B2B 平台上找到的候选商品，用同款关键词的目标语言翻译后，到该地区对内的批发平台上做同款比价，核实是否存在明显的“外向平台加价”，差距异常大时要先怀疑是否图片盗用/非同款，而不是直接假设更便宜的一定是同一货源。
2. 若确认对内批发平台价格更优但自己无法直接下单沟通（语言/结算方式障碍），评估是否引入本地采购代理：明确代理费率/佣金结构、验货职责划分、出问题时的责任认定方式，并要求代理提供下单与质检的过程凭证。
3. 按目标品类的销售旺季倒推生产周期，尝试在同行普遍集中下单的窗口之前（工厂产能相对空闲期）完成打样与首批下单，以换取更优的报价与排产优先级；具体提前量需按该品类实际生产周期与自身资金占用能力反推，不套用固定月份。
4. 询价时不只筛选平台标注的顶级/金牌供应商，同时保留几家规模较小、排名靠后但响应积极的工厂作为对比对象，理由是小厂通常更愿意为拿到订单而在价格与定制上让步，但需要额外补做资质与产能核实，因为它们缺少平台高等级认证背书。
5. 有条件参加行业展会等线下渠道，当面考察工厂并直接议价，作为线上比价与代理沟通之外的补充验证手段，用于交叉核实报价与产能说法的真实性。
6. 在价格谈妥后，尝试与供应商谈成“到岸完税”一类的一口价运输条款，把清关、关税、末端配送整合进供应商责任范围，但仅对有可验证物流履约记录的供应商采用，避免把定价压力转嫁成后续物流失控的风险。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：如需核实同款商品在不同跨境B2B与对内批发平台上的报价差异，可用阿里巴巴/1688类数据连接器拉取公开的商品与供应商页面信息作为比价参考，不替代直接询价与验厂。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 同款跨平台比价记录
- 采购代理评估与责任划分说明
- 反季下单时间线
- 小厂候选与资质补充核实清单
- 运输条款谈判要点
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
