---
name: sealeap-hundun-amazon-niche-content-affiliate-traffic
description: "Identify a narrow, non-commodity niche with pricing power by mining audience comments on public content for unmet demand and mystique-driven positioning, then build a low-cost off-Amazon content flywheel paired with a performance-only affiliate program to drive external traffic toward the brand's Amazon listings without relying primarily on paid ads. Use for 站外内容引流怎么起步、联盟推广怎么设计、小众细分品类怎么找、溢价定位怎么讲故事、免费流量渠道有哪些. Do not use to fabricate provenance or efficacy claims about a product's origin or effects, or to treat this as the sole channel without validating Amazon-side conversion economics."
---

# Amazon 站外内容矩阵与联盟引流选品

## 目标

Identify a narrow, non-commodity niche with pricing power by mining audience comments on public content for unmet demand and mystique-driven positioning, then build a low-cost off-Amazon content flywheel paired with a performance-only affiliate program to drive external traffic toward the brand's Amazon listings without relying primarily on paid ads.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源展示的具体互动量、粉丝规模与年营收数字为特定账号的历史快照，不代表可复制的效果；评估选品与内容方向时以自身账户与内容表现为准。
- “零投流、完全靠免费流量”是来源的个案描述，不同类目与市场的自然流量获取难度差异很大；应把免费流量当作补充渠道验证，不作为唯一流量假设。
- 内容素材如涉及他人拍摄的图片或视频二次创作，需先确认使用权限与平台版权政策，来源中“搬运再处理”的做法存在版权风险，不建议直接复制他人素材。
- 溢价故事化定位需与产品实际信息一致；把普通材质包装成有特殊功效或稀缺产地而缺乏依据的表述，可能构成虚假宣传，不采用。

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

1. 从海外内容平台的头部创作者内容评论区反向挖掘需求：找到受众持续追问“这是什么产品、哪里能买”的高互动内容，记录反复出现的关键词和使用场景，作为该细分需求存在但供给不透明的初筛信号。
2. 选品优先级向体积小、价格不敏感、叙事空间大的细分品类倾斜，避开已被大量成熟卖家占据、只能靠比价竞争的大众类目；用同类目现有卖家数量和内容饱和度做粗筛。
3. 给产品设计溢价定位而非跟随现有低价竞品：围绕产地、工艺、文化背景或功效讲一个可信但不夸大的故事，定价对标情感/收藏属性相近的品类而非同质化商品的地板价；所有表述需与产品真实情况一致，不编造功效或来源。
4. 搭建内容矩阵作为免费流量入口：以图文/短视频形式围绕选定叙事持续产出内容，可复用已有素材加辅助工具二次创作降低产能门槛，但需核实素材授权与合规使用范围，避免侵犯他人版权。
5. 设计按业绩付费的联盟/推广者计划，只在实际产生转化后支付佣金，佣金比例参考同类目常见区间并结合自身毛利空间校准，不预设固定数字。
6. 若最终承接页是独立站，需在独立站与亚马逊之间做好流量与转化的分工验证：观察站外内容与联盟带来的访问是否能转化为实际订单，用账户内数据判断是否值得持续投入，而不是只看内容互动量。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取目标细分品类在内容平台上的公开评论与话题热度，作为需求线索与叙事验证的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 细分需求与选品线索清单（来源评论区高频诉求）
- 溢价定位与叙事脚本草案
- 内容矩阵产出计划（素材来源与合规核查）
- 按业绩付费联盟计划条款草案
- 站外流量到订单转化验证记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
