---
name: dev-mysql
description: 面向生产后端的 MySQL 与 MariaDB 模式,涵盖 schema 设计、查询、索引、事务、复制与连接池。
metadata:
  origin: ECC
---

# MySQL Patterns

当涉及 MySQL 或 MariaDB 的 schema 设计、迁移、慢查询排查、
队列式事务、连接池或生产数据库配置时,使用本技能。
在应用特定于某个特性的模式之前,先确认准确的版本,
因为 MySQL 和 MariaDB 在若干 SQL 细节上已经产生分歧。

## 适用场景(Activation)

- 设计 MySQL 或 MariaDB 的表、索引和约束
- 在迁移运行于大型生产表之前对其进行评审
- 调试慢查询、锁等待、死锁或连接耗尽
- 添加键集分页(keyset pagination)、upsert、全文检索、JSON 列或队列
- 配置应用连接池、只读副本、TLS 或慢日志

## 版本检查(Version Check)

首先确认引擎和版本:

```sql
SELECT VERSION();
SHOW VARIABLES LIKE 'version_comment';
```

当语法存在差异时,分别对待 MySQL 和 MariaDB 的指引:

- MySQL 文档将行别名(row aliases)作为 `VALUES(col)` 在
  `ON DUPLICATE KEY UPDATE` 中的替代写法;`VALUES(col)` 在 MySQL 中已弃用。
- MariaDB 文档将 `VALUES(col)` 作为在 `ON DUPLICATE KEY UPDATE` 中引用插入
  值的支持写法;为了跨引擎兼容性,请使用它。
- `SKIP LOCKED` 仅适用于类似队列的场景。它会跳过被锁定的行,
  可能返回不一致的视图,因此不要用于一般的账务
  或对完整性敏感的读取。

## 主题索引(Topic Map)

在编写 SQL 或配置之前,先加载与任务匹配的参考文件:

| 任务 | 参考文件 |
| --- | --- |
| 表设计、列类型、复合索引、`EXPLAIN` 评审 | `references/schema-and-indexing.md` |
| Upsert、键集分页、JSON 列、全文检索 | `references/query-patterns.md` |
| 事务、加锁顺序、死锁、`SKIP LOCKED` 队列 | `references/transactions.md` |
| 应用连接池(SQLAlchemy、mysql2)、池容量配置 | `references/connection-pools.md` |
| 慢日志配置、`PROCESSLIST`、副本、`my.cnf` 起点配置 | `references/operations.md` |
| 用户、授权、TLS、最小权限评审 | `references/security.md` |

## 反模式(Anti-Patterns)

| 反模式 | 风险 | 更好的模式 |
| --- | --- | --- |
| 热点路径中使用 `SELECT *` | 过度拉取数据,客户端脆弱 | 显式选择所需列 |
| 深度 `OFFSET` 分页 | 线性扫描,页面变慢 | 键集分页(keyset pagination) |
| 外键连接列缺少索引 | 连接缓慢,删除时锁开销大 | 有意为外键列建索引 |
| 长事务 | 锁等待,undo 历史过大 | 以小工作单元提交 |
| 直接对 `mysql.user` 执行 DML | 授权表损坏风险 | 使用 `CREATE USER`、`ALTER USER`、`DROP USER` |
| 应用用户拥有管理员权限 | 爆炸半径过大 | 运行时使用最小权限用户 |
| 连接池回收周期超过 `wait_timeout` | 池中出现失效连接 | 在超时之前回收并启用预检(pre-ping) |
| 写入后从副本读取 | 用户读到过期状态 | 将写后读流程固定到主库 |

## 输出要求(Output Expectations)

当本技能用于评审时,返回:

1. 引擎/版本假设。
2. 最高风险的正确性、锁、安全和迁移问题。
3. 安全路径的确切 SQL 或代码修改。
4. 验证计划:`EXPLAIN`、迁移演练(dry run)、锁/死锁检查,以及
   回滚标准。
5. 任何影响建议的 MySQL/MariaDB 语法差异。

## 相关资源(Related)

- Skill:`postgres-patterns` - PostgreSQL 特有的 schema 和查询模式
- Skill:`database-migrations` - 迁移规划与发布安全
- Skill:`backend-patterns` - API 与服务层模式
- Skill:`security-review` - 密钥处理、认证与最小权限
- Agent:`database-reviewer` - 更广泛的数据库评审工作流
