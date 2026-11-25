---
name: sealeap-athena-patent-document-analysis
description: "提取、核对或翻译专利摘要、著录事项、说明书、权利要求和附图。用于已有专利文献的解析，保留原文定位与翻译边界。"
---

# 专利文档解析与翻译

提取、核对或翻译专利摘要、著录事项、说明书、权利要求和附图。用于已有专利文献的解析，保留原文定位与翻译边界。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [专利摘要附图核对](references/capabilities/patent-abstract-figures/workflow.md) | 定位专利原始公开文件中的摘要附图，核对图号和对应技术说明 |
| [专利标题摘要翻译](references/capabilities/patent-abstract-translation/workflow.md) | 保留标题与摘要结构，逐句翻译并维护技术术语对照 |
| [专利著录事项核对](references/capabilities/patent-bibliography/workflow.md) | 核对申请人、发明人、日期、分类、优先权与公开授权文献关系 |
| [专利权利要求提取](references/capabilities/patent-claims-extraction/workflow.md) | 提取独立和从属权利要求，保留编号、引用关系和原文术语 |
| [专利权利要求翻译](references/capabilities/patent-claims-translation/workflow.md) | 保持限定语、编号、引用和开放/封闭式表述，制作逐项对照 |
| [专利说明书结构提取](references/capabilities/patent-description-extraction/workflow.md) | 按技术领域、背景、实施方式和附图说明提取相关段落并标定位 |
| [专利说明书翻译](references/capabilities/patent-description-translation/workflow.md) | 保留章节、附图标记和技术术语，完成原译对照并核查数值单位 |
| [专利完整附图核对](references/capabilities/patent-drawing-set/workflow.md) | 提取或定位所有目标附图，核对页码、图号和参考标记 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。按摘要、说明书、权利要求和附图选择参考；提取/翻译不替代法律解释。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
