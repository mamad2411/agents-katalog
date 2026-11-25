---
name: sealeap-luduan-amazon-eu-scale-product-screen
description: "Screen a high-volume Amazon EU category for mid-to-large sellers by estimating competitor daily sales from review velocity, checking growth trend, unit margin after marketing and return allowances, compliance certification, breakage and after-sales exposure, and competitor aggression, then issue a GO/HOLD decision with the evidence behind each factor. Does not replace supplier sampling or a formal compliance review. Use for 欧洲站选品怎么看体量、评价增速反推销量、大卖选品逻辑、类目容量增长趋势、带电产品欧洲合规风险、选品前问同行. Do not use for small-seller niche entry decisions or as a substitute for product testing and certification."
---

# Amazon 欧洲站中大卖选品体量与风险核查

## 目标

Screen a high-volume Amazon EU category for mid-to-large sellers by estimating competitor daily sales from review velocity, checking growth trend, unit margin after marketing and return allowances, compliance certification, breakage and after-sales exposure, and competitor aggression, then issue a GO/HOLD decision with the evidence behind each factor. Does not replace supplier sampling or a formal compliance review.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源用固定留评率倍数把评价增速换算成订单，这是粗估，不同类目与时期的留评率差异很大；结论必须标 ESTIMATE 并用第二来源交叉验证。
- 来源给出的采购价档位、利润率、营销占比与退货比例是特定时点的案例数字，本 Skill 不保留；一律按当前报价与账户数据重算。
- 来源承认该案例最终因续航与售后问题不推荐，本 Skill 把“数据面看好但实物有已知缺陷”作为典型失败模式，要求上线前完成样品测试与同行问询。
- 来源提到竞争对手可能通过刷差评或恶意投诉打压新进入者，这只作为风险提示；本 Skill 不采用任何测评操纵或投诉对抗手段。

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

1. 先定卖家体量与决策口径：可投入资金、可承受的竞争强度、目标利润率与目标站点；中大卖的优先级是类目容量与增长趋势、做到头部后的整体利润，而不是避开竞争。
2. 找容量证据：选取类目内若干代表性 Listing，按固定间隔记录评价总数变化，用日均新增评价乘以留评率假设换算日销；留评率倍数以当前类目校准，来源使用的固定倍数仅作参考，并用第三方销量估算或前台可见数据交叉验证。
3. 看增长而不是绝对量：比较不同上线时长 Listing 的评价增长曲线是否自然、近期是否加速；把日销换算成日销售额时使用当前站点的客单价区间。
4. 做单位经济：采购价按能保证质量的档位报价（低价档位的质量风险计入）、头程与 FBA 费用、平台佣金、营销费用占比按高竞争类目上浮、退货与不可售库存处置比例单独预留；营销与退货比例以当前账户校准，来源经验值仅作参考。
5. 合规与售后核查：带电类产品在欧洲站需要的认证与责任人要求、包装防破损设计、退货后不可售库存在海外的处置成本；任一项无解先记 HOLD。
6. 选品前做外部验证：把产品交给做过该类目的同行或供应商看电池寿命、故障率、售后投诉等已知问题；除非产品高度新颖需要保密，否则不只看数据面。
7. 竞争风险评估：记录类目内是否存在恶意差评、投诉下架、跨站点改 Listing 等对抗行为的迹象，评估团队是否有应对能力；输出 GO/HOLD 与理由，并标出待补证据。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取类目内代表性 Listing 的评价数量变化、销量估算与评论中的质量问题，作为容量与风险核查的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 类目容量与增长证据表（评价增速、换算假设、交叉验证）
- 单位经济测算（含营销、退货与不可售处置预留）
- 合规与售后核查清单
- 同行/供应商问询记录
- GO/HOLD 结论与待补证据
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
