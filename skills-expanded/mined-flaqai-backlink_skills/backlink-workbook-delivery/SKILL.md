---
name: backlink-workbook-delivery
description: "Deduplicate screened backlink candidates against history and frozen batches, assign configurable batches, build free and paid execution workbooks, and perform mechanical plus visual QA. Use after screening; do not research new sites or claim submission outcomes."
---

# 外链表格交付

把已经完成线路筛选的候选池变成可执行工作簿。此技能负责去重、批次冻结、费用分表、品牌显示、机械检查和视觉检查，不重新研究网站。

## 输入要求

每条候选至少有标准域名、完整 URL、投递条件、费用状态、适合品牌、来源和证据。批量线与质量线必须明确标记，不能混成无法追溯的总表。

## 去重和批次

按标准 URL、根域名和入口类型处理重复；与历史已投表、已导出批次和本次另一线路交叉检查。详细规则见 [references/dedup-and-batches.md](references/dedup-and-batches.md)。

## 工作簿

使用环境中的电子表格技能和工作簿工具创建或修改 XLSX。保留源文件并另存新版本。默认每个线路一个工作簿，包含“免费”和“付费”两个工作表；最终可见列为：域名、URL、投递条件、适合品牌网站。具体合同见 [references/workbook-contract.md](references/workbook-contract.md)。

若用户要求执行跟踪表，可在品牌下分别增加执行日期和执行情况列；未要求时不得擅自增加可见字段。

## 质量检查

1. 在生成工作簿前，对导出 CSV 运行 `scripts/validate_delivery_csv.py`。
2. 检查目标行数、空值、URL、重复、费用分组、品牌名称和历史冲突。
3. 重新导入生成后的工作簿，检查工作表名、列名、数据行、公式错误和隐藏辅助列。
4. 渲染并查看每张表顶部、底部和新增区域。视觉检查不能替代数据检查。
5. 输出质量检查报告，记录源文件、去重数量、最终行数和状态边界。

## 完成边界

最终文件只能称为“执行表”或“待执行候选表”。没有提交回执和公开页证据时，不得称为已投递、已发布或已收录。
