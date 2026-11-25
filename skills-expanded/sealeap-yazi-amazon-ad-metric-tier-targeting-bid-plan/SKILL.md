---
name: sealeap-yazi-amazon-ad-metric-tier-targeting-bid-plan
description: "Diagnose Sponsored Products/Brands/Display performance through a layered metric model (exposure-click-spend-order, cost, conversion-efficiency and share-of-total layers), determine the current advertising objective for the listing's lifecycle stage, then build a keyword/ASIN targeting list from relevance-volume quadrants and back-calculate bid and budget from the account's own margin data. Every formula input is treated as an account-specific variable rather than a fixed constant. Use for 广告指标一堆看不懂怎么理清、ACOS 高是不是广告不好、该投关键词还是投 ASIN、竞价怎么定、新品和老品预算怎么分配、标品和非标品广告架构怎么搭. Do not use to justify high ACOS or a large new-listing budget without lifecycle and margin evidence, and do not use to copy a category CPC benchmark as a bid without checking current auction data."
---

# Amazon 广告分层诊断与选词定竞价

## 目标

Diagnose Sponsored Products/Brands/Display performance through a layered metric model (exposure-click-spend-order, cost, conversion-efficiency and share-of-total layers), determine the current advertising objective for the listing's lifecycle stage, then build a keyword/ASIN targeting list from relevance-volume quadrants and back-calculate bid and budget from the account's own margin data. Every formula input is treated as an account-specific variable rather than a fixed constant.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的相关性判定占比、点击率提升幅度、CPC 参考区间等均为经验观察或特定品类样本，需按自身账户与品类重新校准，不作为通用阈值直接使用。
- 竞价公式按目标 ACOS 反推 CPC 假设转化率与客单价保持稳定，实际会随广告位、素材与季节波动，公式结果只作为起始竞价，需要用实际点击与转化数据持续修正。
- 预算按毛利润或销售额比例分配的具体区间是经验参考，不同品类、客单价与竞争强度下应有不同区间，需以账户自身盈亏平衡点作为分配依据。
- 广告订单占比的合理区间因标品/非标品和品类而异，不能脱离账户历史数据直接套用来源给出的区间。

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

1. 先按基础指标（曝光/点击/花费/订单）到成本指标（CPC/CPA）到转化效率指标（CTR/广告转化率/ACOS）到占比指标（广告订单占比/TACOS）逐层核对，定位问题出现在漏斗的哪一层，而不是只看 ACOS 一个数字下结论。
2. 结合链接所处阶段判断当前广告目标（推排名、拓词拓流、提升关联流量、盈利、扩流放量五类中的哪一类或组合），推排名阶段允许 ACOS 阶段性偏高，但需有自然排名或自然流量同步改善的证据支撑，否则回到问题排查。
3. 构建关键词库：从若干同赛道表现较好的竞品 ASIN 反查流量词，按自然结果中同赛道商品占比判定相关性强弱，再用相关性与流量大小画四象限，优先选流量大且相关性强的词，预算有限时选流量小但相关性强的词起量。
4. 构建 ASIN 定投清单：合并外观或功能相似的竞品 ASIN、自身广告报告中表现好的 ASIN、通过购买行为报告发现的交叉销售 ASIN 三类来源，按各自转化数据决定分组密度。
5. 定竞价时按数据可得性和目标选择方法：能接受快速试错就用平台建议值上浮测试；预算有限就用建议值小幅递增并观察数天一调；需要控制盈利就用目标 ACOS 反推 CPC；有长期品类经验则参考自身历史成交 CPC 区间，四种方法互相校验而非只用一种。
6. 分标品与非标品设置不同预算结构：标品把多数预算集中到高相关性核心词以推排名，非标品把多数预算分散到自动广告、广泛匹配与再营销以扩大流量入口；新品按目标出单量倒推预算，老品按现有毛利或销售额比例设定预算上限。
7. 每轮调整后回读 TACOS 与 ACOS、广告订单占比的联动变化：TACOS 过高时先判断是 ACOS 高还是广告订单占比高，分别对症调整竞价或自然流量建设，而不是笼统加大或砍掉预算。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品 ASIN 的公开流量词反查结果与外观相似匹配，补充关键词库与定投清单的第三方证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 广告指标分层诊断表（基础/成本/转化效率/占比四层）
- 广告目标判定记录（推排名/拓流/关联/盈利/扩量）
- 关键词象限分类与预算倾斜草案
- ASIN 定投清单（按来源分类）
- 竞价与预算测算表（含账户自身校准依据）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
