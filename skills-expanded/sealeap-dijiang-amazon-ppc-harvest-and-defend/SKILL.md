---
name: sealeap-dijiang-amazon-ppc-harvest-and-defend
description: "Run two complementary PPC structures on Amazon: a low-bid automatic campaign with placement modifiers to cheaply harvest converting search terms, and a manual campaign built from a reverse-ASIN lookup of the listing's currently-ranking keywords to reinforce organic rank, mining and negating terms between the two over time. Use for 广告结构怎么搭、自动广告怎么用来挖词、怎么反查自己已经在排的关键词、acos太高怎么优化结构. Do not use fixed bid or budget numbers from any external source as targets — calibrate every value against the account's own CPC and break-even ACOS."
---

# Amazon 捡漏反查双轨PPC结构

## 目标

Run two complementary PPC structures on Amazon: a low-bid automatic campaign with placement modifiers to cheaply harvest converting search terms, and a manual campaign built from a reverse-ASIN lookup of the listing's currently-ranking keywords to reinforce organic rank, mining and negating terms between the two over time.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 具体出价分值、广告位加价百分比与每日预算金额均为来源示例，不构成任何跨账户通用的基准，必须用当前账户的实际 CPC、转化率与目标 ACOS 重新测算。
- “广告出单会提升自然排名”是行业内被广泛采信但未经平台官方证实的因果假设，只能作为待验证假设，观察窗口要控制价格、促销、库存等变量，避免把其他因素造成的排名变化误记为广告效果。
- 自动广告与反查关键词工具给出的匹配结果分别代表平台侧词语相关性判断和第三方对自然排名的估算，两者口径不同，不应直接相加或互相替代验证。
- 双轨结构会同时消耗预算，若账户整体广告预算有限，需要先设定两条广告的资源分配优先级，而不是同时不设上限地跑满。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 新建一个覆盖全部在售商品的自动定向广告活动，出价从账户当前可承受的最低起始价位开始（不套用他人给出的固定分值），先以“花小钱换取平台自行匹配的长尾词表现数据”为目的，而不是追求短期起量。
2. 在该自动广告的竞价策略里加入按广告位的动态调价（首页顶部、商品页等位置可适度上调），上调幅度从一个较小的比例开始测试，观察是否明显推高花费而不带来相应转化，再决定是否继续放大。
3. 运行一段可判断出趋势的周期后拉取该广告的搜索词报告，把确认有转化的词挑出来，迁移到独立的手动广告活动里精细化出价管理；对花费高但从未转化的词加入否定关键词，防止持续无效消耗。
4. 另建一条广度覆盖思路不同的广告：先用反查自身 ASIN 的关键词工具，找出当前listing已经在自然结果里有一定排名或表现的关键词清单，把这些词整理为该新广告活动的定向关键词来源，而不是凭空猜测。
5. 用这条反查得来的关键词建手动广告活动，目的是对“已经有一定自然排名基础”的词加大曝光与转化密度，帮助进一步稳固或提升这些词的排名，而不是像第一条广告那样以发现新词为目的。
6. 每条广告活动的每日预算设置到“能产生足够点击量以获得可判断的数据样本”这一水平即可，不必对标他人公布的具体预算数字，预算是否合理以“该广告是否能在合理周期内跑出可解读的搜索词/转化数据”为验证标准。
7. 定期（如按周或按可判断趋势的周期）复盘两条广告线的花费、转化与是否推动了自然排名变化，只把“广告过程中观察到的自然位置变化”记为账户内证据，不对外宣称这是平台排名算法的确定规律。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：需要反查自身 ASIN 当前排名关键词时，可用关键词类数据连接器获取该 ASIN 的关键词表现估算，作为构建第二条广告活动的关键词来源，仅作代理证据使用。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 自动广告捡漏搭建记录（含广告位加价设置）
- 搜索词报告与迁移/否定决策记录
- 自身ASIN反查关键词清单
- 反查词手动广告搭建记录
- 双轨周期复盘结论（费用/转化/排名观察）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
