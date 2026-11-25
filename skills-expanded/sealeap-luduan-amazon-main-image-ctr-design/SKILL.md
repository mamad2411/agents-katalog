---
name: sealeap-luduan-amazon-main-image-ctr-design
description: "Audit an Amazon main image and image set against the current marketplace image requirements, then design differentiation across usage scene, size reference, material cues, feature highlights and packaging, producing a revision brief with a single-variable CTR verification plan instead of asserting that images move organic rank. Use for 主图怎么做、主图点击率低、主图规范核对、副图放什么、主图差异化、图片被盗用怎么开 case. Do not use to claim image changes directly move organic ranking, or to upload or replace live images without approval."
---

# Amazon 主图合规核对与点击率设计

## 目标

Audit an Amazon main image and image set against the current marketplace image requirements, then design differentiation across usage scene, size reference, material cues, feature highlights and packaging, producing a revision brief with a single-variable CTR verification plan instead of asserting that images move organic rank.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源把“主图影响点击率、点击率影响排名”当作确定因果；本 Skill 只把 CTR 变化作为账户内观测，对排名的影响记为待验证假设，需在控制价格、促销与广告投放后再看。
- 来源给出的图片像素下限、产品占比和可上传张数是特定时点的规范摘录，可能已变化；一律以当前站点后台的图片要求为准。
- 来源把绿色代表环保、金色代表高级当作通用配色规则，这是与市场和品类相关的经验假设；应结合目标站点消费者认知与同类目对照验证，不作为默认设计规则。
- 来源提到的替换 logo 直接使用他人图片属于侵权，不采用；所有图片必须为自有拍摄或已获授权的素材。

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

1. 先固定对象与基线：站点、ASIN/变体、当前主图与副图序列、近期曝光/点击/CTR（广告报告或业务报告口径）与同期价格、促销、库存记录；缺基线标 NEEDS_EVIDENCE，不凭观感断言“主图差”。
2. 按当前站点的图片规范逐条核对主图硬性项：是否纯白底、产品占画面比例、最短边与最长边像素、是否含文字/logo/水印/多余道具、是否展示非售卖附件、可上传张数；条款与阈值以当前卖家后台的图片要求页为准，来源给出的像素与占比只作参考。任一硬性项不达标先修，再谈创意。
3. 抓取同类目头部与相邻价位的公开 Listing 图片序列做对照表：逐家记录是否有使用场景图（手持/摆放/运行中三类）、尺寸参照物图、材质特写、基本功能与独有亮点图、包装图；标出本品缺失的类型与全类目同质化最重的类型。
4. 从四个维度写差异化假设：颜色/外形能否与同类目的同色同形产品区分、场景是否表达真实使用方式、材质与环保/高级概念如何用画面而非文字表达、基本功能与独有亮点如何各占一张图；每条假设注明依据（产品事实、评论中被反复提及的关注点），不把来源的配色寓意当规律。
5. 拍摄与制作路径二选一并记录成本：自拍（小型摄影棚、近年机型手机、自行后期）或外包拍摄加修图；无论哪种，原始文件、拍摄时间与源工程文件归档保留，作为日后图片被盗用时的权属证据。
6. 发现图片被盗用时，通过卖家后台的帮助/支持入口（以当前控制台为准）提交侵权申诉，逐项核对字段：本品 ASIN、涉嫌侵权 ASIN、被盗图片与原始文件证据、创作时间、联系方式与沟通渠道；申诉编号与回复写入案件台账并跟踪。
7. 上线改版前做单变量实验：只换主图、其余图片/价格/广告不动，记录基线 CTR、观察窗、成功与回退条件；观察期内 CTR 与转化同步改善才保留，只涨点击不涨转化要复查画面是否造成误导。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取同类目头部 Listing 的公开图片序列与评论中的关注点，作为主图差异化对照的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 主图硬性规范核对表（按当前站点要求逐条核对）
- 同类目图片序列对照表（场景/参照/材质/亮点/包装）
- 四维差异化假设清单与每张图的任务分工
- 主图改版方案与单变量 CTR 验证计划（基线/观察窗/回退）
- 图片权属证据归档与侵权申诉记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
