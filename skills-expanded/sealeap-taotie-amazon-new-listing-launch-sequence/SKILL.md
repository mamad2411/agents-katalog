---
name: sealeap-taotie-amazon-new-listing-launch-sequence
description: "Sequence a new seller's first launch—account document readiness, product decision, keyword-to-listing preparation, an FBA-first test shipment, compliant review acquisition, the first Sponsored Products run and the first report review—so each step has an entry condition and a checkable output before the next starts. Use for 新手运营顺序、先做什么后做什么、注册前准备什么资料、先自发货还是直接 FBA、新品期怎么用、什么时候开广告、广告开多久看报表. Do not use for multi-account setup, VPS isolation, or any review-manipulation tactics."
---

# Amazon 新品上线运营节奏与前置检查

## 目标

Sequence a new seller's first launch—account document readiness, product decision, keyword-to-listing preparation, an FBA-first test shipment, compliant review acquisition, the first Sponsored Products run and the first report review—so each step has an entry condition and a checkable output before the next starts.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「自配送等于浪费新品期流量」「新品期有流量扶持」是来源观点，新品期机制未公开，用本店新品前几周的访问量与转化数据验证，不作规律。
- 来源提及「做评价」与多账号云服务器操作，本 Skill 只保留合规获评渠道，不采用刷评或关联规避做法。
- 注册资料要求、身份验证方式与收款渠道随站点和年份变化，以当前注册页面提示为准。
- 「广告跑一周再看报告」是经验节奏，实际以点击样本量是否足够判断，不以天数为准。

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

1. 开户前按当前站点要求备齐资料：可扣美元的信用卡与其账单、公司营业执照、法人身份证件正反面合一、第三方收款账户；资料不全先不提交注册，避免审核中断。
2. 选品与注册可并行，但上架前必须有选品结论与关键词清单：用关键词工具与搜索趋势确定主词与长尾词，再据此写标题、五点与描述；主图白底且分辨率满足当前要求。
3. 首发默认走 FBA 而不是自配送：自配送很难拿到购物车和新品期流量，测不出真实转化；首批可少量发 FBA，把「新品期内的转化率与访问量」作为该品是否加码的证据。
4. 上架后在开广告前处理评价基础：只用平台合规渠道（请求评论按钮、Vine 等按当前资格）获取评价，并区分 review 与 feedback；无评价时广告转化通常偏低，预算先收着。
5. 开启自动 + 手动各一组小预算广告，运行到累计足够点击样本（来源以约一周为经验起点）后下载搜索词报告，按报告结论调整关键词与出价。
6. 进入常态循环：每周看业务报告的访问量、转化率、销量三项，与广告报表交叉，判断问题在流量还是转化；把每一步的入口条件、产出物与负责人写成节奏表。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充关键词搜索量与趋势的第三方代理证据，用于上架前的关键词清单。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 开户资料清单
- 上架前关键词与素材清单
- FBA 首发测试计划
- 合规获评与广告启动节奏表
- 首轮报告复盘记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
