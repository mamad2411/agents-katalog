---
name: sealeap-jiaotu-amazon-ai-content-disclosure-audit
description: "Turn mandatory AI-generated-content disclosure into a repeatable audit: verify the current labeling requirement and enforcement stance in Seller Central first, then check that AI-produced images retain generation metadata, add a disclosure flag where a platform declaration field exists, and sweep all listing assets (images, A+, description, video) for undisclosed AI content. Treats the exact detection method and enforcement severity as unverified until confirmed against current policy pages. Use for AI生成图片下架排查、AI内容标注合规、A+页面AI审核、上新前AI素材自查、存量Listing AI内容补标. Do not use to strip or fake metadata to evade detection, and do not assume a listing is safe just because it rendered normally in preview."
---

# Amazon AI内容合规标注自查

## 目标

Turn mandatory AI-generated-content disclosure into a repeatable audit: verify the current labeling requirement and enforcement stance in Seller Central first, then check that AI-produced images retain generation metadata, add a disclosure flag where a platform declaration field exists, and sweep all listing assets (images, A+, description, video) for undisclosed AI content. Treats the exact detection method and enforcement severity as unverified until confirmed against current policy pages.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源描述的具体检测手段（像素特征扫描、透视分析、元数据字段清单）是其观察或推测，平台实际检测方法未公开，不能反向设计规避方式，也不能假设检测一定或一定不会命中。
- "诚实标注不影响搜索排名"是来源转述的说法，是否有隐性权重影响缺乏可验证数据，按自身账户实际排名表现观察，不默认为保证。
- 处罚阶梯（限制展示、强制下架、账户健康分影响）会随政策版本调整，具体触发门槛和后果以当前账户收到的实际通知和后台状态为准，不作为固定规则记忆。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、产品事实、品牌语气和当前政策约束
- 已授权的 Listing、关键词、评论/VOC、图片和竞品证据
- 每项数据的来源、时间、站点、样本和限制
- 人工审核人、发布边界和不可生成的声明或视觉特征

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先到卖家后台政策公告与帮助页确认当前是否存在强制性AI内容标注要求、覆盖哪些素材类型（图片/视频/文案/A+）、判定与处罚口径，避免按旧版或转述规则执行。
2. 对使用AI工具生成的图片，检查生成软件是否已在文件中保留标准化生成信息；未保留的，用具备该功能的图像工具或专门的元数据工具补充嵌入，避免在压缩、转码环节把标记信息丢失。
3. 若后台提供AI内容声明选项，对确实使用AI生成或深度改写的素材如实勾选，包括图片、A+信息图、经AI改写的产品文案和视频，不因担心排名下滑而漏报。
4. 对已上架的存量Listing做一次全店排查：逐个检查主图、辅图、A+模块、文案与视频是否有未声明的AI生成或AI辅助内容，建立台账记录处理状态。
5. 把生成记录（原始生成文件、对话记录或工具导出日志）按素材归档保留，作为后续被要求举证时的依据，保留期限参考当前官方审核追溯期。
6. 把"生成即打标、上传前自检"写入内部素材制作SOP，明确谁负责在上传前做最后一次标注核对，防止流程断点导致新素材再次漏标。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 当前AI内容标注规则核对记录
- 素材元数据补标处理清单
- 全店AI内容声明审查台账
- 生成记录归档规范
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
