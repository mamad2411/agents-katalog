---
name: sealeap-fenghuang-amazon-prelaunch-audience-launch
description: "Plan a compliant pre-launch audience build for a new Amazon product (US marketplace by default)—social following, email list, private community, creator seeding, live shopping—and combine it with launch-week PPC and truthful persuasion cues (scarcity, social proof, authority) while excluding any incentivized-review tactic. Use for 新品怎么首发、站外引流、上架前预热、邮件列表怎么用、找达人推广、首发用不用广告、首发抓大放小. Do not use to plan giveaways-for-reviews, search-find-buy, or any incentivized review scheme."
---

# Amazon 新品站外预热与首发流量组合

## 目标

Plan a compliant pre-launch audience build for a new Amazon product (US marketplace by default)—social following, email list, private community, creator seeding, live shopping—and combine it with launch-week PPC and truthful persuasion cues (scarcity, social proof, authority) while excluding any incentivized-review tactic.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源提到的抽奖换评论、让路人「搜索-找到-购买」并留好评等做法违反平台政策，不采用；Vine 是唯一建议的早期评论渠道。
- 「站外销量激增会被推到搜索前列」是来源对算法的解释，只作待验证假设；用 Attribution 与自然排名跟踪去验证。
- 稀缺与限量信息必须真实（真的限量、真的到期），否则违反广告与消费者保护规则。
- 来源中的达人平台推荐不采纳；直播购物功能的可用性与资格以当前站点政策为准。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实与目标购买任务
- 关键词、商品投放、展示和视频的聚合表现
- 受众包定义、资格、站点限制和隐私边界
- 价格、评论、页面、库存与转化基线

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 在库存到仓前留出足够预热窗口（按品类与备货周期校准）：至少一个社媒账号持续发产品诞生过程，用钩子把关注者引导进邮件列表或私域社群。
2. 邮件列表运营：预热期发进度与教育内容建立信任，首发日发限时限量通知；记录打开率、点击率与到达 Listing 的比例。
3. 私域社群预热：让潜在买家参与包装、口味等决定以提升参与感；首发时公告上架，不附带任何评论要求。
4. 达人合作：通过达人平台类别或人工搜索找受众匹配的创作者，寄样并约定内容形式（社媒帖、视频、平台直播）；用 Attribution 链接分渠道追踪成交。
5. 首发周 PPC：新品无评论时转化偏低，用较小预算测试核心词并与站外流量叠加；库存不足时先限流而不是硬推。
6. 用说服原则设计首发信息：限量折扣（稀缺）、创作者背书（权威）、用户故事（社会认同）、品牌介绍视频（喜好）；每条都必须真实可证。
7. 抓大放小复盘：按 Attribution 与广告报告比较各渠道成交与成本，保留效果最好的两三条渠道进入下一次首发模板。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取受众匹配的公开创作者与竞品站外内容的代理观测。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 预热时间线
- 邮件与社群内容计划
- 达人寄样与追踪表
- 首发周广告与库存方案
- 渠道效果复盘表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
