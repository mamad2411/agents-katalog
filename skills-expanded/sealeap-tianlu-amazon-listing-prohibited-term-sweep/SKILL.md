---
name: sealeap-tianlu-amazon-listing-prohibited-term-sweep
description: "Sweep listing title, bullet points, A+ content, image and video text overlays, and backend search terms against the current prohibited-term categories from Seller Central policy, tag each hit by risk tier, and route fixes through a scheduled recheck cadence calibrated to account risk. Historic and inactive variants are included in the sweep since policy enforcement can reach dormant listings. Use for Listing违禁词自查、五点/A+/图片水印文案审查、上新前合规检查、历史停售链接排查. Do not use to bypass or game keyword filters, or to assume a fixed prohibited-word list without checking current policy."
---

# Amazon Listing违禁词分级自查

## 目标

Sweep listing title, bullet points, A+ content, image and video text overlays, and backend search terms against the current prohibited-term categories from Seller Central policy, tag each hit by risk tier, and route fixes through a scheduled recheck cadence calibrated to account risk. Historic and inactive variants are included in the sweep since policy enforcement can reach dormant listings.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 具体违禁词清单与判定口径由平台持续更新，来源列举的类别仅作排查方向参考，实际命中判定以账户当前后台提示与官方政策文本为准。
- 系统扫描与人工复核的具体触发机制、命中后果与处罚等级未经官方文本证实，属于来源观察总结，需按实际收到的系统提示或绩效通知调整应对方式。
- 复查频率、认证类用语的举证标准应按自身类目风险与历史整改记录校准，来源给出的节奏仅作起点参考，不是固定规律。

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

1. 在卖家后台核对当前 Listing 合规政策与禁限用语说明的最新版本，记录检查口径与适用范围，不沿用旧版印象或他人经验列表。
2. 按标题、五点描述、A+ 内容文案、图片/视频中的文字水印与字幕、后台 Search Terms 五个字段逐一导出待查文本，含在售、停售与废弃变体，形成统一检查表。
3. 用当前政策口径把命中词按风险类别打标（如医疗/治疗类用语、绝对化承诺、认证声称、平台或商标近似词、促销与物流承诺用语等），优先处理与账户历史整改记录或类目高敏感度相关的类别。
4. 对命中项按是否有证据支持分流：能提供有效凭证的认证类表述保留并附证据来源，其余一律改写为中性、可验证的事实性描述。
5. 制定固定周期的复查计划，并在大促或批量上新前加密检查频率；每次复查结果与处理记录留痕，便于追溯。
6. 若已被系统判定下架或限制，先停用命中内容、保留修改前后对比记录，再按官方要求准备申诉材料，不在未核实前批量删改造成证据缺失。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 五字段命中清单（SKU/字段/命中词/风险类别）
- 违禁用语分级整改优先级表
- 改写前后对照与证据留痕记录
- 复查周期计划与触发加密条件清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
