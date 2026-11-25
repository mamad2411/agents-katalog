---
name: sealeap-chongming-amazon-seller-storefront-lead-mining
description: "Mine product opportunities by tracing well-performing organic listings back to their sellers' storefronts, ranking storefront items by estimated revenue and review count, then validating each candidate's main keyword on the search results page for demand versus competition. Uses front-end observation and third-party estimates only, and never contacts or profiles the sellers. Use for 选品没思路、反查卖家店铺、Sold by 找同店产品、杂货铺卖家挖新品、店铺产品按销售额排序、验证一个品能不能做. Do not use to contact or investigate sellers, or to decide sourcing before margin and compliance checks."
---

# Amazon 反查卖家店铺挖选品线索

## 目标

Mine product opportunities by tracing well-performing organic listings back to their sellers' storefronts, ranking storefront items by estimated revenue and review count, then validating each candidate's main keyword on the search results page for demand versus competition. Uses front-end observation and third-party estimates only, and never contacts or profiles the sellers.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源认为海外本土卖家一定有利润、中国卖家可能亏本卖，这无法从前台验证；是否有利润只能靠价格与费用测算，不按卖家所在地判断。
- 第三方插件的销量、销售额与评论数为估算或抓取快照，受时间、变体聚合和个性化影响；写入报告时标为 ESTIMATE 并注明采样时间。
- 来源把“评论数几百到上千”当作竞争过大、“月销几千到上万”当作需求达标，这些是经验数字；以本账户的评论积累速度和可承受的广告投入校准。
- “一个卖家卖得好，其店铺里其他产品也会好”是线索假设而非规律；每个候选仍需独立验证需求、竞争、利润与合规。

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

1. 在目标站点前台以未登录状态、设置目标配送邮编后搜索任意起始词（只作线索，不是目标品）；用第三方插件读取结果页时先隐藏广告位，只看自然结果，并记录采样时间。
2. 按价格带初筛：用当前佣金、FBA 配送费和采购成本粗算，剔除在现有费率下难有毛利的低价带；价格下限按本账户测算校准，不沿用固定数字。
3. 打开自然位表现好的 Listing，通过 Sold by 进入卖家店铺并查看全部商品；只用卖家公开资料判断是品牌店还是多品类杂货店，不联系、不查访卖家。
4. 在店铺内用插件按单 ASIN 月销售额估算降序排列，优先记下两类候选：销售额高而评论数低的；上架不久但已有销量的。多品类杂货店通常能提供更多不同类目的线索，优先展开。
5. 为每个候选提取主关键词（从标题与同类竞品共有词判断），在全部类目下搜索该词，再用插件隐藏广告后读取首页：评论数分布代表竞争强度，估算销量/销售额代表需求；目标是需求中等、头部评论数与新品差距可追的市场，具体阈值以本账户能承受的评论差距与广告投入校准。
6. 排除普通大宗商品（无差异化、首页均为高评论老品）和变体过多、需要备齐大量 SKU 的候选；保留的候选记录：主关键词、首页评论数中位数、估算月销、价格带、来源店铺类型。
7. 在验证页上再取其他表现好的卖家进入下一轮循环；设置停止条件（每轮固定时长或候选数达标）后，把候选交给排除清单与利润测算，不直接进入采购。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取搜索结果页与卖家店铺内产品的估算销量、评论数与价格的第三方代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 起始词与采样条件记录（站点、邮编、时间、是否隐藏广告）
- 卖家店铺线索表（店铺类型、ASIN 销售额排序、评论数）
- 候选产品清单（主关键词、需求/竞争观测、价格带、来源）
- 排除记录（大宗普品、变体过多、价格带过低）
- 下一轮循环起点与停止条件
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
