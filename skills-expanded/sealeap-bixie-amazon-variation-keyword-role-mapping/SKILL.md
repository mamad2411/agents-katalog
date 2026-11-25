---
name: sealeap-bixie-amazon-variation-keyword-role-mapping
description: "Analyze keyword coverage at the parent-ASIN level to assign each child variation a distinct keyword role instead of letting variations compete for the same terms. Benchmarks against a competitor's parent-level keyword spread to find coverage gaps the competitor has left open. Use for 竞品关键词比我多、多变体自相竞争、变体该主攻什么词、看不清父体流量全貌. Do not use for single-variation keyword optimization, or to delist a variation before verifying parent-level data."
---

# Amazon 变体结构关键词角色分配

## 目标

Analyze keyword coverage at the parent-ASIN level to assign each child variation a distinct keyword role instead of letting variations compete for the same terms. Benchmarks against a competitor's parent-level keyword spread to find coverage gaps the competitor has left open.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 流量词数量由结构决定而非文案决定是一种经验归纳，并非平台机制的官方结论，调整变体结构前仍需结合具体关键词相关性判断。
- 下架低效变体会影响该变体已积累的历史评论与排名权重，属于不易完全回退的操作，执行前需评估其对整体链接的影响并留存证据。
- 竞品父体的关键词与流量数据来自第三方代理估算，存在误差和延迟，只能作为方向参考，不能当作竞品真实数据直接使用。

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

1. 先在父体层面拉出整条链接的关键词、流量与价格分布，而不是只看单个子体的转化数据。
2. 从父体数据里区分全变体通用的核心词和只适合特定子体的细分属性词，避免所有子体重复投放同一批词。
3. 结合各子体的历史转化与流量表现，为每个子体分配明确角色（冲大词、占细分场景词、或列为低效变体候选下架），形成一张变体关键词分工表。
4. 用同样方法拉出一到两个主要竞品的父体关键词与变体结构，标出对方未覆盖或投入较弱的词与变体定位。
5. 优先在竞品薄弱的词和定位上做差异化布局，而非跟随竞品已占优的核心词正面竞争。
6. 定期复查各子体排名与流量占比变化，排名上升的角色分配继续加强，下滑的重新核对关键词与 Listing 匹配度。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品父体的关键词分布与流量结构作为变体角色划分的比对证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 父体关键词流量全景表
- 变体角色分工表
- 竞品父体差异对比表
- 排名变化跟踪记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
