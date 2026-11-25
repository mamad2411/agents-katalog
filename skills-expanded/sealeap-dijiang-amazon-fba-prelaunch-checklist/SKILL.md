---
name: sealeap-dijiang-amazon-fba-prelaunch-checklist
description: "Run a pre-launch self-audit across policy compliance, price-floor economics, competitive saturation, and inventory commitment before funding a new Amazon product, using account and category evidence rather than fixed thresholds copied from any single source. Use for 新品上架前自检、定价是否太低、竞争是否太激烈、囤货风险评估、要不要放弃这个品. Do not use as a substitute for reading Amazon's current Seller Policies and Code of Conduct directly."
---

# Amazon 新品上架前风险自检

## 目标

Run a pre-launch self-audit across policy compliance, price-floor economics, competitive saturation, and inventory commitment before funding a new Amazon product, using account and category evidence rather than fixed thresholds copied from any single source.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “定价不低于某固定金额”“成本利润三等分”均为来源经验总结的启发式规则，不是平台规律，必须用当前费率与目标利润重新测算。
- 用评论数量与第三方销量/搜索量工具判断竞争度和需求，属于估算/代理指标，不是 Amazon 一方真实成交数据，工具间口径可能不一致，需保留各自数据源并列，不取平均。
- 品类是否已被“大品牌垄断”属于主观判断，需结合具体品类的实际竞争结构复核，不能仅凭品牌知名度一概而论。
- 长期坚持与止损是两种相反的建议，需结合前序证据（是否已验证需求、是否仍在可承受的资金与时间预算内）做具体判断，不应机械地套用任一方向。

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

1. 逐条对照 Amazon 当前的卖家协议与政策（尤其评论获取方式、禁止诱导好评、禁止操纵排名的条款），凡是计划中的推广动作触碰这些条款的，一律先排除，不因“别人也这样做”而侥幸尝试。
2. 用当前平台费率结构（成交费、履约费、仓储费等）反推目标定价下限：只有当预估售价扣除全部平台与物流成本后仍留有要求的最低利润空间时才继续，不套用某个固定金额作为“安全定价线”。
3. 参考“成本/平台与履约费用/利润”三分启发式做粗算，作为快速筛掉明显不划算品类的第一道关卡，再用真实报价与费率表做精算复核，不以粗算结果直接下单。
4. 抽样统计目标品类搜索结果页前列一批竞品的评论数量分布，判断是否被知名品牌把持：评论断层过大或被强势品牌垄断的品类判定为高风险，评论过少、搜索量也低的品类判定为低需求风险；用第三方销量/搜索量代理数据交叉验证，不单看评论数。
5. 首批备货量按“先小批量验证需求，再逐步放量”的节奏设定，避免在没有实际动销数据前就压满仓；同时预估长期仓储费触发时间点，作为若滞销需要促销清仓的止损时间线。
6. 把学习投入（课程/工具/社群等）控制在验证产品可行性所需的最小范围内，优先使用官方帮助文档与免费公开资料完成第一轮判断，避免在验证产品之前先过度投入沉没成本。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 政策合规自检清单
- 定价与费率测算表
- 竞争与需求分级判断
- 首批备货与止损时间线
- 学习/工具投入预算上限
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
