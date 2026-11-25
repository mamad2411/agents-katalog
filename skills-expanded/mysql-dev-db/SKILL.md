---
name: mysql-dev-db
description: 用于 Claude Code、Codex 或其他本地 agent 安全连接、检查和操作本地开发 MySQL 数据库。用户提到 MySQL、本地数据库、数据库连接、数据库配置、.env 数据库配置、SQL 文件、执行 SQL、查库、查表、查字段、看表结构、表数据检查、导入 SQL、避免临时 PDO 脚本、优先使用 mysql CLI 或 PyMySQL 兜底时应使用此 skill。
---

# MySQL 本地开发数据库

## 使用边界

- 只用于本地开发数据库，不用于生产库、线上库或不可确认环境。
- 默认用简体中文说明操作结果；SQL、命令、表名、字段名、配置 key、错误信息保持原文。
- 优先使用当前工作目录或本 skill 自带的 `mysql_dev_db.py` helper 连接数据库，不要临时生成 PHP PDO 脚本。
- 如果当前工作目录存在 `scripts/mysql_dev_db.py`，优先执行就近 helper；否则再按当前 shell 调用全局 skill helper。
- 命令示例必须按当前 shell 写路径变量：PowerShell 用 `$env:USERPROFILE`，cmd 用 `%USERPROFILE%`，Bash/Git Bash/Linux/macOS 用 `$HOME`。
- 优先使用 `mysql` CLI，因为它最接近真实 MySQL 执行行为，适合执行 `.sql` 文件、初始化表结构和排查 SQL 错误。
- 只有 `mysql` CLI 不可用时，才使用 `PyMySQL` 作为兜底。

## 配置读取规则

先从当前工作目录读取数据库配置。按以下顺序查找：

1. `.env`
2. `.env.local`
3. `.env.development`
4. `.ai/config.json` 中的 `mysql_dev_db`
5. 当前 shell 环境变量

支持常见变量名：

```text
MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_CHARSET
DB_HOST, DB_PORT, DB_USER, DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_NAME, DB_CHARSET
DATABASE_URL
database.hostname, database.hostport, database.username, database.password, database.database, database.charset
```

如果 `.env` 中存在 `[DATABASE]` 段，也应识别：

```text
HOSTNAME, HOSTPORT, USERNAME, PASSWORD, DATABASE, CHARSET, PREFIX
```

## 命令选择规则

先用就近 helper；只有当前工作目录没有 `scripts/mysql_dev_db.py` 时，才使用全局 helper。

### 就近 helper

就近 helper 最适合所有 AI 或 agent，因为它不依赖具体用户目录：

```powershell
python scripts/mysql_dev_db.py ping
python scripts/mysql_dev_db.py tables
python scripts/mysql_dev_db.py schema
python scripts/mysql_dev_db.py describe users
python scripts/mysql_dev_db.py query "SELECT COUNT(*) AS c FROM users"
python scripts/mysql_dev_db.py file database/init.sql
```

### 全局 helper

Windows PowerShell：

```powershell
python "$env:USERPROFILE\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" ping
python "$env:USERPROFILE\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" tables
python "$env:USERPROFILE\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" schema
python "$env:USERPROFILE\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" describe users
python "$env:USERPROFILE\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" query "SELECT COUNT(*) AS c FROM users"
python "$env:USERPROFILE\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" file database/init.sql
```

Windows cmd：

```bat
python "%USERPROFILE%\.cc-switch\skills\mysql-dev-db\scripts\mysql_dev_db.py" ping
```

Bash / Git Bash / Linux / macOS：

```bash
python "$HOME/.cc-switch/skills/mysql-dev-db/scripts/mysql_dev_db.py" ping
```

### Claude Code 权限

Claude Code 的 Windows PowerShell 授权使用 JSON 转义后的 `$env:USERPROFILE` 形式，避免写死用户目录：

```json
"PowerShell(python \"$env:USERPROFILE\\\\.cc-switch\\\\skills\\\\mysql-dev-db\\\\scripts\\\\mysql_dev_db.py\" *)"
```

不要把这个写法当成所有 shell 都通用：`$env:USERPROFILE` 只属于 PowerShell；cmd 用 `%USERPROFILE%`；Bash/Git Bash/Linux/macOS 用 `$HOME`。

## 工作流程

1. 先确认当前目录是否为数据库配置所在目录。不要在用户主目录或无关目录里猜数据库配置。
2. 读取 `.env` / `.ai/config.json`，只输出必要配置摘要，不要输出明文密码。
3. 先执行 `ping`，确认数据库可连接。
4. 只需要了解数据库结构时，优先执行 `tables`、`schema`、`describe <table>`。
5. 执行查询时，优先使用只读 SQL，例如 `SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN`。
6. 执行 `.sql` 文件、建表、初始化数据或变更结构前，说明目标文件、目标数据库和可能影响。
7. 执行后必须验证：至少运行 `tables`、`describe` 或关键 `SELECT COUNT(*)`。

## 输出约定

执行数据库任务后，用这个结构简要汇报：

```md
## 数据库操作结果

- 配置来源：`.env` / `.ai/config.json` / 环境变量
- 连接方式：`mysql CLI` / `PyMySQL`
- 目标库：`database_name`
- 执行内容：查询 / 表结构检查 / SQL 文件
- 验证结果：...
- 风险或未完成项：...
```

## 注意事项

- 不要把数据库密码写进回复、日志或命令行参数展示中。
- 不要把 `Bash(mysql *)` 作为通用放行权限；优先放行固定 helper 脚本。
- 如果 `mysql` CLI 报编码问题，先确认 `charset` 是否为 `utf8mb4`，再看终端输出编码。
- 如果 `PyMySQL` 不存在，可以建议安装：`pip install --user pymysql`。
- 如果缺少数据库配置，不要猜库名、用户名或密码，明确指出缺少哪些 key。
