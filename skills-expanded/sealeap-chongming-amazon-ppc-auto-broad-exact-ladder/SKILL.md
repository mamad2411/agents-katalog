---
name: sealeap-chongming-amazon-ppc-auto-broad-exact-ladder
description: "Structure Sponsored Products as a three-tier keyword pipeline (auto campaign for discovery, manual broad for testing candidate terms, manual exact for harvested converters) with the break-even ACOS derived from the product's own margin as the promotion and negation rule, weekly search-term migration, and stepwise bid and budget changes read back against account data. Keeps every threshold calibrated to the current account instead of fixed numbers. Use for 新品广告怎么搭、自动广告跑出来的词怎么用、广泛匹配测词、精准匹配收口、否定词标准、竞价怎么起步、预算怎么加. Do not use to change bids, budgets or negatives on a live account without approval, or to apply another account's ACOS threshold."
---

# Amazon PPC 自动到精准三级递进

## 目标

Structure Sponsored Products as a three-tier keyword pipeline (auto campaign for discovery, manual broad for testing candidate terms, manual exact for harvested converters) with the break-even ACOS derived from the product's own margin as the promotion and negation rule, weekly search-term migration, and stepwise bid and budget changes read back against account data. Keeps every threshold calibrated to the current account instead of fixed numbers.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源的盈亏平衡 ACOS 举例、起始竞价区间、建议竞价加价幅度、观察天数与日预算数值均为经验值，本 Skill 不保留；以当前账户毛利率、竞价建议与曝光回读校准。
- “搜索词 ACOS 高于毛利率就否定”需要足够点击样本，否则会误否定；样本不足的词先降价观察而非直接否定。
- 来源不使用词组匹配并认为广泛匹配可覆盖其范围，这是个人偏好；匹配类型的覆盖差异随平台规则变化，按本账户测试数据决定。
- 来源提及用远程桌面在一台电脑管理多个账号，涉及账号关联规避，本 Skill 不采用、不转译。

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

1. 先用官方收益计算器按当前费率与自有采购/头程报价算出单品毛利率；把毛利率作为盈亏平衡 ACOS 上限，并另设一条低于上限的目标 ACOS 作为好词判定线。
2. 启动自动广告前确认 Listing 已有合规渠道获得的基础评论与完整图文；自动广告用较低起始竞价、动态竞价只降低、固定日预算；启动后隔日回读曝光，曝光不足时按小步幅上调竞价直至有稳定曝光。
3. 让自动广告跑满一个观察窗（以积累足够点击为准，不以固定天数为准）后下载搜索词报告；ACOS 高于盈亏平衡线且点击达样本量的搜索词加否定，低于目标 ACOS 且有订单的搜索词记入好词表。
4. 建手动广泛匹配广告作为测词层：词源 = 自动广告好词 + 系统建议词 + 主词表（按搜索量代理数据排序后分批投放）；竞价在建议竞价基础上小幅上浮，每周换一批待测词，同样按报告否定与收集。
5. 建手动精准匹配广告作为收口层：只放已在自动/广泛层验证出单且 ACOS 达标的搜索词，竞价可高于建议竞价并高于测词层；每周把新验证的好词迁入，并在测词层对已迁词加精准否定避免内部竞争。
6. 预算与状态维护：精准层预算随利润按小步幅上调；自动广告在 ACOS 持续高于盈亏平衡线且不再产出新词时暂停，仍在贡献新词且 ACOS 可接受时保留；词组匹配是否加入按本账户测试决定。
7. 每周固定复盘三层各自的花费、订单、ACOS、迁移词数与否定词数；任何竞价/预算/否定变更先写对象、旧值、新值、预期与回退值，待批准后执行并回读。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取关键词搜索量代理数据用于构建并分批投放主词表。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 盈亏平衡 ACOS 与目标 ACOS 计算表（按当前费率）
- 三层广告结构与词源分配表
- 每周搜索词迁移与否定清单
- 竞价/预算变更草案（对象、旧值、新值、回退）
- 三层周复盘记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
