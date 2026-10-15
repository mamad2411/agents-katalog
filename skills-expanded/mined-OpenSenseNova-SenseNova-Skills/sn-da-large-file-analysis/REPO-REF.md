# Repo Ref
- source: https://github.com/OpenSenseNova/SenseNova-Skills (path: skills/sn-da-large-file-analysis/SKILL.md, branch: main)
- mined: 2026-10-13
- desc: 万行以上 Excel 数据集的高性能分析引擎。提供 openpyxl read_only 流式读取（iter_rows 支持 10 万行以上）、Parquet 转换加速、内存优化、分块处理和大文件写入模式。**遇到以下任一情况就主动使用本 skill**：①数据行数 ≥ 10k（由 sn-da-excel-workflow 的行数评估步骤触发）；②用户出现触发词：大文件 / 大数据量 / 性能优化
