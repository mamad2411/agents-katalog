---
name: sealeap-athena-amazon-listing-management
description: "处理已授权 Amazon 店铺的商品属性、目录、A+、媒体、批量提交及价格任务。支持现状核对、字段草稿和范围明确的写入，每种动作保留验证与回读要求。"
---

# Amazon Listing、素材与定价管理

处理已授权 Amazon 店铺的商品属性、目录、A+、媒体、批量提交及价格任务。支持现状核对、字段草稿和范围明确的写入，每种动作保留验证与回读要求。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon 商品管理](references/capabilities/amazon-account-product/workflow.md) | 读取商品现状与当前类目 schema，生成字段级变更预览，验证后执行授权范围并回读 |
| [Amazon 目录商品核对](references/capabilities/amazon-account-catalog/workflow.md) | 读取平台目录及变体关系，核对实体标识与属性来源 |
| [Amazon 批量数据提交](references/capabilities/amazon-account-feeds/workflow.md) | 本地核对 schema、重复 SKU 与记录数，再上传并提交已授权批次，解析逐条处理结果 |
| [Amazon 素材上传](references/capabilities/amazon-account-uploads/workflow.md) | 检查文件格式和用途，使用正式上传能力提交已授权文件并回读上传状态 |
| [Amazon A+ 内容管理](references/capabilities/amazon-account-aplus-content/workflow.md) | 先核对资格与模块限制，编写内容草案并预检，发布后跟踪审核与 ASIN 关联 |
| [Amazon 价格核对与变更](references/capabilities/amazon-account-pricing/workflow.md) | 读取现价和促销叠加，测算授权价格变化后逐 SKU 提交并回读生效值 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。查询、草稿、上传、批量提交与价格修改分别路由；明确每次外部写入的对象和授权。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
