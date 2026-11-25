---
name: sealeap-chiwen-amazon-ai-ad-creative-review-gate
description: "Batch-generate advertising images and a short product-showcase video from an existing product photo and text prompts using the ad platform's native AI creative tools, on the marketplaces where those tools are enabled. Routes every generated asset through a manual compliance review before publishing, since AI output can misrepresent product features, specs, or on-image text. Use for 批量做广告图/广告视频、AI 生成创意素材、品牌推广视频广告制作、素材预算不够时批量补图. Do not use to publish generated assets without human review, or to keep any version that shows a function, spec, or on-image claim the product does not actually have."
---

# Amazon AI广告素材生成与合规审核

## 目标

Batch-generate advertising images and a short product-showcase video from an existing product photo and text prompts using the ad platform's native AI creative tools, on the marketplaces where those tools are enabled. Routes every generated asset through a manual compliance review before publishing, since AI output can misrepresent product features, specs, or on-image text.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- AI 生成入口开放的站点范围、单次生成数量上限、是否为测试阶段功能等均可能随后台更新调整，以当前实际界面为准，不代入固定数字。
- 生成图片或视频存在编造产品未具备的功能、参数或文字的风险，人工审核是必需环节，不能因追求效率或素材紧缺而跳过。
- 系统自动提示词只是起点，多个商品直接套用同一套提示词容易导致素材同质化，需结合商品差异调整后再生成。

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

1. 确认目标广告位（品牌推广、展示型推广、品牌旗舰店、创意素材工具、DSP 等）与目标站点是否已开放 AI 图片或视频生成入口，开放范围以当前后台为准，不同站点、不同时期可能不同。
2. 选定要生成素材的商品，用开放式文字描述所需画面元素、背景与风格；可先用系统给出的自动提示词作为起点，再手动调整而非直接照搬默认结果。
3. 同一商品生成多版本结果后逐张比对，只保留画面、参数、文字与商品真实属性一致的版本，凡出现捏造功能、虚构数据或错误文字的版本一律弃用。
4. 需要品牌推广视频广告时，按目标选择、广告格式与落地页设置、素材模块生成或上传视频的顺序创建广告，视频与静态图分开走完整校验流程。
5. 生成结果进入人工审核环节：逐项核对画面文字、功能演示、参数标注是否与商品详情页一致，任何夸大或捏造内容打回重做，不带着侥幸心理上线。
6. 审核通过的素材归档到创意素材库，同时记录对应的商品、提示词与风格选择，便于后续复用与出现问题时追溯来源版本。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- AI生成广告素材候选集（图片/视频）
- 人工审核记录（通过/打回原因）
- 品牌推广视频广告创建清单
- 素材归档记录（商品/提示词/风格对应关系）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
