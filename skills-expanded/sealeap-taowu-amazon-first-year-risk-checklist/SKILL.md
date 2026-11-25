---
name: sealeap-taowu-amazon-first-year-risk-checklist
description: "Run a pre-order risk check for a new private-label seller: validate demand with estimated-sales evidence, size the first order conservatively from comparable-listing velocity, reserve an advertising budget inside the margin model, and screen the listing and backend keywords for third-party trademarks. Outputs a go/hold decision with the evidence behind each gate. Use for 新卖家避坑、第一批货订多少、新品要不要先投广告、Listing 能不能写别人的品牌词、后台关键词商标风险、首年常见错误. Do not use as a legal trademark clearance opinion or as a substitute for a full product-selection study."
---

# Amazon 新卖家首年风险自检

## 目标

Run a pre-order risk check for a new private-label seller: validate demand with estimated-sales evidence, size the first order conservatively from comparable-listing velocity, reserve an advertising budget inside the margin model, and screen the listing and backend keywords for third-party trademarks. Outputs a go/hold decision with the evidence behind each gate.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源用“可比竞品估算月销的一半”定首月预期、“首单为月销两倍”等比例，是个人经验值；按当前品类季节性、资金和仓储成本校准，来源比例仅作参考。
- 第三方销量估算是估算，不同工具口径不同；用于排序与量级判断，不作为一方事实写进决策。
- “新品不打广告就卖不动”是经验判断而非平台规则；广告依赖度按当前品类的广告占比与自然流量证据评估。
- 商标检索只是初筛，查不到不等于没有；涉及仿制外观或功能的产品还要另做专利与外观权初筛，必要时咨询专业人士。

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

1. 先做需求验证：用第三方销量估算与可比 Listing 的评论增速、价格带交叉核对，估算值标为 ESTIMATE；只有个人偏好、没有需求证据的候选品直接 HOLD。
2. 评估 Listing 质量基线：主图、标题、卖点是否达到同类目在售水平；Listing 未成型前不下大单，因为转化差会把库存问题放大。
3. 定首单数量：以一款可比竞品的估算月销为锚，乘以保守折扣作为首月预期，并按资金、仓储费和滞销清仓成本设上限；不确定时先用小批量测款，首周动销验证后再追加正式订单。
4. 把广告预算写进利润模型：新品在缺少评论和自然排名时通常需要 PPC 起量，用目标 ACOS 与预计广告占比反推售价和毛利是否仍成立，不成立则重新选品或定价。
5. 商标排查：逐项检查标题、五点、描述、后台关键词和图片中是否出现任何第三方品牌名、产品线名或标志（包括“兼容/仿/同款”式表述）；先用商标数据库与搜索初筛，再决定是否保留；已出现的立即移除并记录。
6. 形成下单前的四闸结论（需求、数量、广告预算、IP）：任一闸未过写 HOLD 并列出补证据动作；全部通过再向供应商确认订单。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取可比 Listing 的估算销量、评论与价格证据，以及品牌词/商标的公开检索结果。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 需求验证证据表（估算销量、可比 Listing、口径与限制）
- 首单数量测算与上限（锚点、折扣、资金与滞销约束）
- 含广告预算的利润模型草案
- 商标与品牌词排查记录（检查位置、发现项、处理动作）
- 下单前四闸结论（GO/HOLD 与待补证据）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
