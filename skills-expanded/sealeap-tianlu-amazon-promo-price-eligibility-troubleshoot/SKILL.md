---
name: sealeap-tianlu-amazon-promo-price-eligibility-troubleshoot
description: "Diagnose why an Amazon promotion submission is rejected on reference-price/regular-price eligibility grounds, and work through a sequence of compliant adjustments (promo-duration pacing, tool selection, pre-submission cap check, List Price external validation, optional SKU split) to restore eligibility without fabricating price history. Mechanics described are current-policy-dependent and must be reverified in the seller console before acting. Use for 促销/秒杀提报报错排查、参考价资格恢复、List Price划线价验证、促销工具选择. Do not use to inflate prices before discounting or to fabricate order history to shape reference price."
---

# Amazon 促销价格资格排错

## 目标

Diagnose why an Amazon promotion submission is rejected on reference-price/regular-price eligibility grounds, and work through a sequence of compliant adjustments (promo-duration pacing, tool selection, pre-submission cap check, List Price external validation, optional SKU split) to restore eligibility without fabricating price history. Mechanics described are current-policy-dependent and must be reverified in the seller console before acting.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 参考价/常规价的具体计算规则（如价格占比阈值、统计窗口天数）会随平台政策调整，文中数字仅为该时点观察到的机制描述，操作前必须以当前后台规则与官方说明为准。
- 各类促销工具是否计入常规价计算、是否显示划线价等属于平台前台展示逻辑，可能因站点、类目或账户而异，需实测确认而非直接套用。
- 拆分SKU属于结构性调整，会影响历史评论与排名积累，只在评估过收益与代价后再执行，不作为默认首选方案。

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

1. 出现促销提报报错时，先在店铺后台确认当前的参考价/常规价计算口径与生效规则，以后台实时提示与官方最新说明为准，不套用旧经验判断报错原因。
2. 回溯近期一段时间内的日常售价与各类促销工具使用记录，核对是否存在促销覆盖天数占比过高、导致系统把促销价并入常规价计算的情况。
3. 核对当前使用的促销工具类型是否会被计入常规价计算，优先安排官方标注为不计入页面常规价的工具，同类效果的工具之间按当前规则重新分配使用频率。
4. 提报前先查看后台“管理促销”页面给出的当前最高可促销价格提示，确认拟提报价格未超过该上限，而不是凭历史提报经验直接提交。
5. 如使用建议零售价作为参考价基础，核实是否有其他渠道以该价格销售或成交的可验证记录，缺乏验证记录时不要假设划线价会正常显示。
6. 若某条Listing的促销资格反复因历史定价行为受限且短期无法解开，评估是否用新SKU单独承接促销场景、原链接维持日常价格的方案，并记录该决策的适用范围与退出条件。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：核实拟填写的建议零售价是否存在其他零售渠道的公开标价或成交记录，作为外部验证证据，避免因无法验证导致划线价与促销资格审核失败。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 促销报错原因诊断记录
- 促销工具计入常规价对照表
- 提报前资格自检清单
- SKU拆分决策记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
