---
name: sealeap-baxia-amazon-ai-shopping-evidence-pipeline
description: "Assemble a repeatable evidence pipeline covering demand mining, side-by-side competitive teardown, and review-driven pain-point extraction before drafting Amazon listing copy and images meant to be legible to AI-assisted shopping interfaces. Use for AI购物入口上线后的选品调研、竞品拆解取证、评论痛点提炼、文案与图片产出前的证据准备. Do not use to fabricate competitive data or to publish AI-drafted copy without a human fact and policy check."
---

# Amazon AI购物入口内容生产流程

## 目标

Assemble a repeatable evidence pipeline covering demand mining, side-by-side competitive teardown, and review-driven pain-point extraction before drafting Amazon listing copy and images meant to be legible to AI-assisted shopping interfaces.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- AI购物入口的具体名称、覆盖市场与呈现形式会持续变化，操作前需在目标站点确认当前实际功能，不套用过去经验。
- 第三方数据聚合工具给出的市场信号是估算代理证据，需与账户一方真实数据交叉验证后再作决策。
- 内容是否更容易被AI购物入口理解和推荐，目前缺乏可验证的因果机制，只能作为待验证假设，不能承诺排名或推荐效果。

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

1. 用自然语言检索工具圈定细分需求，记录检索词、返回结果与筛选口径，标注哪些是待验证的市场信号而非确定销量。
2. 对锁定的竞品做逐项对比拆解（价格、评分、核心卖点、差评主题），形成结构化的优劣势表而非主观印象。
3. 从竞品与自身评论中提炼高频买家关切，按发现、比较、决策阶段归类，标记证据来源与样本量。
4. 把上述证据转成文案与视觉素材的创作简报（标题、五点、图片脚本），要求每条卖点都能追溯到具体证据。
5. 生成的文案与图片先做政策与事实核对，再小范围测试信息结构变化对转化的影响，不做一次生成即上线。
6. 沉淀本次从调研到产出的证据链模板，供下次同类目复用，避免每次重新摸索工具组合。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充关键词、竞品对比与评论痛点等第三方证据，用于支撑文案与图片素材的产出简报。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 细分需求检索记录
- 竞品优劣势对比表
- 买家痛点证据矩阵
- AI可读文案与图片简报
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
