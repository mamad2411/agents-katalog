---
name: sealeap-yingzhao-amazon-conversion-gated-ppc-launch
description: "Gate manual Sponsored Products keyword campaigns on a new listing behind conversion evidence—business-report conversion rate, review and Q&A readiness and an anonymized side-by-side buyer test against competitors—then start with a small pool of exact-match keywords and keep or pause each keyword by comparing its conversion rate with the listing's own baseline. Auto and broad campaigns are treated as optional discovery channels rather than defaults. Use for 新品要不要先开广告、转化率不行先别开手动广告、怎么判断产品转化率够不够、前期打几个词、精准还是广泛、哪些词该留哪些该关、新品 ACOS 高要不要停、广告没点击怎么办. Do not use to launch, pause or re-bid live campaigns without approval, and do not use for mature listings with established keyword history."
---

# Amazon 新品转化先行的手动广告起步

## 目标

Gate manual Sponsored Products keyword campaigns on a new listing behind conversion evidence—business-report conversion rate, review and Q&A readiness and an anonymized side-by-side buyer test against competitors—then start with a small pool of exact-match keywords and keep or pause each keyword by comparing its conversion rate with the listing's own baseline. Auto and broad campaigns are treated as optional discovery channels rather than defaults.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “转化差会让建议竞价走高、曝光走低，要救回来必须大幅提价”是来源对竞价机制的解释，属待验证假设；用当前账户的曝光、CPC 与建议竞价曲线观察，不当作平台规则。
- “几类关键词工具能覆盖绝大多数出单词，所以自动广告没必要开”是来源经验；自动广告作为词发现与商品投放渠道的价值按当前账户数据校准，工具产出的词与流量估算一律标为 ESTIMATE。
- 来源的样本与阈值（多少次点击不出单即关词、词级转化率与整体转化率的比较）需按当前账户的点击量、类目转化水平与盈亏平衡 ACOS 校准，来源经验值仅作参考；“让平台认为产品在任何词上都高转化从而提升自然流量”是算法假设，不外推。
- “做了站外之后广告才有点击”是来源观察，属待验证假设；站外只采用合规促销渠道，服务商“不出单退款”属其商业承诺而非决策依据，任何刷单、操纵评论或诱导点击的做法不采用。

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

1. 先核对产品与 Listing 的转化基础：从业务报告取订单数 ÷ Session 得到 Listing 整体转化率（自选并记录时间窗），同时清点评论数、Q&A、视频、图片和文案本地化程度；转化基础未成型时不开手动关键词广告，先补齐这些项。
2. 做匿名对比测试：把自家 Listing 与几款可比竞品整理成同一格式的对比表（标题与五点译成中文、主图与 A+ 截图、价格、评论数与评分），不标注哪一个是自家，让若干不知情的人选出会购买的一款并说明理由；自家反复垫底时记 HOLD，回到产品或 Listing 改进，而不是靠广告硬推。
3. 转化未验证但需要流量时，只用低风险方式试水：商品定位（ASIN/类目投放）或低竞价的自动广告，记录曝光、点击与订单作为基线；这一步的目的是观察而非放量。
4. 转化通过后建词池：合并竞品出单词反查、词根组合扩展、前台搜索框下拉长尾词以及自家独有功能词；去重和相关性筛选后只保留少数核心词，以精准匹配起步；广泛/词组只在对产品不熟悉、需要发现词时使用，并配合搜索词报告否定不相关词。
5. 按词做留关判断：每个词累计到足够点击（按账户点击量与转化率设定样本线）后，比较词级转化率与第 1 步的 Listing 整体转化率，不低于基线的保留，明显低于且样本充分的暂停；样本不足的继续观察，不因个位数点击做结论。
6. 前期容忍高 ACOS 但不容忍低转化：转化达标而 ACOS 偏高的词继续投放，跟踪 CPC 与建议竞价的趋势；只有在核心词排名与转化稳定后再逐步加入新词，每次改动记录对象、旧值、新值与观察窗。
7. 竞价已足够却几乎没有点击时，先复核关键词相关性、主图与价格，再考虑合规的站外促销作为激活手段：把站外单位成本与广告单位点击成本对比，设定预算上限与停止线，并把站外期间的数据与广告数据分开记录。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品出单词反查、关键词扩展与搜索下拉长尾词作为词池输入。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 转化基础核对表（整体转化率、时间窗、评论/Q&A/视频/本地化完成度）
- 匿名对比测试记录（对比表、参与者选择与理由、HOLD/GO 结论）
- 核心词池与匹配类型草案（词来源、筛选依据、起始竞价范围）
- 词级留关判断表（点击、订单、词级转化率、基线、动作与样本状态）
- 改动日志与站外激活方案（对象、旧值、新值、预算上限、停止线）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
