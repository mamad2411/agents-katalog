---
name: sealeap-hundun-amazon-factory-sourcing-playbook
description: "Sequence supplier discovery for an individual or small-team seller from broad online factory mapping, to phone screening, to selective on-site visits, to trade-show and community sourcing, so higher-cost verification steps such as travel and on-site audits are reserved for suppliers that already passed cheaper screening. Generic sourcing workflow; does not endorse any specific platform or supplier as authoritative. Use for 怎么找工厂、怎么搭建供应链、要不要去看厂、去展会有什么用、怎么加入供应商群. Do not use as a substitute for factory audits, quality agreements, or contractual due diligence once a supplier is selected."
---

# Amazon 个体卖家供应链搭建方法

## 目标

Sequence supplier discovery for an individual or small-team seller from broad online factory mapping, to phone screening, to selective on-site visits, to trade-show and community sourcing, so higher-cost verification steps such as travel and on-site audits are reserved for suppliers that already passed cheaper screening. Generic sourcing workflow; does not endorse any specific platform or supplier as authoritative.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 现场拜访前的电话/线上筛选标准应结合自身产品的品质与合规要求细化，“态度好、产品线契合”等判断标准较为主观，需要补充可验证的量化指标。
- 展会与群组渠道获取的信息真实性参差不齐，只作为线索来源使用，正式合作前仍需走完整的资质与样品验证流程。
- 供应商的产能、起订量、生产周期等描述以实地或书面确认为准，口头沟通内容不能直接作为合同条款依据。

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

1. 先在一个覆盖面足够广的批发/工厂直供平台上，针对目标产品做穷尽式摸底：列出尽可能多的相关工厂，记录各家所在地区、产品线覆盖范围和相对优势，做横向对比而不是只看排名靠前的少数几家。
2. 电话/在线沟通筛选：在决定是否值得线下拜访之前，先通过沟通判断对方的服务态度、产品质量描述、配合度是否与自身产品需求匹配，筛掉明显不匹配或响应差的供应商。
3. 对通过筛选、匹配度高的供应商再安排实地拜访，重点了解其生产线优劣势、真实产能、起订量、人员规模，为后续可能的团队扩张和产能保障做准备；线下拜访成本较高，只对已筛选出的候选执行。
4. 视资源情况参加行业展会：展会能在短时间内接触大量工厂、看到尚未上线的新品、感知行业趋势与需求变化，适合用来发现前两步摸底摸不到的新方向。
5. 加入行业相关的从业者群组，适度发布自己的选品/供货需求，从群内推荐获取补充线索；作为前几种方式之外的辅助渠道，不作为主要验证手段。
6. 把以上几步得到的候选供应商按响应速度、报价、起订量、产能与实地考察结果汇总对比，再进入正式合作与打样验证阶段。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充候选工厂/供应商在公开渠道的展示信息与联系方式，用于扩大初筛候选池。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 候选工厂横向对比表
- 电话筛选记录与评分
- 实地拜访纪要（产能/起订量/人员规模）
- 供应商候选池汇总
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
