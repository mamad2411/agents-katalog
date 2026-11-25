---
name: sealeap-tianlu-amazon-ai-agent-mcp-product-research
description: "Configure an AI coding/agent tool with a third-party Amazon-data MCP connector to retrieve category, ASIN sales-structure, keyword, review, and price-band evidence, and drive a structured, source-traceable product-selection analysis. Estimates from the connector are directional third-party proxies, not first-party Amazon data. Use for 配置AI选品工作流、用MCP连接器批量拉取选品数据、让Agent做可溯源的选品分析. Do not use its output as a final selection decision without cross-checking an independent source."
---

# Amazon AI选品数据代理协同

## 目标

Configure an AI coding/agent tool with a third-party Amazon-data MCP connector to retrieve category, ASIN sales-structure, keyword, review, and price-band evidence, and drive a structured, source-traceable product-selection analysis. Estimates from the connector are directional third-party proxies, not first-party Amazon data.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 第三方数据MCP连接器返回的销量、搜索量等均为平台外估算值，与亚马逊官方后台口径可能存在差异，只能作为方向性参考，不能替代自身店铺一方数据。
- AI Agent的分析步骤与结论组织方式依赖其推理过程，同样的数据在不同次调用中可能产出不同表述，关键结论需人工复核而非直接采纳。
- 数据连接器的可用字段、鉴权方式与购买渠道由服务商决定且会变化，接入前以服务商当前文档为准。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、产品事实、品牌语气和当前政策约束
- 已授权的 Listing、关键词、评论/VOC、图片和竞品证据
- 每项数据的来源、时间、站点、样本和限制
- 人工审核人、发布边界和不可生成的声明或视觉特征

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 在AI编程/agent工具中新增一个第三方亚马逊数据MCP连接器，按数据服务商当前的接入文档完成鉴权（通常需在服务商后台单独购买或开通该接口权限），并用一次最小化查询验证连通与返回字段。
2. 明确本次选品要回答的具体问题（如某类目容量、某关键词竞争格局、某价格带机会），把问题拆解成需要拉取的数据字段清单，避免让Agent无目标地全量抓取。
3. 让Agent按拆解好的步骤依次调用数据连接器获取类目大盘、ASIN销量结构、关键词搜索量、竞品评论与价格带分布，每一步先检查返回数据的时间窗口、样本量与口径是否与上一步一致。
4. 对Agent给出的中间结论（如某类目机会、某价格带空档）逐项要求列出支撑数据来源与计算方式，凡是无法追溯到具体返回字段的结论标记为待验证，不直接采信。
5. 把Agent产出的候选清单与至少一个独立信源（如另一数据连接器或人工核对店铺后台）做交叉验证，出现明显冲突的候选先搁置。
6. 保留本次查询的字段范围、时间窗口与Agent推理过程记录，作为后续复查或调整分析问题的依据。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：通过第三方亚马逊数据MCP连接器获取类目大盘、ASIN销量结构、关键词搜索量、竞品评论与价格带分布，供AI Agent做可溯源的选品分析与交叉验证。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- MCP连接器接入与验证记录
- 选品问题拆解与字段需求清单
- 候选品交叉验证结果表
- Agent推理过程留痕记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
