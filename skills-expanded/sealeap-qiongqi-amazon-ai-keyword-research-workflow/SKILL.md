---
name: sealeap-qiongqi-amazon-ai-keyword-research-workflow
description: "Run an agentic AI keyword research workflow for an Amazon product: start with the simplest prompt, add raw keyword exports and explicit context, require intent-segregated output against an excellence example, then verify relevance before campaign use. Use for AI 做关键词调研、关键词分组自动化、把关键词导出给 AI 整理、AI 关键词表能不能直接投. Do not use AI output for live campaigns without human relevance review."
---

# Amazon AI 辅助关键词调研工作流

## 目标

Run an agentic AI keyword research workflow for an Amazon product: start with the simplest prompt, add raw keyword exports and explicit context, require intent-segregated output against an excellence example, then verify relevance before campaign use.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- AI 会从公开网页与搜索联想补词，可能引入无搜索量或不相关的词；搜索量只信来自工具导出的数据。
- 『AI 已可完全替代人工关键词调研』是来源观点，属待验证假设；仍需按类目抽检。
- 输出质量高度依赖上下文与示例，模型与工具版本变化会改变结果，每次批量使用前先跑小样本对照。
- 含他人品牌、受保护词或违规声明的词不得直接投放；相关性与合规复核由人负责。

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

1. 先做最简尝试：只给产品链接或产品事实，让 AI 输出关键词调研；追问它的来源与分组方式，记录缺口（覆盖不全、未按意图分组、混入不相关词）。
2. 补数据：从关键词工具导出目标主词的完整未过滤关键词列表，连同产品事实一起提供；不要预先手工过滤，把过滤逻辑交给模型。
3. 补上下文：明确要求只保留与产品相关的词、指出机会点、按购买意图/语义核心分组，并给出输出格式（分组表、后台搜索词、竞品品牌词、否定词、意图说明）。
4. 给一份『优秀输出示例』作为模板，让 AI 对齐结构与质量；把这套提示固化成可复用的 Skill 或 SOP，让它主动追问缺失的上下文。
5. 人工复核：抽查每组关键词与产品事实的相关性、搜索量是否来自导出数据而非臆测，剔除幻觉词与不合规词。
6. 复核后的分组表交给分组建活动流程；上线后用搜索词报表验证分组是否与实际触发搜索一致，并把纠错回填到示例模板。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取原始关键词列表、搜索量与竞品关键词的第三方代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- AI 关键词调研提示与上下文包
- 按意图分组的关键词表
- 人工复核记录
- 优秀输出示例模板
- 可复用 Skill/SOP 草案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
