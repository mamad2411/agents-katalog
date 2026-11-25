---
name: sealeap-fenghuang-amazon-product-research-methods
description: "Generate product candidates for the US marketplace through several discovery paths—keyword-gap search, filtered product databases, reverse-ASIN keyword pulls, and own-problem ideas—then push every candidate through the same demand, competition, and revenue-estimate validation before shortlisting. Use for 怎么找产品、选品方法有哪些、关键词找品、反查竞品关键词、自己想做的产品有没有市场、竞品月销怎么估. Do not use to output a final GO decision without unit economics and compliance checks."
---

# Amazon 多路径选品发现与需求验证

## 目标

Generate product candidates for the US marketplace through several discovery paths—keyword-gap search, filtered product databases, reverse-ASIN keyword pulls, and own-problem ideas—then push every candidate through the same demand, competition, and revenue-estimate validation before shortlisting.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「搜索结果越靠后销量越少」是来源的经验分布，实际曲线随类目与设备不同，用当前数据观察。
- 所有月销与营收数字都是第三方估算，标为 ESTIMATE；不同工具口径差异大，不得写成事实。
- 来源强调「先动手别拖延」，可作决策节奏建议，但不等于省略验证步骤。
- 来源中的选品工具与课程推荐不采纳；本 Skill 只描述工具类别。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 明确目标：找「有稳定搜索需求 + 头部竞争可撼动」的品，而不是「便宜好做」的品；先定 marketplace（默认 US）与可投入资金上限。
2. 路径 A 关键词缺口：用关键词工具类别列出搜索量可观的短语，到前台搜索看结果是否缺少精准匹配产品或匹配品质量差；把缺口写成可证伪假设。
3. 路径 B 数据库筛选：按目标月营收、评论数上限、价格带等条件筛产品库，产出候选池；筛选条件以自有资金和类目校准。
4. 路径 C 反查竞品：对候选品头部 ASIN 做关键词反查，看其流量词是否集中、是否存在本品能覆盖而对手未覆盖的词。
5. 路径 D 自身痛点或兴趣：把自己遇到的未被满足需求写成产品定义，但同样走路径 B、C 验证，不因「热爱」跳过数据。
6. 统一估算：用 BSR 与销量估算工具类别推算头部竞品月销与营收（销量 × 售价），标注估算口径；多家工具口径不一致时并列保留，不取平均。
7. 竞争判断：看首页产品的评论数、评分、价格与品牌集中度，判断新品能否以差异化进入；输出候选短名单与各自的缺口证据。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取关键词搜索量、竞品反查词、产品库筛选与销量估算的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 候选品发现记录
- 关键词缺口假设表
- 竞品反查词表
- 销量与营收估算表
- 候选短名单与竞争判断
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
