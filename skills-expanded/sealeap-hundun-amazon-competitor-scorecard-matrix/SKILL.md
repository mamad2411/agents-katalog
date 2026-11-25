---
name: sealeap-hundun-amazon-competitor-scorecard-matrix
description: "Build a multi-dimension scorecard from the current top-ranked listings in a target category, covering image and variant coverage, review sentiment gaps, category-specific packaging or authenticity weight, ad presence, organic-traffic share, landed cost and margin, and price-history-flagged promotion-inflated volume, to score candidate products instead of copying the single best-looking listing. Use for 竞品数据该收集哪些维度、怎么判断一个爆款是不是靠广告砸出来的、怎么看历史降价识别冲量、选品评分表怎么搭. Do not use to justify entering a category solely because one listing looks good, or to treat a single metric as sufficient evidence without cross-checking ad dependency and price history."
---

# Amazon 竞品多维度选品评分表

## 目标

Build a multi-dimension scorecard from the current top-ranked listings in a target category, covering image and variant coverage, review sentiment gaps, category-specific packaging or authenticity weight, ad presence, organic-traffic share, landed cost and margin, and price-history-flagged promotion-inflated volume, to score candidate products instead of copying the single best-looking listing.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的各维度重要性排序基于特定类目经验，实际权重需按目标类目重新判断，不能整表套用到所有品类。
- 评论数多但成交少代表是老链接、评论少但成交多代表是新起链接是来源的经验推断，实际情况还受平台评论展示规则与数据口径影响，需结合月销量与上架时间等其他信号交叉验证。
- 广告投放力度与花费均为第三方工具的估算或前台观测，不是平台一方数据，应标注为估算并结合自身广告后台数据校准。
- 历史价格骤降或评论异常波动只是需要进一步核实的风险信号，不能仅凭这一项就断定对照产品存在违规操作。

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

1. 按类目规模确定采样范围：抓取该类目搜索结果前列的一批 Listing 作为对照池，类目越大采样越多；逐个记录以下维度，缺项标注待补充而非留空猜测。
2. 内容维度：主图/副图风格与数量、变体覆盖广度、产品属性填写完整度、页面视觉风格是否与类目调性匹配；部分类目额外记录是否强调正品授权或品牌调性，部分类目额外记录页面是否分风格系列。
3. 口碑维度：评分分布、差评高频问题与未被满足的诉求（用于后续差异化）、是否存在评论异常波动（短期内评论激增或结构异常需要另外核实真实性，不直接采信为自然增长）。
4. 流量与成本维度：是否投放广告及大致投放力度、自然流量占比高低、当前市场价格带与历史价格/优惠券记录（历史价格骤降后又冲量的模式提示可能靠让利冲单，而非稳定真实需求）。
5. 经济性维度：估算对照产品的采购成本与毛利空间、月销量与月销售额量级、转化率与流量价值，转化率需与流量质量一起看，不能单独作为好坏标准。
6. 汇总打分：把以上维度按自身产品的实际情况加权，排除数据好看但广告依赖度高、自然流量占比低、历史价格异常的样本，优先参考销量稳定且自然流量占比健康的对照产品，形成候选产品的差异化改进方向而非直接照抄。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取类目前排 Listing 的公开图片、评论、价格历史与广告位出现频次等数据，作为竞品评分表的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 类目对照池采样清单
- 多维度评分表（内容/口碑/流量成本/经济性四类）
- 广告依赖度与自然流量占比核查记录
- 差异化改进方向清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
