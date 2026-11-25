---
name: sealeap-dijiang-amazon-aplus-content-playbook
description: "Plan Amazon A+ Content around unresolved customer objections mined from reviews and Q&A, structure it into compliant modules that avoid prohibited claims, and route it through creation, preview, and resubmission until approved. Use for A+内容怎么做、A+图文结构、A+被拒怎么改、要不要做品牌旗舰店故事模块. Do not use to add contact information, promotions, competitor references, or guarantee claims that violate A+ content policy."
---

# Amazon A+ 内容策划与合规

## 目标

Plan Amazon A+ Content around unresolved customer objections mined from reviews and Q&A, structure it into compliant modules that avoid prohibited claims, and route it through creation, preview, and resubmission until approved.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “A+ 内容能带来某个百分点的转化率提升”是来源经验总结的行业观察，不是保证值，应以自身商品上线前后的转化率对比作为唯一可信证据。
- “A+ 内容里的关键词会被搜索引擎索引并帮助自然排名”官方未正式确认，只能作为待验证假设，不应作为决定关键词堆砌程度的唯一依据。
- 品牌故事版解锁更多高级模块的具体规则可能随政策调整，实施前应以账号内当前可见的实际选项为准，不假设与来源描述完全一致。
- 挖掘自身与竞品负评作为内容素材输入时，仅用于归纳顾客关注点，不得在 A+ 画面中出现任何可反查的竞品名称或商标。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实和当前 Listing
- 同购买意图可比竞品、价格、评论、图片和销量
- Search Term、Placement、CTR、CVR、订单、退货和利润
- VOC、Q&A、退货原因与任何页面或广告变更日志

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 确认账号已具备创建 A+ 内容的资格（通常要求品牌注册通过），未满足前提时先完成前置的品牌资质认证，不要在不具备资格时排查“为什么创建不了”。
2. 收集本商品与同类竞品的近期负评、追评与常见问答，归纳出顾客在购买前后最常见的疑虑与信息缺口，作为 A+ 各模块要优先回答的内容清单，而不是先想画面再拼内容。
3. 按“基础版”和“品牌故事版”两类模块规划结构：基础版聚焦单个商品卖点与规格细节，品牌故事版聚焦品牌可信度，通常品牌故事版会作为解锁更多高级模块的前提，两者不建议在同一处重复堆砌相同信息。
4. 素材制作优先保证可读性而非信息密度：每屏聚焦一个卖点或一组对比信息，避免文字堆砌导致顾客划走；如涉及系列商品，可加入选购对比模块帮助顾客在自身产品线内比较而不是跳去竞品。
5. 提交前逐条对照 A+ 内容政策自查：不含卖家联系方式、不含站外推广/自身社媒引流、不提及竞品或第三方商标、不含限时促销与价格信息、不含无法兑现的“保证”类措辞、不擅自使用他人商标或平台自身logo。
6. 提交审核后按结果分流：通过则上线并记录上线前后的转化率变化作为自有证据；被拒则对照驳回原因逐条修改后重新提交，不要整体推倒重做。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：如自身评论/问答样本不足，可用第三方评论抓取工具补充自身与竞品的近期评论与问答作为内容素材输入，仅作为顾客疑虑归纳依据，不得复制原文或引用可反查的竞品信息。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 顾客疑虑/问答清单
- A+ 模块结构规划
- 合规自查表
- 提交前后预览记录
- 上线前后转化率对比
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
