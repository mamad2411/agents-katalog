---
name: sealeap-bifang-amazon-ad-rank-conversion-balance
description: "Find the search-result position where an Amazon Sponsored Products keyword converts best per unit cost by logging position, click-through, conversion and bid over time, comparing the listing with its on-page neighbours before pushing rank, and only then configuring rule-based rank holding with a target range, bid step, bid ceiling, decay after success and dayparting, all bounded by profit. Use for 广告位置越靠前越好吗、卡位怎么设、排名上去转化下降、竞价该加还是减、关键词排名监控、卡位工具参数. Do not use to authorise third-party tools on a live account or to raise bids beyond the profit ceiling without approval."
---

# Amazon 广告位置与转化率平衡卡位

## 目标

Find the search-result position where an Amazon Sponsored Products keyword converts best per unit cost by logging position, click-through, conversion and bid over time, comparing the listing with its on-page neighbours before pushing rank, and only then configuring rule-based rank holding with a target range, bid step, bid ceiling, decay after success and dayparting, all bounded by profit.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “多数搜索流量集中在前几页”是来源引用的行业说法，作为假设；对本品有效的位置区间只能靠账户内观测表得出。
- “平台会过滤恶意点击”“展示免费仅点击计费”等是来源对广告系统的描述，以当前官方广告政策与计费说明为准。
- 卡位工具的监控频率、加价步长与词数额度是特定工具的能力，参数与费用随工具变化；把店铺与广告 API 授权给第三方存在数据与权限风险，需先评估。
- “中小卖家先求转化再求排名、不急于品牌化”是来源的经营取向而非规则；按自身目标决定。

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

1. 准入：确认页面、主图、价格、评论与同页竞品处于可比水平；若明显落后，先优化页面而不是花钱推位置。
2. 建立观测表：对每个重点词按固定采样时间记录广告位置（页/位）、曝光、点击率、转化率、CPC 与当时的竞价；至少覆盖一个完整的调整周期，样本不足不做结论。
3. 判定位置价值：比较不同位置区间的转化率与单位订单成本，找出转化率高且成本可接受的位置区间；不预设首页顶部最优，前几页内各位置都可能是平衡点。
4. 回退规则：位置上升后点击率或转化率下降，说明相邻竞品在价格、图片或评论上更优——先小幅下调竞价回到原区间，同时把差距记入页面优化清单；只有销量与评论积累后再小幅试探更高位置。
5. 自动化卡位：在人工验证过平衡区间后，用规则化的排名卡位设置——目标位置区间、每次加价步长、最高竞价上限（由盈亏平衡 ACOS 推导）、卡位成功后的逐步降价比例、按转化时段设定卡位时段；未卡位时段保留末次竞价或固定值。
6. 运行监控与停止：按周查看卡位词的位置稳定性、ACOS 与利润；连续触及最高竞价仍未达目标区间、或利润转负时停止该词卡位并回到人工观测；任何第三方工具授权只给必要权限并记录。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取关键词自然位与广告位的排名抓取代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 位置-点击率-转化率-竞价观测表
- 平衡位置区间判定与理由
- 页面差距优化清单
- 卡位规则参数表（目标区间、步长、上限、降价比例、时段）
- 周度监控与停止记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
