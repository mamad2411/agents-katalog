---
name: sqlite-tools
description: "SQLite 数据库工具集，用于操作 SQLite 数据库文件。支持 .db、.sqlite、.sqlite3、.vscdb 等常见扩展名。无需额外安装依赖，使用 Python 内置 sqlite3 模块。支持 Windows、macOS 和 Linux 平台。"
---

# SQLite 工具 Skill

用于操作 SQLite 数据库文件的工具集，提供连接测试、表管理和 SQL 执行功能。

## 快速开始

### 前置要求

无需额外安装依赖，使用 Python 内置的 `sqlite3` 模块。

### 支持的文件类型

- `.db` - 标准 SQLite 数据库
- `.sqlite` - SQLite 数据库
- `.sqlite3` - SQLite 3 数据库
- `.vscdb` - VS Code 状态数据库
- 其他任意 SQLite 格式文件

### 平台兼容性

- ✅ Windows
- ✅ macOS
- ✅ Linux

### 连接参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--database` | 数据库文件路径 | 必填 |

## 可用脚本

### 1. 测试数据库连接

```bash
python scripts/sqlite_connect.py --database /path/to/database.db
```

### 2. 列出所有表

```bash
python scripts/sqlite_tables.py --database /path/to/database.db
```

### 3. 查看表结构

```bash
python scripts/sqlite_schema.py --database /path/to/database.db --table TABLE_NAME
```

### 4. 执行 SQL 查询

```bash
python scripts/sqlite_query.py --database /path/to/database.db --query "SELECT * FROM table LIMIT 10"
```

### 5. 查看数据库信息

```bash
python scripts/sqlite_info.py --database /path/to/database.db
```

## 输出格式

所有脚本输出 JSON 格式数据：

```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

## SQLite 特有注意事项

- 支持只读模式，避免意外修改数据库：
  ```bash
  python scripts/sqlite_connect.py --database /path/to/database.db --readonly
  python scripts/sqlite_query.py --database /path/to/database.db --readonly --query "SELECT * FROM users"
  ```
- 文件路径使用绝对路径更可靠
- 某些文件可能被其他进程锁定（如 VS Code 正在使用的数据库）

### 参考更多 SQL 示例

查看 `references/common_queries.md` 获取常用 SQLite 查询模板。
