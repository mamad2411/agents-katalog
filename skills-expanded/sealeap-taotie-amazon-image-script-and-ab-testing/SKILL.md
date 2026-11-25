---
name: sealeap-taotie-amazon-image-script-and-ab-testing
description: "Build a listing image script from competitor review insights and traffic keywords—relevance, value proposition and call to action in the first frames, then scenes, details, care and sizing with localized models—check platform image rules and visual-search recognizability, and validate two image sets through the platform's split-testing tool before committing. Use for 主图怎么做点击率、图片顺序怎么排、场景图要不要 AI 生成、变体缩略图、以图搜图流量、图片 A/B 测试怎么做、改图会不会影响排名、A+ 放什么. Do not use to produce final artwork or to run experiments without brand-registry eligibility."
---

# Amazon 图片脚本设计与 A/B 实验

## 目标

Build a listing image script from competitor review insights and traffic keywords—relevance, value proposition and call to action in the first frames, then scenes, details, care and sizing with localized models—check platform image rules and visual-search recognizability, and validate two image sets through the platform's split-testing tool before committing.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「平台不建议详情页使用 AI 环境图」「AI 素材适合广告」是来源转述的会议口径，需以当前图片政策原文核对，不作规则。
- 「移动端流量占约四分之三」「拆分测试不影响搜索排名」为来源经验或平台宣称，用本店业务报告与实验期间的排名观测校准。
- 评论摘要的人群与场景百分比是第三方或平台估算，标为 ESTIMATE；来源举例的服装品类细节不转译。
- 来源的摄影与设计服务推荐不采纳；本 Skill 只交付脚本与验证方法。

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

1. 先取证据：用评论分析工具类别或平台评论摘要读出人群、使用场景、未满足需求、好评点与差评点；再取本品与竞品的主要流量词，把高占比的修饰词（如无痕、透气）标为图片必须回答的问题。
2. 定三条信息：相关性（与搜索词一致）、价值主张（用户为什么关心）、行动号召（下一步买或比较）；每张图只回答一个问题，前三张必须覆盖价值主张与核心场景。
3. 排图片顺序并用满当前允许的图片位：主图白底且可被以图搜图识别，随后是核心价值场景、材质与工艺细节、洗护/使用方式（本地化习惯，如可机洗可烘干）、尺码与身材覆盖、颜色/组合；变体按款式或颜色建立才有缩略图，按尺码则没有。
4. 本地化模特与场景：覆盖不同肤色与体型，场景贴近目的国真实生活而非国内精修风；AI 换模特可用于 A+ 与副图，AI 合成环境用于详情页要按当前平台图片政策核对，广告素材另计。
5. 把超出图片位的信息放到 A+：品牌故事横幅、正/侧/背三视图配工艺说明、使用步骤与说明书类内容；移动端五点默认折叠，图片与视频优先于文字。
6. 新品初期准备两套风格不同的图片，在品牌备案后用拆分测试工具建立实验（对象可为主图/副图/标题/五点/A+），运行到样本足够（来源经验为数周至更长），读转化率与售出件数差异，胜出版本再做下一轮迭代。
7. 记录每轮实验的假设、变量、样本与结论，未达到样本量前不下结论；无实验资格时改为分时段单变量对照并标注证据等级更低。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品评论摘要、流量词占比与主图样式的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 评论洞察与流量词证据表
- 三条信息定义（相关性/价值/行动）
- 图片顺序脚本
- A+ 内容分工清单
- 拆分测试计划与结果记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
