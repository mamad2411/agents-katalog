---
name: sealeap-tianlu-amazon-ai-readable-title-structure
description: "Restructure product titles from keyword-stuffed strings into a semantically ordered two-part layout (brand plus core category and attributes first, then differentiating function and use-case terms), then validate each candidate term's real search relevance through storefront search evidence and keyword-volume data before committing. Treats the premise that stuffed titles now carry an algorithmic penalty as an unverified hypothesis to test with the account's own indexing and conversion data, not an established rule. Use for 标题关键词堆砌整改、语义化标题结构改写、新品上架标题起草. Do not use to assume any claimed algorithm change is official Amazon policy without independent evidence from the account's own search and conversion data."
---

# Amazon 标题语义结构化改写

## 目标

Restructure product titles from keyword-stuffed strings into a semantically ordered two-part layout (brand plus core category and attributes first, then differentiating function and use-case terms), then validate each candidate term's real search relevance through storefront search evidence and keyword-volume data before committing. Treats the premise that stuffed titles now carry an algorithmic penalty as an unverified hypothesis to test with the account's own indexing and conversion data, not an established rule.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 算法转向语义可读是来源自身的市场解读，未见官方公告或政策文本支持，需当作待验证假设，不作为标题必须改写的依据。
- 关键词研究与搜索热度核对建议使用当前可用的关键词工具或后台数据，具体使用哪款工具由账户自身情况决定，不代表对某一特定第三方产品的依赖。
- 标题结构调整对排名与转化的影响需要以自身账户的实际数据验证，来源给出的示例转换不能保证在其他类目或账户上同样有效。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、产品事实、ASIN/SKU 与目标购买意图
- 本品和可比竞品的关键词、自然位置、广告可见度与采样时间
- 搜索词报告、转化、CPC、订单、利润和 Listing 当前覆盖
- 站点语言、变体、价格、库存与同期促销记录

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 核对当前标题是否存在词汇冗余堆砌、场景词混杂、修饰逻辑断裂等问题，逐条标出待精简或待重排的部分，而不是整体推翻重写。
2. 按品牌加核心品类词加关键属性在前、功能卖点加差异化描述加场景词在后的两段式结构重新组织候选标题，确保信息层级从主到次清晰排列。
3. 用后台搜索词建议、店铺内搜索框自动补全等一方或代理证据核对候选词是否为真实被检索的高频词，剔除凭感觉堆砌但无实际搜索量支撑的修饰词。
4. 核对新标题是否仍完整覆盖原有的核心属性与合规必填信息（型号、数量、安全相关信息等），避免为追求简洁而漏掉必要属性。
5. 小范围替换标题后观察自然排名与点击转化的变化，作为验证结构化标题是否优于堆砌式标题这一假设的实际证据，而不是直接全量替换。
6. 若指标未见改善或出现下滑，评估是否回退旧标题或调整两段式结构的具体权重分配，把本次调整当作可回退的单变量实验对待。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充候选标题词的搜索热度与相关词代理数据，用于核实结构化后的候选词是否为真实被检索的高频词，而非仅凭主观判断保留。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 现有标题问题诊断清单
- 两段式候选标题草案
- 候选词搜索相关性核对记录
- 标题替换前后指标对比与回退判断
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
