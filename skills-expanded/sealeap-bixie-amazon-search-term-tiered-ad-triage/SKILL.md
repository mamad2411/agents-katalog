---
name: sealeap-bixie-amazon-search-term-tiered-ad-triage
description: "Triage a search-term report into no-conversion, high-ACOS-conversion, and healthy-conversion buckets and apply a distinct action to each bucket instead of one blanket bid change. Uses root-word frequency across winning and losing terms to scale negative keywords and broad-match expansion. Use for 广告烧钱不出单、ACOS忽高忽低怎么拆、搜索词该否定还是该加预算. Do not use to bulk-negate keywords without root-word review, or to treat a single reporting window as a long-term conclusion."
---

# Amazon 搜索词报告分层优化

## 目标

Triage a search-term report into no-conversion, high-ACOS-conversion, and healthy-conversion buckets and apply a distinct action to each bucket instead of one blanket bid change. Uses root-word frequency across winning and losing terms to scale negative keywords and broad-match expansion.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 转化率不低于基准就是出价偏高是一种经验判断，实际还需排除展示位置、时段、竞对临时降价等外部干扰因素。
- 词根统计得到的否定与拓展建议需要人工复核相关性，同词根不代表语义或购买意图完全一致，批量操作前应抽样检查。
- 曝光点击转化三层漏斗的优化口诀是经验启发式，实际问题可能叠加多个环节，需结合完整数据确认根因。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 导出搜索词报告并按花费从高到低排序，先看清楚预算主要花在哪些词上，再决定优化动作。
2. 对有花费无转化的词，先判断是否与产品明显不相关：不相关的直接否定，相关但曝光点击不足的先给观察期再下结论。
3. 对有转化但 ACOS 高的词，对比其转化率与同类目基准：转化率不低于基准的优先怀疑出价过高，可尝试小幅降价或调整广告位；转化率本身偏低的转向优化 Listing 或收窄匹配方式。
4. 对转化好且 ACOS 健康的词，核实它们是否集中贡献了大部分优质转化，确认后为其单独建精准投放或追加素材投放，而不是继续埋在原广告组里。
5. 对否定词和高转化词分别做词根统计，同词根的否定词批量处理，同词根的高转化词用于拓展新的广泛匹配广告。
6. 结合曝光、点击、转化三层漏斗数据定位问题所在环节（曝光高点击低查主图、点击高转化低查详情页），把否词与加预算动作和对应素材优化项绑定执行。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 搜索词三层分类表
- 词根否定与拓展清单
- 转化率对标分析
- 漏斗诊断与优化动作清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
