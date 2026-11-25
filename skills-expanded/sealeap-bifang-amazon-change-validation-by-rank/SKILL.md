---
name: sealeap-bifang-amazon-change-validation-by-rank
description: "Validate each listing or advertising change on Amazon by recording the change and its previous value, sampling organic and sponsored keyword positions for the main terms before and after under the same conditions, waiting for the effect window, then keeping, revising or reverting the change based on the observed movement rather than on intuition. Use for 改了 Listing 排名变了吗、否词否错了、加词有没有用、关键词收录查询、优化还是负优化、变更记录怎么做. Do not use to draw conclusions from a single rank query or to attribute rank changes to a change made together with price, stock or promotion changes."
---

# Amazon 变更后关键词排名验证回退

## 目标

Validate each listing or advertising change on Amazon by recording the change and its previous value, sampling organic and sponsored keyword positions for the main terms before and after under the same conditions, waiting for the effect window, then keeping, revising or reverting the change based on the observed movement rather than on intuition.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 排名查询受地区、登录态、变体、个性化与采样时间影响；单次查询和跨条件比较都不作为结论。
- 排名变化与变更之间的因果由来源直接断言；同期市场事件、竞品动作和季节都可能造成移动，需列出替代解释后再判定。
- 第三方工具的页面评分是启发式打分，不代表平台标准；主图尺寸等规范以当前官方要求为准。
- 排名不是唯一目标，最终以转化与利润复核；排名上升但转化下降时不视为成功。

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

1. 变更前建基线：选定主词与若干精准长尾词，在同一条件（站点、邮编、登录态、时段）下连续几天查询自然位与广告位（区分含广告位与不含广告位、品牌广告与商品广告），记录页码与位次。
2. 记录变更：写明对象（主图/标题/五点/描述/某广告词/否定词）、旧值、新值、时间与预期方向；一次只改一个主要变量，价格、库存、促销同期有变动时标注为混杂因素。
3. 等待观察窗：按平台收录与广告归因的常见延迟设定观察期，期间不叠加其他改动；观察期长度以当前账户历史上排名对变更的响应时间校准。
4. 判定：目标词自然位持续上升、广告位在同竞价下改善视为正向，保留并归档；位置下降或收录消失视为负向，恢复旧值后再复查是否回到基线；无变化则记为无效变更，考虑再改。
5. 广告专项：否定某词后相关词排名下降，说明否错，撤销否定；新增精准投放花费上升但位置不动或下降，说明词不合适，降价或移除。
6. 沉淀：把每次变更与判定结果累积成变更日志，形成“哪些改动对本品有效”的账户内证据；查询量大时评估用自动排名监控换时间。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：批量抓取主词的自然位与广告位作为前后对比的代理观测。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 主词排名基线表（自然位/广告位，采样条件）
- 变更记录（对象、旧值、新值、预期、混杂因素）
- 观察窗后判定与回退记录
- 广告否词/加词专项判定
- 变更日志与有效改动清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
