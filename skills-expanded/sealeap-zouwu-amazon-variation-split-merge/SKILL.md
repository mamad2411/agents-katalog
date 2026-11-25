---
name: sealeap-zouwu-amazon-variation-split-merge
description: "Split child ASINs out of a parent or merge children into an existing or new parent on Amazon using console deletion and the category inventory template: confirm the variation theme, fill parentage rows correctly, upload, then read back the resulting family structure. Adapts to whatever the current template columns and console options are. Use for 变体拆分、变体合并、子体并入父体、新建父体合并、批量上传模板怎么填、变体主题选哪个、拆出单个子体. Do not use to merge unrelated products into one family to pool reviews, or to restructure ASINs the account does not own."
---

# Amazon 变体拆分与合并批量操作

## 目标

Split child ASINs out of a parent or merge children into an existing or new parent on Amazon using console deletion and the category inventory template: confirm the variation theme, fill parentage rows correctly, upload, then read back the resulting family structure. Adapts to whatever the current template columns and console options are.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 拆分与合并的生效时间（来源约数分钟到数十分钟）和可用操作项随控制台版本变化，等待时以处理报告状态为准，不以固定时长判断失败。
- 直接删除单个子体的拆分方式在来源中被标注为受政策变化影响，是否仍可用需在当前账户验证；删除操作可能影响报价与库存，先小范围试验。
- 模板列名与顺序随类目和站点不同，不得照搬其他类目的模板；变体主题必须在类目允许的主题范围内。
- 不采用把不同产品硬并成一个变体家族的做法；合并对象必须是同一产品的真实规格差异。

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

1. 先在库存管理中记录现有父子关系：父体 SKU/ASIN、每个子体 SKU/ASIN、当前变体主题与各子体的主题值；明确本次目标是拆出全部子体、拆出部分子体、子体并入已有父体，还是多个独立商品合并到新父体。
2. 拆出全部子体：只选中父体（不选子体）执行删除商品信息，等待系统处理后回读，确认各子体已独立存在且报价未受影响；操作项名称以当前控制台为准。
3. 拆出部分子体：优先采用「先全部拆出，再把需要保留的子体合并回父体」的两段式路径；若当前控制台仍支持在编辑页直接删除单个子体，先在测试对象上验证再批量做。
4. 合并到已有父体：从目录批量上传下载当前类目的商品模板，只填必要列：SKU、更新类型（部分更新）、ASIN、父子关系列（父/子）、父体 SKU、变体关系、变体主题，以及子体的主题值（如颜色）；父体行不填父体 SKU。
5. 合并到不存在的父体：在模板首行新建父体（全新 SKU、全部更新、标题、品牌、类目节点，无 GTIN 时需先取得豁免），描述与要点等字段不留空以免报错，子体行的父体 SKU 指向该新 SKU；原产地、电池、危险品等合规列按实际填写。
6. 上传前逐行复核：同一父体下变体主题一致、子体主题值不缺、SKU/ASIN 与当前库存一致；上传后查看处理报告，等待完成再刷新库存页。
7. 回读结果：父体下子体数量与预期一致、未纳入的子体仍独立、前台变体选择器显示正确；不一致时按处理报告的错误信息修正后重传。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 变体结构现状与目标结构对照表
- 批量上传模板填写清单
- 处理报告与错误修正记录
- 变体结构回读结果
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
