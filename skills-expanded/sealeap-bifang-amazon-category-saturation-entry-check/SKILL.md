---
name: sealeap-bifang-amazon-category-saturation-entry-check
description: "Decide whether a small FBM or light-FBA seller should enter an Amazon sub-category by reading demand versus competition bars, seller count against new-brand and new-ASIN share, return reasons that reveal improvable defects, and price-band demand against achievable margin, then matching the category to a sourcing advantage with a real barrier before preparing listing keywords from Brand Analytics search terms. Use for FBM 选品、类目分析怎么看、新品牌数新 ASIN 占比、这个类目饱和了吗、本地货源有什么优势、标品能不能做. Do not use to justify listing products with unresolved IP or compliance risk, or to replace supplier-level cost verification."
---

# Amazon 类目饱和度与货源门槛判断

## 目标

Decide whether a small FBM or light-FBA seller should enter an Amazon sub-category by reading demand versus competition bars, seller count against new-brand and new-ASIN share, return reasons that reveal improvable defects, and price-band demand against achievable margin, then matching the category to a sourcing advantage with a real barrier before preparing listing keywords from Brand Analytics search terms.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源以某标品类目为例得出“新人没有机会”，结论依赖当时的数据与站点，不能直接套用；饱和信号需在当前站点横向比较后再判断。
- “低退货率意味着改良空间小”是来源推断；退货原因分布来自第三方汇总，样本可能有偏，需用评论与 Q&A 复核。
- 官方类目分析对未品牌备案卖家的可见范围随政策变化，第三方替代数据标为估算。
- 来源提及的平台合规抽查与关联风险属于传闻，不据此做经营决定；只强调合规经营与不铺可能侵权的产品。

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

1. 先盘点货源优势：列出自己与身边关系可触达的行业、工厂或产业带，以及非公开货盘渠道；候选类目必须能对应到至少一条有门槛（款式或成本）的货源，否则标记为“仅靠运营竞争”并提高后续标准。
2. 从大类到小类浏览类目分析：需求条越长意味着竞争越强，先在自己有认知的大类下挑小类，再对每个小类读四组指标——卖家数与新品牌数、相关 ASIN 数与新 ASIN 占比、退货率与退货原因分布、价格带需求分布。
3. 饱和判定：销量高、卖家多但新品牌与新 ASIN 占比很低，视为已被现有卖家锁定的成熟标品市场，对小卖家标记 NO-GO；比例阈值按站点内其他类目横向比较得出，不用固定数字。
4. 改良空间判定：退货原因主要是“不需要了”“物流延迟”而非质量或功能问题时，说明产品改良空间小；原因中有可修复缺陷时记为切入点。
5. 价格带判定：需求集中在低价带时核算采购、头程、平台费后能否保住目标利润；需求集中在高价带时判断是否属于专业用途或品牌溢价，两者都不利于新卖家，找不到可盈利价格带即退出。
6. 循环与关键词准备：对 NO-GO 类目记录否决理由后换下一个，同一大类下反复 NO-GO 时换大类或补货源，而不是降低门槛标准；对 GO 类目在搜索结果页读取 Brand Analytics 搜索词与平台推荐词纳入 Listing 关键词清单，并在上架前完成版权/IP 初筛。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取类目卖家数、新品占比、退货率、价格带分布及搜索词的第三方代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 货源优势与门槛清单
- 类目指标读表（卖家数、新品牌/新 ASIN 占比、退货原因、价格带）
- 饱和度与改良空间判定记录
- 可盈利价格带核算
- GO/NO-GO 结论与上架前关键词及 IP 初筛清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
