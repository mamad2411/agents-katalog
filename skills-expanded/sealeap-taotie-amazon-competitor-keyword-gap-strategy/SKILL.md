---
name: sealeap-taotie-amazon-competitor-keyword-gap-strategy
description: "Reverse-look-up the keyword footprints of top competing ASINs, score each term by relevance weight and rank stability, monitor competitor and own keyword ranks over several days, and build a staged keyword plan that first targets terms where competitors rank weakly but conversion is acceptable, before escalating to head terms. Use for 竞品关键词反查、竞品主打哪些词、关键词排名监控、绝对排名怎么算、新品先打什么词、避开头部竞争、关键词收录检查、流量词权重. Do not use to claim exact rank positions as facts or to plan rank manipulation."
---

# Amazon 竞品关键词反查与错位竞争词策略

## 目标

Reverse-look-up the keyword footprints of top competing ASINs, score each term by relevance weight and rank stability, monitor competitor and own keyword ranks over several days, and build a staged keyword plan that first targets terms where competitors rank weakly but conversion is acceptable, before escalating to head terms.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 流量权重评分、排名位置与搜索量均为第三方估算或抓取值，受地域与个性化影响，标为 ESTIMATE，不作事实。
- 「先打竞品弱词再升级」是来源的策略经验，成效取决于弱词是否真有转化，需用本账户搜索词报告验证。
- 来源提到用刷单推关键词排名，本 Skill 不采用；排名提升只通过 Listing 相关性、广告与合规促销。
- 关键词收录机制未公开，收录检查结果只能作为 Listing 相关性的间接观测。

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

1. 选定类目前十左右的竞品 ASIN，对每个做关键词反查；新上架的 ASIN 可能查不到历史词，记录缺口而非猜测。
2. 对反查出的词看三项：月搜索量、历史趋势、相关性/流量权重评分；只保留评分在工具中上等级以上且与本品事实匹配的词作为候选池。
3. 把候选词导入排名监控，连续观察数天：竞品在某词上长期稳定靠前的，归为「暂不正面竞争」；竞品排名靠后或波动大但该词仍有搜索量与可接受购买率的，归为「优先切入」。
4. 计算绝对排名时用（页码 - 1）× 每页位数 + 页内位次，并接受因 IP、配送地址与个性化导致的偏差；同一词以多次采样的中位数记录。
5. 上架后用收录检查工具确认标题、五点、描述中的目标词是否被平台索引；未收录的词先修 Listing 相关性再投广告。
6. 分阶段执行：新品期把优先切入词作为广告与 Listing 主词，达到稳定排名后再把预算转向次级主词与大词；每阶段写清升级条件与回退条件。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品反查关键词、流量权重、关键词排名监控与收录状态的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 竞品反查词池
- 词的权重与稳定性评分表
- 排名监控记录
- 收录检查结果
- 分阶段关键词计划
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
