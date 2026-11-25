---
name: sealeap-yingzhao-amazon-practical-innovation-screen
description: "Screen product ideas discovered through hands-on retail visits and unboxing content by testing whether each innovation adds value without degrading the category's core function, then confirm—before committing—which primary keywords the product can realistically compete on and whether the target buyer can be reached through search. Produces a GO/HOLD/NO-GO memo with the keyword and evidence gaps to fill. Use for 选品思路、不用选品工具怎么选品、创新产品能不能做、这个功能算不算卖点、产品和关键词怎么一起定、新手该不该做小众词产品. Do not use as a replacement for demand, competition and margin validation, and do not use to copy a specific product seen in stores."
---

# Amazon 创新实用性与关键词同步选品

## 目标

Screen product ideas discovered through hands-on retail visits and unboxing content by testing whether each innovation adds value without degrading the category's core function, then confirm—before committing—which primary keywords the product can realistically compete on and whether the target buyer can be reached through search. Produces a GO/HOLD/NO-GO memo with the keyword and evidence gaps to fill.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “不用选品工具、靠产品认知选品”是来源偏好；产品认知与数据工具互补，需求、竞争和利润仍需用数据验证。
- “先选感兴趣的类目、不管竞争大小”只是起点原则，用于保证持续投入与产品理解；进入前仍要做竞争与盈亏评估，不把兴趣当作 GO 的依据。
- 来源举的具体产品与品牌是当时的观察案例，不构成推荐，也不复制；本 Skill 只沿用“创新不得损害基本功能”的判定框架。
- “细分小词太小不值得做”的量级判断随站点、类目与利润结构变化，按当前搜索量估算与目标销量校准，来源说法仅作参考。

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

1. 先定类目：优先选择自己有使用经验、会持续关注的类目，写下相对于“没摸过产品的运营者”你具备的认知优势（材料、用法、人群、痛点）；说不出优势的类目标 NEEDS_EVIDENCE，不因此排除，但后续需要更多外部证据。
2. 收集创新线索：到目标市场品牌的线下门店上手体验产品的材料、结构与手感，观看多平台的开箱与使用视频，把每个让人觉得“这是好卖点”的功能记录为卖点假设，附上观察到的产品类型与场景。
3. 做实用性判定：为每个候选产品列“基本功能清单”（该品类买家默认必须有的功能）和“新增功能清单”，逐项判断创新是否保留了全部基本功能；只加分不减分的进入下一步，为了创新而削弱基本功能的、纯外观花哨不实用的、与常规款无差异的记 NO-GO。
4. 同步确定要打的词：在定品之前列出该产品能竞争的核心搜索词，判断它是品类大词（基本功能完整、可与常规款同台）还是只能打细分小词（功能取舍导致只适合特定人群）；用搜索量与竞争度证据（第三方估算标 ESTIMATE）判断小词是否撑得起目标销量，词与产品一起决定，不先发货再测词。
5. 定义目标人群与触达方式：写明创新点对应的人群（如特定爱好者或桌面/空间受限场景），检查能否通过关键词、类目和广告定位触达；触达路径不清的记 HOLD。
6. 输出结论：GO/HOLD/NO-GO 与理由、卖点假设、核心词清单和待补证据（需求量、竞争、利润测算），把需求与利润验证交给对应的选品与测算流程。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选核心词的搜索量估算与竞争度，以及同类产品评论中对新增功能的反馈，验证卖点假设。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 类目认知优势说明
- 卖点假设清单（来源、功能、场景）
- 实用性判定表（基本功能、新增功能、加分/减分、结论）
- 核心词与目标人群方案（大词/小词判断、证据、触达路径）
- GO/HOLD/NO-GO 备忘与待补证据
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
