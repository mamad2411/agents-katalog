---
name: sealeap-bifang-amazon-small-niche-market-screening
description: "Screen Amazon sub-markets for a capital-constrained seller by capping demand, checking top-listing concentration against the market average, filtering out seasonal curves, reading new-product share, price band and return-rate signals, and turning recurring return reasons into low-cost product improvements before deciding whether to enter. Use for 精铺选品、小类目选品、需求小竞争小的市场、头部垄断怎么判断、季节性产品怎么排除、退货率看什么. Do not use to place purchase orders or to evaluate large-volume categories that require brand-level capital."
---

# Amazon 小体量低垄断细分市场筛选

## 目标

Screen Amazon sub-markets for a capital-constrained seller by capping demand, checking top-listing concentration against the market average, filtering out seasonal curves, reading new-product share, price band and return-rate signals, and turning recurring return reasons into low-cost product improvements before deciding whether to enter.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “头部占比超过某倍数即垄断”“集中度阈值”“月销上限”等数值均为来源经验，必须按当前站点与自身资金校准；第三方市场数据是估算，不是平台一方事实。
- “新品占比高等于机会大”是来源推断，需结合价格趋势验证是否为低价内卷。
- 退货率与退货原因来自第三方汇总，样本与时间窗可能与当前不同；决策前用平台可见的退货原因或评论复核。
- 来源关于竞争者动机的判断需要证据（融资、扩张速度、长期定价），不能凭印象定性。

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

1. 先写下自身约束：可用资金、可承接的月销上限与最低利润率、可触达的有门槛货源（本地产业带、非公开货盘）；没有货源优势的候选市场后续只能靠运营细节竞争，其余条件要相应收紧。
2. 用市场筛选工具按三条件初筛：月均销量不超过自身可承接上限、头部若干个 Listing 的销量合计相对市场平均的倍数不过高、商品集中度不超过自设上限；倍数与上限的具体数值按当前站点分布校准，来源经验值仅作参考。
3. 逐个候选市场看销售趋势曲线：明显随开学季、节日等波动的先排除，或只在有库存周转把握时作为备选；曲线平缓的进入下一步。
4. 看排名曲线与新品占比：从头部到尾部销量衰减是否平缓（尾部仍有可观销量说明有进入空间）、近半年上架的新品在前列的比例（比例高说明市场未定型，但要核对是否为低价内卷）。
5. 看价格带与退货率：价格带能否覆盖采购、头程、平台费后仍留目标利润；退货率与退货原因是否指向可低成本改善的痛点（说明书、配件、加固提示等），能改善的加分，“不需要了”类退货不算改善机会。
6. 调研在场竞争者的动机：以盈利为目的的对手通常不打持久价格战，以份额或融资为目的的对手会长期压价；出现后者且有证据时，对小资金卖家的合理决定是退出。
7. 输出 GO/NO-GO 与进入方案：定价以利润率与周转率共同约束，接受单品失败但要求组合整体正现金流；候选连续不达标时回到第一步复核约束与货源，而不是放宽筛选条件。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取细分市场销量分布、趋势、新品占比、价格带与退货率的第三方代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 自身约束与货源优势清单
- 细分市场初筛表（需求、集中度、趋势、新品占比、价格带、退货率）
- 痛点与微改进机会表
- 竞争者动机评估
- GO/NO-GO 结论与进入前提
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
