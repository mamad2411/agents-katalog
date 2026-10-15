---
name: db-cli
description: |
  多数据库 CLI 工具 - 支持 MySQL 和达梦(Dameng)数据库的 SQL 导入、导出和执行操作。

  **务必主动触发此 Skill 的场景：**
  - 用户提到数据库操作、SQL 查询、数据导入导出
  - 用户需要备份数据库、迁移数据、执行批量 SQL
  - 用户询问 MySQL 或达梦数据库相关操作
  - 用户说"查一下数据库"、"执行 SQL"、"导出数据"、"导入数据"
  - 用户使用 /db-cli 命令
  - 任何需要连接数据库进行操作的情况

  **支持的数据库：** MySQL, 达梦数据库
  **支持的操作：** import (导入), export (导出), exec (执行 SQL)
---

# db-cli Skill

多数据库命令行工具，统一接口操作 MySQL 和达梦数据库。

## 执行流程

1. **检查安装**：运行 `which db-cli` 或 `where db-cli` 检查是否已安装
2. **如需安装**：运行 `npm i -g @xiaokexiang/db-cli`
3. **参考 usage.md**：读取 `references/usage.md` 获取详细用法和命令示例
4. **构建并执行**：根据用户需求构建并执行 db-cli 命令

## 注意事项

- **连接字符串格式**：
  - MySQL: `mysql://user:password@host:port`
  - 达梦: `dm://user:password@host:port`
- 连接字符串**不包含数据库名**，请在 SQL 中使用 `USE database;` 或 `-s` 参数指定
- **必需参数**：所有命令都需要 `-c, --connection` 指定连接字符串

## 错误处理

| 错误场景 | 解决方案 |
|---------|---------|
| db-cli 命令未找到 | 执行 `npm i -g @xiaokexiang/db-cli` 安装 |
| 连接失败 | 检查连接字符串格式、网络连接和数据库服务状态 |
| SQL 执行错误 | 默认会停止执行，使用 `--continue-on-error` 可跳过错误继续执行 |
| 导入文件不存在 | 检查文件路径是否正确 |

## 参考文档

详细命令用法、参数说明和示例请参考 `references/usage.md`。
