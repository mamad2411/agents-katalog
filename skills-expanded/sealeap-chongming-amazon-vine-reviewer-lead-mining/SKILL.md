---
name: sealeap-chongming-amazon-vine-reviewer-lead-mining
description: "Discover recently launched products by starting from a low-review listing, locating its Vine reviews, opening those reviewers' public profiles to list other Vine-reviewed items, and looping across products and reviewers to build a candidate pool that is then validated on each main keyword's search results page. Treats Vine presence as a launch-investment signal, not as proof of demand. Use for Vine 评论反查选品、找刚上架的新品、评论者主页看他评测了什么、新品线索池、少评论产品怎么验证市场. Do not use to contact reviewers, solicit reviews, or skip demand, margin and compliance validation."
---

# Amazon Vine 评论者反查新品线索

## 目标

Discover recently launched products by starting from a low-review listing, locating its Vine reviews, opening those reviewers' public profiles to list other Vine-reviewed items, and looping across products and reviewers to build a candidate pool that is then validated on each main keyword's search results page. Treats Vine presence as a launch-investment signal, not as proof of demand.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源假设“用 Vine 的卖家对产品质量有信心”；可验证的事实只是该卖家已完成品牌备案并为新品投入了 Vine，质量与需求仍需独立判断。
- 评论者主页的可见范围与 Vine 标识的展示方式由平台决定，可能变化或受限；无法获取时记录缺口，不用抓取工具绕过。
- 候选来自他人新品，不等于市场已验证；“别人替你测过”只是假设，需求与竞争以主关键词首页观测和第三方估算（标为 ESTIMATE）为准。
- 本 Skill 只读取公开评论与主页信息，不联系评论者、不索评、不采用任何评论操纵手段。

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

1. 选一个评论数较少（便于定位 Vine 评论）的新上架 Listing 作为起点，进入其评论列表，找到带 Vine 标识的评论；记录产品、评论日期与评分分布。
2. 打开 Vine 评论者的公开主页，列出其近期评测的其他产品（Vine 评测通常对应刚上架的新品）；逐个记下产品主关键词、当前评论数、是否在售、评分；已停售的只作类目线索。
3. 对每个新发现的产品重复第 1–2 步（找它的其他 Vine 评论者→更多产品），形成“产品→评论者→产品”的循环；给每轮设固定时长或候选数上限，避免无限展开。
4. 把候选按“新上架且已有销量迹象、评论少、评分不差”排序，并从评论正文归纳买家看重的属性与抱怨点，作为后续差异化输入。
5. 对每个候选提取主关键词，在全部类目下搜索，用第三方插件隐藏广告后读取自然结果首页：评论数分布（竞争）与估算销量/销售额（需求）；入选门槛以本账户可承受的评论差距与广告投入校准。
6. 入选候选进入排除清单与利润/合规测算；未通过的记录原因；每轮结束汇总新增候选、来源链路与采样时间。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选产品的估算销量、评论数与关键词首页供给情况的第三方代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- Vine 评论者反查链路记录（起点产品、评论者、发现产品）
- 新品候选池（主关键词、评论数、评分、在售状态）
- 主关键词首页需求/竞争观测表
- 买家看重属性与抱怨点摘要
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
