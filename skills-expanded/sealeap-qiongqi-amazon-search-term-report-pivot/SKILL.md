---
name: sealeap-qiongqi-amazon-search-term-report-pivot
description: "Turn the Amazon Sponsored Products search term report into product-level pivot views that surface high-value search terms and ASIN targets, zero-sale spend leaks, and concrete negation or scale-up actions. Use for 搜索词报告怎么看、哪些词该否定、广告费花在哪了、竞品 ASIN 投放要不要加码、零转化词处理. Do not use to apply negations or bid changes without an approved action list."
---

# Amazon 搜索词报告透视分析与动作清单

## 目标

Turn the Amazon Sponsored Products search term report into product-level pivot views that surface high-value search terms and ASIN targets, zero-sale spend leaks, and concrete negation or scale-up actions.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 『SP 搜索词数据是 SB/SD 投放的主要信息源』是来源经验，SB/SD 受创意影响更大，跨类型迁移目标前先小预算验证。
- 预期出单点击数取决于平均转化率的稳定性；新品与样本过小的词不要因短期无单就否定，先标记观察。
- 零转化的竞品 ASIN 可能是对方价格或功能更优，否定前记录原因，避免误伤后续促销期可能转化的目标。
- 来源提到的 ACOS 数值与窗口天数仅为示例，以当前账户盈亏平衡 ACOS 与样本量校准。

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

1. 在广告控制台的报表中心创建 SP 搜索词报告（汇总口径）；销量低取报表可用的最长窗口，销量高取较短的近期窗口以保证时效，导出后导入电子表格。
2. 先确认账户组织方式：理想是一产品一 Portfolio、该产品全部活动归入；账户混乱时也能分析，但结论只能按活动层解释，并记为限制。
3. 区分『投放目标』与『客户搜索词』两列：广泛/词组匹配会展示到大量相关搜索，精确匹配也可能展示到近似词；搜索词列出现 ASIN 的行是商品页广告而非搜索，需按 ASIN 反查对应商品。
4. 建数据透视表：行=客户搜索词（必要时加 Portfolio/产品维度），值=曝光、点击、花费、销售额、订单，派生 ACOS 与转化率；聚合后同一搜索词跨活动只出现一次，避免重复计数。
5. 按销售额降序逐行看头部：ACOS 低于目标的竞品品牌词或 ASIN 目标，考虑在 SP 商品定位、SB、SD 上同步加投；每条动作附证据行，直到销售额低到不值得逐条分析为止。
6. 筛出零销售额行按花费降序：用该产品平均转化率折算『预期出一单所需点击数』，点击已明显超过预期仍无单的词判定为不匹配，按不匹配成分做词组否定或精确否定；花费高无单的竞品 ASIN 改为否定商品定位或移除。
7. 输出动作清单（否定/加投/移除，各附证据行），获批后执行并在下一轮报表核验效果。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 搜索词透视表
- 高价值搜索词与 ASIN 目标清单
- 零转化浪费清单
- 否定与加投动作表
- 执行后核验记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
