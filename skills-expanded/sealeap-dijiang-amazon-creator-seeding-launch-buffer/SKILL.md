---
name: sealeap-dijiang-amazon-creator-seeding-launch-buffer
description: "Given a committed product launch, size inbound inventory as a buffer derived from comparable sell-through and total lead time rather than a token pilot batch, benchmark every listing element against top competitors before going live, and seed off-Amazon creator content with paid amplification and per-creator tracking to bring external traffic into the cold-start phase. Use for 新品备货要囤多少、上市前listing要对标什么、怎么用达人内容给新品冷启动引流. Do not use as a substitute for the separate pre-commitment risk screen on compliance, pricing floor, and category saturation — this playbook assumes the go decision is already made."
---

# Amazon 新品上市备货与达人引流

## 目标

Given a committed product launch, size inbound inventory as a buffer derived from comparable sell-through and total lead time rather than a token pilot batch, benchmark every listing element against top competitors before going live, and seed off-Amazon creator content with paid amplification and per-creator tracking to bring external traffic into the cold-start phase.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 备货宁多勿少与先小批量验证需求是两种在不同前提下都成立的策略，选择哪一种取决于需求确定性与资金风险承受度，不应不加区分地照搬其中一种。
- 用评论量区间估算竞品销量、以及外部流量拉动自然排名的因果关系，均为第三方代理指标与来源方推测，不是平台确认的事实，需持续用自身账户数据验证。
- 达人种草与付费助推涉及真实预算投入，规模应按自身实际预算设定，不套用来源中的达人数量或投放金额。
- 本流程假设入场与定价的合规、成本可行性已在更早阶段完成核验，不重复替代那一层的风险自检。

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

1. 用同类目内评论量处于自己预期上市阶段区间的竞品，估算其大致月销水平作为自身预期销量的参照，而非直接采用头部爆款的销量。
2. 按自己实际供应链从下单到入仓的全流程周期，叠加一段用于应对物流延误或入仓排队的缓冲期，再据此设定首批备货量；备货是小批量试水还是一次性较大批量取决于需求确定性与自身资金风险承受度，两种取向各有适用前提，需按自身情况权衡，尤其要意识到一旦上市后因缺货导致断货，积累起来的排名与销量势能通常很难简单恢复。
3. 上线前把主图、图集、加强型内容与文案逐项对照三到五个最直接的竞品，确保每一项都不弱于竞品当前水平，用不了解产品背景的人快速浏览素材，检验能否仅凭图片说出产品是什么、解决什么问题。
4. 结合竞品评论的AI摘要梳理竞品的共性差评与共性好评，在自己的文案与素材中主动规避已知差评点、覆盖已知好评点，并突出至少一个竞品普遍不具备的差异点。
5. 起始定价可参考同价格带竞品的下沿区间设置，以弥补新品零评论带来的信任劣势，后续再按定价与转化测试流程逐步向目标利润率靠拢。
6. 有条件的情况下提前联系一批达人在上市当天集中发布产品体验内容，并对这批内容做统一的付费流量助推，为每个达人内容配置独立的追踪链接或编码以区分各自带来的效果，这类站外流量的核心作用是在评论积累之前提前建立社会认可度，而非直接期待站外平台本身产生大量成交。
7. 上市后持续观察站外引流是否伴随自然排名的提升，把这一相关性记录为账户内观测证据，不对外断言平台算法一定会因为承接站外流量而额外加权，这是尚待验证的假设。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：批量获取竞品评论摘要与销量区间估算，为备货规模与差异化卖点提供交叉验证证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 竞品销量区间估算与备货计划
- 上市前竞品对标核对表（主图/图集/加强型内容/文案）
- 差异化卖点与差评规避清单
- 达人种草与付费助推执行及追踪记录
- 站外流量与自然排名相关性观察记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
