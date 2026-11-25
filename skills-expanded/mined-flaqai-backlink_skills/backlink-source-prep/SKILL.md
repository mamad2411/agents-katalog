---
name: backlink-source-prep
description: "Prepare traceable backlink source data from Semrush organic competitors, Backlink Gap, referring-domain exports, local workbooks, and public lists. Use for source acquisition, inventory, normalization, consolidation, exclusion, and priority compression; stop before final site screening or submission."
---

# 外链源表整理

把分散的竞品和外链导出整理成可追溯、可压缩、可继续筛选的标准源表。原始文件永不覆盖；所有派生文件另存。

## 三种模式

- **文件导入**：用户已提供 CSV/XLSX，只做登记、读取和整理。
- **浏览器导出**：只有得到明确授权才操作 Semrush；不使用爬虫替代产品导出。
- **离线整理**：读取已有导出，生成合并候选、排除表、优先候选和统计报告。

需要浏览器导出时，先读 [references/semrush-export.md](references/semrush-export.md)。处理字段和压缩规则时，读 [references/source-schema.md](references/source-schema.md)。

## 工作流程

1. 为每个源文件登记目标域名、报告类型、数据库、报告日期、导出日期和文件名。
2. 从自然搜索竞品中综合相关度、共同关键词、自然流量和主题适配选择参考竞品。指标决定优先顺序，不设单一严格淘汰线。
3. 按工具允许的比较数量分批导出反向链接差异或引荐域名；记录批次号和竞品槽位。
4. 运行 `scripts/audit_semrush_exports.py` 检查文件数、行数、空表、表头差异和读取错误。
5. 标准化目标域名、来源竞品和引荐域名；保留原始值与来源文件。
6. 先排除自有域、竞品自身域、明显短链、赌博、恶意、镜像和没有研究价值的噪声，再生成优先候选。
7. 输出总量、唯一域名数、目标覆盖数和各排除原因，不能只给压缩后的数字。

## 优先候选

优先级可以参考目标覆盖数、竞品覆盖数、链接实力、自然流量和主题信号，但不得把单个第三方分数当作最终质量结论。高权重通用站不自动成为可投递平台；低权重垂直目录也不自动淘汰。

## 交接

至少交付：原始文件登记、合并候选、排除表、优先候选、统计报告。文件名后缀应带数据量，例如 `合并去重候选-<行数>条.csv`。此阶段不得把结果写成“已找到外链平台”或“已核验可投递”。
