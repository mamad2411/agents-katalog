---
name: dm8-tools
description: "达梦数据库(DM8)工具集，用于连接数据库实例、列出所有表、查看表结构、执行 SQL 查询等操作。当需要操作达梦数据库、查询数据、分析表结构时使用此技能。支持通过命令行参数指定 host、port、user、password、database、schema 等连接信息，可代替 dm8 mcp 服务使用。支持 Windows、macOS 和 Linux 平台。"
---

# 达梦数据库 DM8 工具 Skill

用于操作达梦数据库的工具集，提供连接测试、表管理和 SQL 执行功能。

## 快速开始

### 前置要求

安装 Python 依赖：

```bash
pip install jaydebeapi JPype1
```

> 本工具使用 JDBC 驱动连接达梦数据库，已内置 DmJdbcDriver18.jar 驱动文件。

### 连接参数

所有脚本支持以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | 数据库主机地址 | localhost |
| `--port` | 数据库端口 | 5236 |
| `--user` | 数据库用户名 | SYSDBA |
| `--password` | 数据库密码 | 必填 |
| `--database` | 数据库名称 | 可选 |
| `--schema` | Schema 名称 | 用户默认 Schema |

## 可用脚本

### 1. 测试数据库连接

```bash
python scripts/dm8_connect.py --host 127.0.0.1 --port 5236 --user SYSDBA --password YOUR_PASSWORD
```

### 2. 列出所有表

```bash
python scripts/dm8_tables.py --host 127.0.0.1 --user SYSDBA --password YOUR_PASSWORD --schema SCHEMA_NAME
```

### 3. 查看表结构

```bash
python scripts/dm8_schema.py --host 127.0.0.1 --user SYSDBA --password YOUR_PASSWORD --table TABLE_NAME --schema SCHEMA_NAME
```

### 4. 执行 SQL 查询

```bash
python scripts/dm8_query.py --host 127.0.0.1 --user SYSDBA --password YOUR_PASSWORD --query "SELECT * FROM TABLE_NAME WHERE ROWNUM <= 10"
```

### 5. 查看数据库信息

```bash
python scripts/dm8_info.py --host 127.0.0.1 --user SYSDBA --password YOUR_PASSWORD
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

## 平台兼容性

- ✅ Windows
- ✅ macOS
- ✅ Linux

驱动文件查找顺序：
1. `assets/DmJdbcDriver18.jar`（推荐位置）
2. 环境变量 `DM_HOME/drivers/jdbc/`
3. 系统默认安装位置

## 达梦数据库特有注意事项

- 使用 Schema 概念（类似 Oracle）
- 系统视图使用 `DBA_*`、`ALL_*`、`USER_*` 命名
- 支持 PL/SQL 语法
- 默认端口为 5236
- 默认管理员用户为 SYSDBA

### 参考更多 SQL 示例

查看 `references/common_queries.md` 获取常用达梦 SQL 查询模板。
