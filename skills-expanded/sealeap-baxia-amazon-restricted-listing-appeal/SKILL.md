---
name: sealeap-baxia-amazon-restricted-listing-appeal
description: "Respond to an Amazon compliance flag that misclassifies a general-audience listing as a children's product by removing age-triggering language from the listing and filing a structured reinstatement appeal. Use for 非儿童品类被误判要求提交儿童合规文件、Listing含敏感年龄词汇的自查、被误判下架后的申诉邮件撰写. Do not use this appeal path for products that are genuinely marketed to or intended for children — those must complete real compliance requirements instead."
---

# Amazon 儿童品类误判申诉

## 目标

Respond to an Amazon compliance flag that misclassifies a general-audience listing as a children's product by removing age-triggering language from the listing and filing a structured reinstatement appeal.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 触发误判的具体关键词清单会随平台合规规则调整而变化，需以当前后台提示或政策页面为准，不能只套用一次性总结的词表。
- 误判涉及的品类范围是来源观察到的现象，不代表全部受影响类目，需按自己账户收到的具体通知判断适用范围。
- 申诉说明需要结合自己账户的真实情况改写，不能整段照抄同一模板，避免出现与实际产品不符的表述。

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

1. 收到合规文件要求或下架通知后，先确认产品设计与营销定位是否本就不面向儿童，若产品确实面向儿童则不走本流程。
2. 逐字检查标题、五点描述、产品描述与后台关键词，标出可能触发误判的年龄或人群相关词汇，逐条判断是否需要删除或改写。
3. 在详情页信息中补充清晰的目标受众说明与不适用低龄人群的提示，确保修改后的页面表述前后一致。
4. 修改生效后撰写申诉说明，逐条对应本次修改内容与整改结果，避免笼统陈述。
5. 提交申诉后跟踪处理结果，若被驳回需核对是否还有遗漏的敏感表述或图片文字，补充材料后再次申诉。
6. 把本次触发误判的具体词汇与页面位置记录下来，用于其余相似Listing的预防性自查。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 敏感词汇自查清单
- Listing修改前后对照记录
- 申诉说明文本
- 同类Listing预防性自查表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
