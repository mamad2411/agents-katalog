---
name: sealeap-hundun-amazon-blue-ocean-filter-differentiation
description: "Narrow blue-ocean product candidates using a combined filter of search-demand floor, competing-listing count ceiling, minimum price floor, non-seasonality, click-concentration ceiling and an ad-cost ceiling as a competition proxy, then mine negative reviews on shortlisted competitors for unmet needs to design a differentiated version, with an IP screen before committing to sourcing. Use for 蓝海类目怎么快速筛、选品筛选条件怎么组合、差评怎么挖差异化点、选完品还要查什么再下单. Do not use to skip the IP screen step, or to copy a competitor's product one-to-one without addressing the mined pain points."
---

# Amazon 蓝海筛选与差评差异化

## 目标

Narrow blue-ocean product candidates using a combined filter of search-demand floor, competing-listing count ceiling, minimum price floor, non-seasonality, click-concentration ceiling and an ad-cost ceiling as a competition proxy, then mine negative reviews on shortlisted competitors for unmet needs to design a differentiated version, with an IP screen before committing to sourcing.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的搜索量、竞品数量、价格、点击集中度与广告竞价的具体阈值为特定时点的经验参考，需按当前账户数据与类目基准重新校准，不作为固定标准。
- 差评中反映的问题只是候选痛点，不代表解决后一定能转化为销量提升；改进方向仍需通过小批量上架与实际转化数据验证。
- 第三方选品工具给出的搜索量、点击集中度与广告竞价均为估算或平台数据的再加工，与官方一方数据可能存在口径差异，决策前应与前台观测交叉核对。
- 知识产权初筛只能排除明显红旗，查不到不代表没有风险；涉及外观相近或功能性专利较多的品类，建议在批量采购前追加专业查询。

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

1. 先明确蓝海判断的核心逻辑：需求足够大但竞争足够小，用搜索结果数量和广告竞价水平两个方向性指标交叉判断，而不是只看其中一个；具体数值门槛按当前账户目标毛利与类目基准校准，不套用固定数字。
2. 用组合筛选条件缩小候选范围：设定搜索量下限、竞品数量上限、价格下限、排除季节性产品、点击集中度上限、广告竞价上限；这些门槛都需要按自身目标利润和风险承受度设定，来源给出的具体数值仅作起点参考。
3. 对通过筛选的候选词，回到平台前台核实真实搜索结果数量与关键词近期搜索趋势、点击集中度、广告竞价区间，避免只信任工具后台数据而不做前台交叉验证。
4. 核实候选产品的大致采购成本，估算目标售价下的毛利空间是否达到自身要求；成本核实要覆盖同款产品的至少几个供应商报价，不只取第一个报价。
5. 从头部竞品的差评与购买动机中提炼未被满足的诉求（功能不好用、耐用度不足、结构不牢固等常见类型），针对性设计差异化改进点，而不是直接复制头部产品的规格；差评文本可人工抽样阅读或用文本分析工具辅助归类高频问题。
6. 正式下单采购前补做知识产权初筛：核对产品外观、名称与核心宣传语是否可能触碰他人已注册商标或外观专利，初筛通过后再进入打样与批量采购环节。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选关键词的搜索量、点击集中度、广告竞价区间及竞品差评文本等代理数据，用于蓝海筛选与差异化设计。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 组合筛选条件与候选类目清单
- 前台搜索结果与关键词趋势交叉核验记录
- 供应商报价与毛利测算表
- 差评痛点归类与差异化改进方向
- 上市前知识产权初筛记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
