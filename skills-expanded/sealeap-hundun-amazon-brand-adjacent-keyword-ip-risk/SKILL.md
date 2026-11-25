---
name: sealeap-hundun-amazon-brand-adjacent-keyword-ip-risk
description: "Screen whether a candidate core keyword or brand name sits too close to an existing trademark or an unresolved utility patent before building ranking around it, and follow a time-boxed response protocol for a patent dispute or neutral-evaluation notice so a listing is not permanently removed by default inaction. Use for 关键词选到接近商标的通用词怎么办、收到专利异议或中立评估通知怎么处理、要不要参加专利中立评估、被投诉侵权链接下架前的应对窗口. Do not use to provide legal advice or decide litigation strategy; escalate any formal response to qualified IP counsel."
---

# Amazon 关键词商标风险与专利异议应对

## 目标

Screen whether a candidate core keyword or brand name sits too close to an existing trademark or an unresolved utility patent before building ranking around it, and follow a time-boxed response protocol for a patent dispute or neutral-evaluation notice so a listing is not permanently removed by default inaction.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源把平台对知识产权投诉“宁可错杀”当作固定原则，这是对特定时期执法尺度的经验总结，不代表所有品类和站点的现行标准；以当前收到的通知内容与官方政策为准。
- 来源描述的专利中立评估费用、流程时长与判定方式为特定个案的经验数字，不作为通用规则；具体条款以通知内容与平台当时的官方说明为准。
- 通过在品牌名或文案中插入他人商标变体来维持关键词收录，属于打擦边球的规避行为，本 Skill 不采用；核心词与商标的关系应在上架前用检索方式厘清，而不是靠事后文字游戏补救。
- 是否构成侵权、是否值得参加中立评估或和解均属专业法律判断，本 Skill 只提供何时该找律师、该在什么时间点做决定的流程，不替代法律意见。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 上新品前核对目标关键词与拟用品牌名是否落在他人商标权利范围内：用商标查询与专利检索确认核心词是否为注册商标、是否存在同名或近似的未决专利（pending 状态也算风险，不因未授权就当作可放心使用）；若核心关键词本身就是知名商标词，评估绕不开该词时的可替代表达。
2. 避免把品牌名或 Listing 文案中嵌入他人商标的变体拼写（如中间插入前后缀）来试图规避审查；这类做法即使一时不侵权，也会被平台按从严尺度处理，且被下架后基本没有申诉空间。
3. 建立关键词与品牌名的风险分层：确认商标/通用词边界不清晰时，优先使用与自身品牌强绑定、与他人商标无重叠的词根做核心排名词，把可能引发投诉的词降级为辅助词或不使用。
4. 收到平台转来的知识产权异议通知（含专利中立评估邀请）后，第一时间完整阅读条款并记录时间窗口：明确若不在窗口内回应或参加评估，链接是否会被判定为最终处置且不可再申诉；不要把警告类通知等同于普通提醒而搁置。
5. 决定是否参加中立评估或和解前，先咨询有资质的知识产权律师评估己方侵权可能性、评估费用与潜在风险，并核实对方专利的实际授权状态（pending、已授权还是已撤销）。
6. 无论选择参加评估、和解还是不回应，都在到期前把决定和依据落成记录；若因故错过窗口导致链接下架，同步评估是否需要通过法律途径申请恢复，并把这次决定复盘写入未来选品的风险清单。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：查询候选关键词/品牌名对应的商标注册与专利公开状态，作为上架前风险核查的第三方证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 目标关键词/品牌名商标与专利风险核查记录
- 关键词风险分层清单（核心词/辅助词/规避词）
- IP 异议通知应对时间线与决定记录
- 法律咨询要点清单（侵权可能性、费用、专利授权状态）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
