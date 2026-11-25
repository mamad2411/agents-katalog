---
name: sealeap-hundun-amazon-flatfile-merge-split-listings
description: "Use an inventory flat-file template to merge multiple already-live, same-brand, same-category listings into one parent/child variation family, or split an existing family back into standalone listings, by setting the correct parent/child SKU references and update-mode flags. Applies only within a single brand and category; never fabricates identifiers. Use for 表格合并变体、批量拆分变体、listing怎么用表格设置成变体、parent sku怎么填、update和部分更新怎么选. Do not use across different brands or unrelated categories, and do not use this for a one-off single-listing merge (use the interactive per-listing workflow for that)."
---

# Amazon 表格批量合并拆分变体

## 目标

Use an inventory flat-file template to merge multiple already-live, same-brand, same-category listings into one parent/child variation family, or split an existing family back into standalone listings, by setting the correct parent/child SKU references and update-mode flags. Applies only within a single brand and category; never fabricates identifiers.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 上传前建议先用单个或小批量 listing 验证表格字段是否正确，因为部分账户版本的“库存文件校验”功能不一定可用，错误可能要等上传后才能通过报错报告发现。
- “更新”模式会用表格里出现的字段整体覆盖对应 listing，未出现在表格中的字段可能被清空；只要不是要整体重建，都优先用“部分更新”。
- 合并操作把子体并入家族后，子体原有的标题、五点、描述等内容存在被附体内容覆盖的风险，建议合并前先备份子体原有内容。

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

1. 合并或拆分前先确认所有目标 listing 品牌一致、类目一致；品牌或类目不一致的不能用同一变体家族合并，需先各自修正。
2. 按目标产品类目下载对应的库存批量表模板，在表格中新建一行作为附体（parent），其余每行对应一个已存在的子体（child）。
3. 附体行的 SKU 自定义命名，子体行的 SKU 必须与该 listing 当前已生效的 SKU 完全一致；子体商品编码列填写其 ASIN，而不是 UPC/EAN。
4. 在变体关系列为附体填写 parent、为子体填写 child，并按产品属性选择正确的变体主题（如颜色，或颜色加尺寸）。
5. 更新方式列：附体（新建的父级关系）选择“更新”（完整写入），已存在的子体行选择“部分更新”，避免用错模式把子体已有字段清空。
6. 如需把家族拆分回独立 listing，同样下载模板、填入附体与要拆分子体的 ASIN，把附体行的更新方式改为“删除”，子体保持部分更新，上传后子体会与家族解除关系。
7. 上传表格后按当前后台节奏等待生效，生效后到前台核对变体数量、每个子体的价格与关键信息是否仍然完整。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 变体合并/拆分用批量表格文件
- parent/child SKU 与 ASIN 对照表
- 更新方式（update/部分更新/delete）设置记录
- 上传后前台核验记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
