---
name: sealeap-hundun-amazon-launch-review-rank-playbook
description: "Sequence a new listing's launch into review-seeding, rank-building, ad-structuring and assortment-differentiation phases, each with an evidence check and a go/no-go signal, targeting a sub-category rank band and a review-count threshold benchmarked against the current category's own weakest qualifying listings rather than a fixed number. Any cross-listing causal or algorithmic claim stays flagged as an account-level hypothesis pending verification. Use for 新品怎么打爆、新品期目标怎么定、要不要做站外折扣冲评论、新品广告怎么分组、变体怎么做差异化. Do not use to justify review manipulation, paid reviews, or any incentivized-for-positive-review arrangement; do not treat any phase budget or conversion figure below as a fixed rule."
---

# Amazon 新品冲榜与评论积累打法

## 目标

Sequence a new listing's launch into review-seeding, rank-building, ad-structuring and assortment-differentiation phases, each with an evidence check and a go/no-go signal, targeting a sub-category rank band and a review-count threshold benchmarked against the current category's own weakest qualifying listings rather than a fixed number. Any cross-listing causal or algorithmic claim stays flagged as an account-level hypothesis pending verification.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 阶段目标里的具体评论数量、折扣力度、出单速度等均为来源经验值，必须用当前账户所在类目、当前时点的 BSR/新品榜实际数据重新校准，不能直接套用固定数字。
- 站外限时折扣加速排名与评论积累的效果、以及“经过站外折扣的订单索评回复率更高”这一说法，均为账户内观察到的经验，属于待验证假设，不同类目/客群可能表现不同。
- 任何形式的刷单、付费换好评、虚假交易不在本方法适用范围内；本方法仅覆盖真实成交基础上的合规让利与合规索评。
- “一个店铺只聚焦一到两个类目、两三款核心 listing”是来源给出的经验取舍，实际聚焦程度应结合团队精力、供应链掌控力与现金流综合判断，不是绝对规则。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先用同类目 BSR 前列与新品榜中评论数最少的若干条 listing，估算出“进入这个小类需要的评论量门槛”和“目标排名区间”，作为本次新品的阶段性目标，而不是直接对标头部大卖家。
2. 阶段一：善用平台官方的合规索评渠道（如允许卖家赠送样品换取早期评论的官方计划）获取第一批基础评论；若这批评论的平均分明显偏低，先评估产品本身能否改进，改不动就趁早止损换品。
3. 阶段二：如果评估后决定推进，可用不在 listing 页面展示、只在站外渠道发放的限时折扣，配合请求评论动作来加速排名与评论积累；必须持续监测站外折扣的出单速度，连续放不完说明需求不足，应及时停止并更换产品，而不是加大折扣力度硬撑。
4. 阶段三：围绕该 listing 建立自动广告、精准手动广告、低价广泛匹配广告三个广告组的基础结构，把自然转化最好的词补进标题、五点与后台关键词，用关键词覆盖数与自然流量趋势是否持续增长作为是否继续当前打法的判断依据。
5. 阶段四：排名和评论积累到一定程度后再做变体差异化——用一个变体做价格竞争力最强的引流款，用其余变体做正常利润款，并评估哪些变体可自主设计以形成竞争壁垒。
6. 全程执行前先测算所需备货量与预算是否可承受（含索评赠品和折扣损耗），评估不可接受就调低目标节奏或更换风险更低的产品，避免多品类分散精力导致每个 listing 都做不透。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充同类目 BSR 前列与新品榜的评论数量分布等第三方观测数据，用于校准新品进入门槛与目标排名区间。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 类目排名与评论门槛测算表
- 四阶段推进计划（含止损条件）
- 广告组结构记录（自动/精准手动/低价广泛匹配）
- 变体差异化与角色分工表（引流款/利润款）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
