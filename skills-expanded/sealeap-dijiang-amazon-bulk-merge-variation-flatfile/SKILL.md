---
name: sealeap-dijiang-amazon-bulk-merge-variation-flatfile
description: "Merge several already-live standalone Amazon listings into a single parent-child variation family in one batch using the inventory flat-file template, mapping parentage, relationship, and variation-theme columns correctly, as an alternative to manually recreating listings from scratch. Use for 已经分开上线的listing怎么合并变体、批量模板怎么填父子关系、创建新品时要不要先勾选变体. Do not use to merge listings whose underlying products are not genuinely the same item differing only in the allowed variation attributes."
---

# Amazon 批量合并已上线变体

## 目标

Merge several already-live standalone Amazon listings into a single parent-child variation family in one batch using the inventory flat-file template, mapping parentage, relationship, and variation-theme columns correctly, as an alternative to manually recreating listings from scratch.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 批量模板的具体列名、可选值与所在位置会随类目与平台模板版本变化，操作前应以当前下载到的模板及其数据定义说明页为准，不套用来源里描述的列名顺序。
- 用模板合并已独立上线的listing是三种方式里最复杂、出错代价最高的一种（填错父子关系列可能导致listing异常），操作前建议先在非核心listing上小范围验证流程，再应用到主力listing。
- 合并变体只解决listing结构问题，不会自动统一或优化各子体原有的标题、图片与描述内容，仍需人工逐条检查是否需要调整为家族一致的呈现方式。
- 提前勾选“该商品有变体”这一预防性技巧的实际效果（是否真的能减少未来追加变体的步骤）应以当前后台实际流程验证为准，不同类目/时期可能有差异。

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

1. 新建商品且未来可能有多规格时，即使当前只上线一个规格，也在创建流程里提前勾选“该商品有变体”，即便先不填具体变体值，也能大幅简化未来追加变体的步骤，避免事后走更复杂的合并路径。
2. 若已有一条独立上线的listing、现在想给它加变体，优先尝试后台自带的“创建变体”向导直接在该listing基础上转换，这条路径比批量模板更简单，适用于“从一条已有listing派生出其他规格”的场景。
3. 若已有多条完全独立上线的listing需要合并为同一个变体家族，下载当前类目对应的库存文件模板，此时才需要用批量模板方式处理，而不是逐条手动改。
4. 在模板中新增一行作为父体记录：自定一个便于识别的父体SKU，填入品牌名称，并将更新类型标记为“局部更新”，避免覆盖这些listing已有的其他字段。
5. 对每一行（含父体与各子体）填写“父子关系”列（父体填parent、子体填child）与“关联父体SKU”列（父体本行留空，各子体填对应父体SKU），并统一填写“变体主题”列（如“尺寸+颜色”），子体行填写对应的具体变体属性值。
6. 核对模板中数据定义说明页，逐列确认格式无误后保存并上传；上传后等待处理完成，在库存管理页面确认这些原本独立的listing已经按父子结构分组显示，而不再是各自独立的一行。
7. 合并生效后逐一进入每个子体核对标题、图片、描述等信息是否仍然贴合各自的具体规格，因为合并动作本身不会自动帮你优化这些内容，需要人工检查调整。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 变体预留勾选/合并路径判断
- 库存合并模板填写记录
- 父子关系与变体主题列核对表
- 合并后各子体内容一致性核查结果
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
