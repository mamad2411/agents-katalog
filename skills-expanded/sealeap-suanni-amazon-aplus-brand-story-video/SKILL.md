---
name: sealeap-suanni-amazon-aplus-brand-story-video
description: "Prepare, submit and verify Amazon A+ content, Brand Story and product video for a listing: confirm eligibility and module set, benchmark competitor page structure, brief creative assets in the required desktop and mobile sizes, apply to ASINs and check the live page after approval. Use for A+ 怎么上传、基础 A+ 和高级 A+ 区别、品牌故事怎么做、产品视频上传、A+ 图片尺寸、美工做图需求、视频审核后没显示. Do not use to write A+ claims that cannot be substantiated or to upload images, video or copy you do not hold rights to."
---

# Amazon A+ 品牌故事与视频上架准备

## 目标

Prepare, submit and verify Amazon A+ content, Brand Story and product video for a listing: confirm eligibility and module set, benchmark competitor page structure, brief creative assets in the required desktop and mobile sizes, apply to ASINs and check the live page after approval.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的模块数量、图片像素尺寸、视频格式与体积上限、审核时长都是某一时期的后台规则，以当前上传页面的实时提示为准。
- “A+、品牌故事与视频能显著提升转化”在来源中是经验断言；实际影响以自身账户上线前后的转化率对比（控制价格、广告与库存）验证，不预设幅度。
- 对标竞品只借鉴模块结构与信息组织方式，不得复制其图片、文案或宣称；A+ 内容需符合平台内容政策，避免不可证实的宣称。
- 后台入口位置与模块名称会随改版变化，本 Skill 只提供顺序与检查项，操作以当前页面为准。

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

1. 先确认资格与入口：品牌是否已完成注册（品牌故事与 A+ 依赖品牌资格）、账户能创建的是基础 A+ 还是高级 A+（版本决定模块数量、模块尺寸以及是否有视频、问答等模块），以当前后台目录与广告菜单下的入口为准。
2. 对标优秀竞品的公开详情页：记录其 A+ 用了几个模块、各模块类型（大图带标题、多图对比、问答等）、品牌故事有哪些卡片、视频位是卖家视频还是红人/买家视频；把这个结构作为自己的版式草案，不复制其图片与文案。
3. 把版式转成给美工的素材需求单：每个模块的图片尺寸按后台当前提示；高级 A+ 与品牌故事背景图需要桌面端与移动端两套尺寸，需求单里分别列出；视频按后台允许的格式与体积上限、封面按推荐比例，清晰度尽量高。
4. 上传时逐项填齐：视频名称（会显示在前台）、对应 ASIN、品牌、站点语言与封面；A+ 每张图片填写与产品相关的图片关键词；品牌故事先上传固定背景模块再添加其余卡片。
5. 提交前用后台预览分别检查桌面端与移动端显示（裁切、文字可读性、模块顺序），确认关联 ASIN 列表完整（含变体）后再提交审核。
6. 审核通过后到前台回查：视频是否出现在图片区、A+ 与品牌故事是否在描述区展示、移动端是否正常；未展示或被驳回时按原因修改重提，并把最终版本与上线日期记入 Listing 变更记录，便于后续归因转化变化。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取竞品公开详情页的 A+、品牌故事模块结构与视频位，作为版式对标。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 资格与 A+ 版本确认记录
- 竞品版式对标表（模块、卡片、视频位）
- 美工素材需求单（含桌面端/移动端尺寸）
- 提交与前台回查记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
