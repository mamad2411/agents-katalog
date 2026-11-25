---
name: sealeap-qiongqi-amazon-main-image-ai-iteration
description: "Iterate Amazon primary images as a continuous experiment: mine search term and performance data for click-through hypotheses, generate compliant image variants with AI, and validate through Manage Your Experiments before rollout. Use for 主图怎么优化、点击率低换主图、AI 生成主图、主图 A/B 测试、主图假设从哪来. Do not use to publish images that misrepresent the product or add claims outside the real packaging."
---

# Amazon 主图数据驱动 AI 迭代测试

## 目标

Iterate Amazon primary images as a continuous experiment: mine search term and performance data for click-through hypotheses, generate compliant image variants with AI, and validate through Manage Your Experiments before rollout.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源列举的点击率与转化率提升幅度为其案例数据，不可外推；本账户效果只以实验结果为准。
- 『主图也影响转化率是因为吸引了更相关的流量』是来源解释，属待验证假设。
- 生成式图像可能产生与实物不符的细节或违规元素，任何上线前须人工逐项核对图片规则。
- 实验结果受同期价格、促销、库存与广告变化干扰，测试期间保持这些变量不变。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实和当前 Listing
- 同购买意图可比竞品、价格、评论、图片和销量
- Search Term、Placement、CTR、CVR、订单、退货和利润
- VOC、Q&A、退货原因与任何页面或广告变更日志

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 拉取报表可用最长窗口的搜索词报表与 Listing 的曝光、点击率、转化率基线，明确当前主图是猜测还是有数据支撑。
2. 让 AI 分析搜索词与评论：提炼买家的核心意图、异议与关注点（用途、人群、成分、尺寸、配件），标注哪些已在主图体现、哪些缺失。
3. 把缺失点写成可证伪的点击率假设，每条只改一个主要元素：加人物/使用场景、展示成分或配件全家福、在真实包装上呈现主搜索词或指标、突出色彩对比、换角度或渲染风格、展示多颜色变体。
4. 按假设生成变体，先做合规审查：产品外观必须与实物一致，指标与声明只能出现在真实包装上，纯白底与主体占比等图片规则照旧；细节偏差用编辑功能修正而不是接受。
5. 在 Manage Your Experiments 里配置 A/B（A=现图，B=一个假设），跑满平台要求的时长，看点击率与转化率的实际差异；转化率变化解释为流量相关性变化的假设。
6. 赢家上线后继续用新假设挑战，把每轮的假设、结果与结论沉淀成可复用工作流；不赢则回到假设库换方向。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取同一搜索结果页竞品主图与价格的公开页面观测，用于对照点击率假设。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 买家意图与异议清单
- 主图点击率假设库
- 合规审查表
- A/B 实验记录
- 主图迭代工作流
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
