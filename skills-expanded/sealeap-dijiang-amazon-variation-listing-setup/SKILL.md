---
name: sealeap-dijiang-amazon-variation-listing-setup
description: "Set up an Amazon parent-child variation listing by first creating compliant child listings, then linking them through a parent record with matching identifiers, pricing, and required attributes, verifying the family renders correctly before treating it as live. Use for 建立变体listing、父子listing怎么关联、颜色尺码变体怎么做、变体信息填错怎么排查. Do not use to force unrelated products into one variation family purely to share reviews or ranking."
---

# Amazon 变体Listing建立流程

## 目标

Set up an Amazon parent-child variation listing by first creating compliant child listings, then linking them through a parent record with matching identifiers, pricing, and required attributes, verifying the family renders correctly before treating it as live.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 变体处理时效以官方当前说明为准，来源经验中的具体分钟/小时数仅供参考，不同类目、不同时期可能不同。
- 强行把差异较大的商品塞进同一变体家族（超出官方允许的“仅在颜色/尺寸等受限属性上不同”范围）可能被判定违反变体政策，导致父体被拆分或受限，应先以官方变体政策为准再决定是否适合做成变体。
- 复制已有子体生成父体、或用向导直接转换现有listing为父体，两者对已有评论与排名历史的影响可能不同，操作前应先在小范围或非核心listing上验证效果，而不是直接在主力listing上试错。
- 第三方条码（非官方渠道购买、可能被多次转卖或与其他品牌关联过的条码）存在被系统判定异常的风险，商品编码建议从官方认可的条码颁发机构获取。

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

1. 先确认目标类目在该站点支持的变体主题（如颜色、尺寸、颜色+尺寸、气味/材质等），不同类目可选主题不同，需在实际创建界面核对，而不是套用其他类目的经验。
2. 为每个规格分别创建完整、独立可售的子体 Listing（各自有合规的商品编码、标题、图片、定价、库存/发货方式），逐一检查每条子体的必填信息是否完整。
3. 建立父体记录：可选择新建空白父体、复制已有子体转为父体、或用官方创建变体的向导直接转换，三种方式均可，选择时以“是否会改动已产生的评论与排名历史”为判断依据，优先选不影响现有子体历史数据的方式。
4. 在父体的变体信息里逐一录入每个子体的商品编码与所选变体属性值，并检查系统返回的关联确认提示（通常会显示已匹配到哪条子体listing的标题），出现不匹配要立即修正而不是提交后再排查。
5. 核对父体与各子体之间需要保持一致的字段（如价格需与子体实际售价一致、制造商编号等），避免父体内填写与子体实际不符的信息导致审核异常。
6. 提交后按官方处理时效等待生效，生效后在前台与后台各自核查：前台看是否正常展示变体选择器与图片，后台库存管理里看是否已按父子结构分组显示，如未按预期分组要回到变体信息里排查具体哪个属性值或编码填错。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 子体 Listing 完整信息核对表
- 父子变体关联操作记录
- 变体字段一致性检查清单
- 上线后前台/后台核验结果
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
