---
name: sealeap-zouwu-amazon-aplus-content-build
description: "Plan and assemble an A+ (enhanced) product description in Amazon's A+ Content Manager: choose a module sequence informed by category leaders, prepare images that meet each module's size rules with alt text, configure the comparison module with the brand's own ASINs, apply to ASINs, and pre-check before submitting for approval. Module names and limits follow the current console. Use for A+ 页面怎么做、图文详情页模块、A+ 图片尺寸、对比模块放自家 ASIN、A+ 审核被拒、替代文本怎么写. Do not use for accounts without brand registry eligibility or to make claims the product evidence cannot support."
---

# Amazon A+ 页面模块规划与提交预检

## 目标

Plan and assemble an A+ (enhanced) product description in Amazon's A+ Content Manager: choose a module sequence informed by category leaders, prepare images that meet each module's size rules with alt text, configure the comparison module with the brand's own ASINs, apply to ASINs, and pre-check before submitting for approval. Module names and limits follow the current console.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「A+ 能提高购买欲望、对比模块能留住流量并省广告费」是来源经验判断，需用上线前后同口径的 CVR 与页面指标验证，不作既定结论。
- 模块数量上限、图片尺寸要求与可用模块类型随站点与版本调整，以当前 A+ 管理器提示为准。
- 参考头部商品的模块结构只作布局启发，不复制其文案与图片。

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

1. 先确认资格与对象：账户已有品牌备案且目标 ASIN 归属该品牌；在广告菜单下的 A+ 内容管理器中区分基础增强描述与品牌故事等类型，首次先做基础版；内容名称只作内部备注。
2. 观察本类目头部商品的 A+ 结构（大场景图、场景与卖点模块、细节图组、对比模块），记录其模块数量与顺序作为参考，再结合本品五点选出要放大的少数几个卖点。
3. 规划模块：在当前允许的模块数上限内按内容量决定数量（来源经验通常三到四个）；每个模块记录用途、标题、副标题、正文与要点，正文从五点改写而非复制；可安排一个品牌介绍模块放 Logo 与品牌描述。
4. 图片按每个模块的最低尺寸要求准备（小于要求无法上传，超出会被压缩），上传后为每张图填写替代文本（品牌 + 品名 + 图片内容），可复用图片库中已上传的素材。
5. 对比模块填入自家其他 ASIN 与简短标题，设置可比指标（材质、功能、适用场景等），核对显示选项；评分不理想的商品可选择不展示评分。
6. 应用到 ASIN 并在提交前预检：违禁词、无法证实的宣称、图片内文字与模块留空；提交后跟踪状态（审核中/已批准/被拒），被拒时按原因修改重提。
7. 批准上线后回读前台页面：模块顺序、图片与文字、对比模块链接是否正确，并记录上线时间供后续转化对比。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取本类目头部竞品 A+ 页面模块结构与卖点组织方式的公开页面观测，作为布局参考。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- A+ 模块结构规划表
- 图片规格与替代文本清单
- 对比模块配置表
- 提交预检与审核状态记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
