---
name: data
description: 统计、筛选和汇总明确指定的 CSV、TSV、JSON、JSONL、Parquet 本地表格数据。
---

# 本地数据分析

使用 CLI data 或 MCP query_local_data，明确指定一个输入文件。默认数据表名 data，仅允许单条 SELECT 或 WITH SELECT，最多返回 1000 行。先读列名和实际类型，再编写查询。

引擎先载入指定文件，然后关闭外部访问；用户 SQL 不能读取其他文件或网络。只读查询不修改输入，进程限制 30 秒、内存上限 1 GB。数据来源太大或类型不符时说明限制，不伪造统计结果。

数据功能需要独立 DuckDB 环境；尚未安装时说明 npm run setup:data 的作用，不在只读 MCP 调用中偷偷安装。
