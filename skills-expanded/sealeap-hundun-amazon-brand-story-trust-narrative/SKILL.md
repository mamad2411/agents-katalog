---
name: sealeap-hundun-amazon-brand-story-trust-narrative
description: "Design a trust-building narrative structure for a differentiated or premium-priced product's Brand Story and A+ content, covering discovery context, the pain point addressed, material or sourcing rationale, team background and customer outcomes, for cases where a plain spec-sheet page under-communicates positioning, without fabricating claims the seller cannot substantiate. Use for 客单价高但转化差、产品卖点需要讲故事、品牌故事写什么内容、详情页太像参数表、如何建立买家信任感. Do not use for standard low-differentiation commodity listings where spec-forward pages already convert, or to write unverifiable origin, health or efficacy claims."
---

# Amazon 品牌故事信任叙事设计

## 目标

Design a trust-building narrative structure for a differentiated or premium-priced product's Brand Story and A+ content, covering discovery context, the pain point addressed, material or sourcing rationale, team background and customer outcomes, for cases where a plain spec-sheet page under-communicates positioning, without fabricating claims the seller cannot substantiate.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源用具体案例的粉丝量与转化效果作为叙事有效性的证明，属于个案观察；实际效果需在自身账户用转化率对比验证，不预设提升幅度。
- 来源提出“高客单非标品在标准电商货架式页面上卖不动”的判断是对特定场景的经验总结，不同市场与品类的承载力应分别验证，不作为普遍规律套用。
- 品牌故事内容必须与产品真实信息一致；为了塑造神秘、稀缺人设而编造来源、工艺或功效，属于虚假宣传风险，不采用。
- 独立站与平台详情页的呈现规则和买家浏览习惯不同，独立站的叙事设计经验搬到 A+/品牌故事时需按当前模块限制重新适配，不能整页照搬。

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

1. 先判断产品是否属于需要叙事的类型：客单价明显高于同类目、购买决策依赖信任而非纯参数比较（如工艺品、文化周边、非标定制品）；若产品是标准化刚需品，参数与价格对比往往比故事更有效，不强行套用叙事结构。
2. 梳理五类叙事素材：发现契机、用户痛点、选材/工艺依据、团队背景、客户故事，逐项收集真实素材，缺项标注待补充而非编造。
3. 把素材组织进 Brand Story 与 A+ 模块：按“发现—痛点—方案—团队—验证”的顺序编排卡片，让买家在浏览过程中建立起品牌可信度，而非中途跳出，不是简单堆砌参数图。
4. 核对每条叙事表述的可证实性：凡涉及产地、工艺、功效或稀缺性的描述，需能对应真实的采购凭证、检测报告或产品事实；无法证实的表述改写为中性描述或删除。
5. 视觉与文案统一人设：确保图片场景、模特/道具风格与文案语气一致，避免页面看起来仍是通用货架风格；如同时经营独立站，两端叙事保持一致但各自适配平台呈现形式。
6. 上线后用转化率与详情页停留/跳出等可获得的指标做前后对比，控制价格与广告投放不变的情况下观察叙事改版是否带来可归因的转化变化，不达预期则复盘素材真实性与叙事顺序。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 叙事素材收集表（发现/痛点/选材/团队/客户故事）
- Brand Story 与 A+ 模块编排草案
- 表述可证实性核查记录
- 视觉与文案一致性检查清单
- 上线前后转化对比记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
