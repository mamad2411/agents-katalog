---
name: sealeap-chiwen-amazon-title-cap-keyword-rebuild
description: "Restructure a listing's title, highlight/bullet fields, and backend search terms when a marketplace enforces a shorter title character limit, reallocating keyword coverage across fields instead of dropping it outright. Prioritizes brand, core product identity, and true differentiators in the title while routing conversion-oriented claims and secondary keywords to the fields designed for them. Use for 标题字数超限被截断、标题关键词堆砌被限流、字符新规上线后要重排关键词、亮点字段怎么写、五点卖点转化率低. Do not use to paste removed keywords verbatim into another field without rewriting them as a coherent sentence, or to treat a platform-suggested title rewrite as final without human review."
---

# Amazon 标题字符合规与关键词重排

## 目标

Restructure a listing's title, highlight/bullet fields, and backend search terms when a marketplace enforces a shorter title character limit, reallocating keyword coverage across fields instead of dropping it outright. Prioritizes brand, core product identity, and true differentiators in the title while routing conversion-oriented claims and secondary keywords to the fields designed for them.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 平台给出的标题优化建议以合规和格式统一为目标，不一定以转化率为目标，可能删除有效的长尾词或场景词，需人工复核后再采用，不能直接全盘接受。
- 标题字符上限、是否设有独立亮点字段及其额度、生效时间等均以当前官方说明和后台实际界面为准，不代入来源中的具体日期或字符数作为长期规律。
- 若账户有内容修改审核期可用于驳回不合理的自动改写建议，但审核机制与时限以当前政策为准，不假设长期不变。

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

1. 导出受影响 Listing 的标题、五点、后台关键词字段与近期销售额、广告花费、自然搜索词数据，按销售权重排出优化优先级，先处理主力款。
2. 核实当前站点标题字符上限、是否有独立的商品亮点或同类字段及其字符额度，规则以当前后台说明和站点公告为准，不沿用旧版规则或来源里的具体数字。
3. 重写标题：只保留品牌、核心产品词、关键差异点与规格适配信息，剔除空泛宣传词与重复词汇；被移出的关键词不直接照搬，而是重新组织进其他字段。
4. 若站点提供亮点或同类字段，用连贯陈述句承接被移出的核心词，说明该商品相对同类的具体优势，避免变成词汇堆砌。
5. 五点描述按购买决策顺序分工（核心卖点、功能效果、规格参数、使用便利、包装售后），关键词自然融入语句而非罗列。
6. 后台搜索词字段补充同义词、缩写、场景词等长尾覆盖，不填竞品词、无关词或标题已出现的重复词。
7. 改版上线后跟踪曝光、点击率、转化率与自然排名变化，同时备份原始文案，指标异常时可快速回滚。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 受影响Listing优先级清单（含销售/广告数据）
- 新旧标题与亮点字段对照表
- 后台关键词补充清单
- 改版前后曝光/点击/转化/排名监控记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
