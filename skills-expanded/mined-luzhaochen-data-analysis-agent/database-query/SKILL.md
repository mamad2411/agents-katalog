---
name: database-query
description: 数据库查询工具集。在需要执行 SQL（execute_query.py）、查询表结构/字段/索引（get_metadata.py）、为新表生成建档草稿（doc_table.py）、或扫描团队空间发现新表（scan_tables.py）时使用。所有工具走 data_agent 只读账号，输出结构化 JSON，含错误四分类与修复建议。
---

# 数据库查询工具集（database-query）

> 四个确定性脚本的使用约定。脚本只做执行与事实返回，不含判断——语义决策在 analysis 主工作流。
> 脚本位置在仓库 `skills/database-query/scripts/`，Python 用 `.venv\Scripts\python`。

## 工具一览

| 工具 | 何时用 | 命令模板 |
|---|---|---|
| execute_query.py | 执行 / 验证 SQL | `--sql "..." [--format json\|csv\|table] [--dry-run] [--session <id>]` |
| get_metadata.py | 字段 / 表 / 索引 / 行数不清楚时 | `[--brief]` |
| doc_table.py | 为 memory/tables/ 无文档的表生成建档草稿 | `--table <表名>` |
| scan_tables.py | 检查团队空间（mock_data/team_space/）新表 | 无参数 |
| list_memories.py | 查看知识库里存了什么（表/片段/草稿/语法） | 无参数 |

## 执行 SQL（execute_query.py）

```powershell
.venv\Scripts\python skills\database-query\scripts\execute_query.py --session <会话ID> --sql "SELECT ..."
```

- 只支持单条只读语句；自动追加 LIMIT（默认 1000、硬上限 10000），结果带 `truncated` 标记
- 成功 JSON：`status/columns/rows/row_count/truncated/limit/elapsed_ms`——直接读，不要二次加工
- `--dry-run`：用 EXPLAIN 验证语法与执行计划，不抓数据（**改 SQL 前先用它验证**）
- 每次调用自动追加 `runs/<session>/retry_log.json`（attempt 自增，主工作流据此计重试次数）

### 错误分类与标准应对

| error_type | 标准应对 |
|---|---|
| FIELD_ERROR | 调 get_metadata.py 拿真实 schema，修正字段/表名后重试 |
| SYNTAX_ERROR | 对照 memory/sql_syntax.md 对应小节修正后重试 |
| PARTITION_ERROR | 检查时间过滤与日期值格式（memory/sql_syntax.md §1）后重试 |
| TIMEOUT_ERROR | 缩小时间范围 / 先聚合再取明细后重试 |
| PERMISSION / CONFIG / CONNECTION | **不重试**，向用户说明原因并转达建议 |

重试上限 `retry_max=3`（config/analysis.json），计数由 analysis 主工作流读 retry_log 完成。

## 查元数据（get_metadata.py）

```powershell
.venv\Scripts\python skills\database-query\scripts\get_metadata.py --brief   # 表总览
.venv\Scripts\python skills\database-query\scripts\get_metadata.py           # 全部表/字段/索引
```

字段名、类型、索引、近似行数一律以本工具输出为准，不凭记忆。

## 建档（doc_table.py）

```powershell
.venv\Scripts\python skills\database-query\scripts\doc_table.py --table <表名>
```

- 会话中遇到 memory/tables/ 无文档的表时调用，按模板自动生成草稿到 runs/drafts/
- 草稿需补充语义（用途/粒度/口径/坑/关联键）并审阅后，才落库 memory/tables/ 并更新 overview.md

## 团队空间扫描（scan_tables.py）

```powershell
.venv\Scripts\python hooks\scan_tables.py
```

- 检查 mock_data/team_space/ 的 *.sql 发现新表；已上线的表自动生成建档草稿
- `new_tables` 非空 → 按 next_steps 审阅落库；`pending_online` 非空 → 等待业务方建表，不处理

## 记忆浏览（list_memories.py）

```powershell
.venv\Scripts\python skills\database-query\scripts\list_memories.py
```

- 只读展示知识库现状：表知识（含使用频次）、SQL 片段摘要、待审阅草稿、语法规则
- 何时用：Step 6 提案前核对现状；用户问「库里存了什么」；会话开头报告知识库状态

## 输出约定

- 错误 JSON 含 `error_type/suggestion/sql/elapsed_ms`——把 suggestion 转达给用户
- 不要修改脚本；脚本不支持的能力（多语句、写操作）会被拒绝并返回原因
