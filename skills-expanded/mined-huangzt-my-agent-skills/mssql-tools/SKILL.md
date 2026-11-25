---
name: mssql-tools
description: "SQL Server (MSSQL) 数据库工具集，用于连接数据库实例、列出所有表、查看表结构、执行 SQL 查询等操作。当需要操作 SQL Server 数据库、查询数据、分析表结构时使用此技能。支持通过命令行参数指定 server、port、user、password、database 等连接信息，可代替 mssql mcp 服务使用。支持 Windows、macOS 和 Linux 平台。"
---

# MSSQL 工具 Skill

用于操作 SQL Server 数据库的工具集，提供连接测试、表管理和 SQL 执行功能。

## 快速开始

### 前置要求

**安装 Python 库：**

```bash
pip install pymssql
```

**平台特定依赖：**
- **Windows**: 无需额外依赖
- **macOS**: `brew install freetds`
- **Linux (Debian/Ubuntu)**: `sudo apt-get install freetds-dev`

### 平台兼容性

- ✅ Windows
- ✅ macOS
- ✅ Linux


### 连接参数

所有脚本支持以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--server` | 数据库服务器地址 | localhost |
| `--port` | 数据库端口 | 1433 |
| `--user` | 数据库用户名 | sa |
| `--password` | 数据库密码 | 必填 |
| `--database` | 数据库名称 | 必填 |

## 可用脚本

### 1. 测试数据库连接

验证数据库连接参数是否正确：

```bash
python scripts/mssql_connect.py --server 127.0.0.1 --port 1433 --user sa --password YOUR_PASSWORD --database YOUR_DB
```

### 2. 列出所有表

获取数据库中的所有表名：

```bash
python scripts/mssql_tables.py --server 127.0.0.1 --user sa --password YOUR_PASSWORD --database YOUR_DB
```

输出格式：表名列表，包含表类型（TABLE / VIEW）、Schema 和行数

### 3. 查看表结构

显示指定表的字段信息：

```bash
python scripts/mssql_schema.py --server 127.0.0.1 --user sa --password YOUR_PASSWORD --database YOUR_DB --table TABLE_NAME
```

可选指定 Schema：`--schema dbo`

输出格式：字段名、类型、是否可空、是否主键、默认值

### 4. 执行 SQL 查询

运行任意 SQL 语句：

```bash
python scripts/mssql_query.py --server 127.0.0.1 --user sa --password YOUR_PASSWORD --database YOUR_DB --query "SELECT TOP 10 * FROM users"
```

支持 SELECT、INSERT、UPDATE、DELETE 等所有 T-SQL 语句。

### 5. 查看数据库信息

获取数据库版本、大小等信息：

```bash
python scripts/mssql_info.py --server 127.0.0.1 --user sa --password YOUR_PASSWORD --database YOUR_DB
```

## 输出格式

所有脚本输出 JSON 格式数据，便于解析：

```json
{
  "success": true,
  "data": [...],
  "message": "操作成功"
}
```

错误时返回：

```json
{
  "success": false,
  "error": "错误信息",
  "message": "操作失败"
}
```

## 常见用例

### 探索新数据库

1. 测试连接：`mssql_connect.py`
2. 列出所有表：`mssql_tables.py`
3. 查看关键表结构：`mssql_schema.py --table TABLE_NAME`
4. 查询示例数据：`mssql_query.py --query "SELECT TOP 5 * FROM TABLE_NAME"`

### 数据分析

1. 获取表记录数：`mssql_query.py --query "SELECT COUNT(*) FROM TABLE_NAME"`
2. 分析数据分布：`mssql_query.py --query "SELECT column, COUNT(*) FROM TABLE_NAME GROUP BY column"`

## SQL Server 特有注意事项

- 使用 `TOP N` 替代 MySQL 的 `LIMIT N`
- 字符串连接使用 `+` 而非 `CONCAT()`
- 日期函数与 MySQL 有差异，如 `GETDATE()` 替代 `NOW()`

### 参考更多 T-SQL 示例

查看 `references/common_queries.md` 获取常用 T-SQL 查询模板。
