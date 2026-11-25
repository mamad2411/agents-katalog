---
name: sqlite3-expert
description: "编写、审查和优化 SQLite SQL、表结构、索引与数据迁移，处理 SQLite 类型亲和性、约束、JSON、事务锁及 sqlite3 接口。用于 SQLite 建库、查询纠错、慢查询分析、数据库结构审查和应用集成；其他数据库的 SQL 仅在需要迁移到 SQLite 时使用。"
metadata:
  version: "0.1.0"
---

# SQLite3 Expert

交付符合实际 SQLite 运行时、业务语义正确且可验证的 SQL。重点是减少模型容易犯的方言、空值、连接基数、索引和迁移错误，而不是机械套用数据库规范。

## 工作方式

1. **识别任务与执行范围**：区分解释、生成 SQL、只读审查、修改代码、执行数据库变更。用户要 SQL 或审查时，不据此改动现有数据库；已有执行授权无需重复询问。
2. **获取最小必要上下文**：优先从已有 DDL、调用代码、迁移脚本和连接读取版本、结构、参数及查询需求。不要要求用户重复提供已能读取的信息。简单语法题可直接回答；只有无法推断且影响正确性的业务含义才需澄清。
3. **选择对应参考**：只读取本次任务相关文件，不要每次加载全部资料。
4. **先保证语义，再设计物理实现**：明确结果一行代表什么、是否保留无匹配项、重复和 NULL 的含义、排序与分页规则。建表先确定键和约束，索引根据真实查询设计。
5. **按风险验证**：查询验证结果与边界；索引验证结果等价及计划；迁移在副本验证保留的数据、约束、依赖对象和失败回滚。仅凭 SQL 能解析，不能声称业务正确或性能提高。
6. **交付可执行结果**：说明必要的版本要求、参数绑定方式、关键设计理由和已做的验证。未执行就明确写“未执行”；不要把本机测试描述成目标应用验证。

## 按需阅读

- 版本、PRAGMA、类型、NULL、SQLite 方言差异：[运行时与类型](references/runtime-and-types.md)。
- 主外键、范式、约束、STRICT、JSON 建模：[表结构设计](references/schema-design.md)。
- 增删改查、连接、聚合、窗口函数、分页、UPSERT、JSON：[查询与特殊语法](references/query-patterns.md)。
- 联合索引、覆盖索引、部分/表达式索引、查询计划：[索引设计](references/index-design.md)。
- 锁、WAL、重试、备份、表重建与回滚：[事务与迁移](references/transactions-and-migrations.md)。
- 命令行、导入导出、Python/C 接口、连接生命周期：[应用集成与常用操作](references/integration-and-operations.md)。
- 技能自测与真实任务验收：[验证场景](references/evaluation.md)。

## 必须保留的 SQLite 判断

- 从执行 SQL 的连接读取 sqlite_version()；命令行、Python、Qt/Android 或其他驱动的 SQLite 可能不是同一版本。未知版本时使用兼容写法，或注明最低版本，不替用户升级运行环境。
- 新建类型优先明确使用 INTEGER、REAL、TEXT、BLOB；不要把 SQLite 的 VARCHAR(n)、DECIMAL(p,s)、DATE 当作其他数据库的强制类型规则。
- 值使用绑定参数，标识符使用白名单及正确引用。不要拼接用户值，不将 CLI 点命令交给 SQL API。
- 使用 IS NULL 判断空值；审查 NOT IN 中的 NULL、LEFT JOIN 的过滤位置、COUNT(*) 对空匹配的计数、整数除法和非分组列。
- 不默认用 REPLACE 实现更新，不默认给所有表加 AUTOINCREMENT，不把 PRIMARY KEY、UNIQUE 已覆盖的索引再建一遍。
- 联合索引看定义顺序、条件类型、排序与返回列；WHERE 条件书写顺序不决定是否使用索引。不要断言“索引一定更快”“范围后的列完全没用”或“低基数字段永远不能建索引”。
- 每个需要外键的应用连接在事务开始前启用并核实 foreign_keys。不要认为 DDL 中写了 REFERENCES 就已经在所有连接生效。
- 创建初始化脚本、编写迁移和清空重建是不同任务。CREATE TABLE IF NOT EXISTS 不会校验/升级旧结构，DROP TABLE 会删除数据及其索引、触发器。
- 不为了消除错误删除现有约束、关闭持久性、忽略坏行或丢弃业务数据。需要改变业务规则时应明确提出，不悄悄“修好”。

## 获取已有数据库结构

可使用 [inspect_sqlite.py](scripts/inspect_sqlite.py)，仅依赖 Python 标准库。路径必须已存在，脚本用 mode=ro 打开，不创建数据库、不执行传入 SQL、不输出业务行。

```text
python <skill-dir>/scripts/inspect_sqlite.py <database-path> --table orders
python <skill-dir>/scripts/inspect_sqlite.py <database-path> --checks
```

输出 JSON 包含本工具连接的引擎版本、编译选项、PRAGMA、DDL、列、索引及外键。默认不扫描全表；--checks 显式执行全库 quick_check 和 foreign_key_check，可能耗时并输出违反约束的记录标识。输出可能含 DDL 默认值等业务信息，仅在任务范围内使用。

本工具的连接设置不代表应用连接设置；自定义排序规则、扩展、加密数据库需要原应用环境支持。工具打不开时报告原因，不改库、不默认绕过锁或启用 immutable。

## 建表与评审的输出重点

- **生成 SQL**：给出必要 SQL、输入参数、最低版本和少量影响行为的假设，避免附带无关 DDL。
- **结构评审**：分清确定的问题、依赖工作负载的建议、风格改进；给出具体字段/索引和影响，不以“违反很多原则”代替证据。
- **性能优化**：至少列出目标查询、现有索引、候选索引、预期改善及查询计划/耗时证据；没有规模和参数时只能给候选方案。
- **迁移**：交付有顺序的迁移过程、数据映射、验证与回滚方式，明确是否执行。
- **学习解释**：按用户熟悉程度控制展开；用户偏好分点时用分点，短字段名和条件不必使用行内代码样式，完整 SQL 使用代码块。

## 可复用示例与维护

[order_schema.sql](assets/order_schema.sql) 是独立生成的客户、商品、订单与明细示例，要求 SQLite 3.37+ 和 JSON 函数。它演示整数主键、唯一业务键、历史成交价、外键和查询驱动索引；不是现有数据库的自动迁移脚本，使用前按业务调整。

```text
python -m unittest discover -s <skill-dir>/tests -v
```

测试只使用内存或临时数据库，覆盖检查工具与关键 SQL 行为。修改示例或规则后运行相关测试；仍需在真实任务的目标运行时验证。官方文档链接放在对应参考中，使用新语法或遇到版本差异时查阅，不能把技能版本 0.1.0 当作 SQLite 版本。
