---
name: schema-migration-convergence
description: >
  检测并修复 "运行时 schema 补丁" 反模式——每次启动用 information_schema 探测 + ALTER TABLE，
  将多轨 schema 管理（create_all + 运行时补丁 + 迁移工具）收敛为迁移工具单一管理。
  触发词：运行时补丁、schema兼容、三套并存、迁移收敛、_ensure_schema_compatibility、
  information_schema ALTER TABLE、启动时修表、Prisma Migrate、Django migrations。
---

# 数据库迁移收敛

## 核心原则

数据库 schema 管理应**只有一种机制**。常见的反模式是项目演进中积累多套并存：

1. **ORM 建表**（如 `Base.metadata.create_all`、Prisma `db push`、Django `migrate`）— 早期用来建新表
2. **运行时补丁** — 启动时 `information_schema` 探测 + `ALTER TABLE` 补齐列
3. **迁移工具**（如 Alembic、Prisma Migrate、Django migrations、TypeORM Migrations）— 后期引入的版本化迁移

三轨并存的后果：改一张表有三套代码可能动，变更来源不可追溯。

修复目标：将运行时补丁转为迁移工具版本，删除补丁函数，迁移工具成为唯一入口。

## 支持的技术栈

| 技术栈 | 迁移工具 | 补丁检测关键词 |
|--------|----------|----------------|
| Python + SQLAlchemy | Alembic | `information_schema`, `ALTER TABLE`, `Base.metadata.create_all` |
| Python + Django | Django migrations | `RunPython`, `migrate`, `state.ops` |
| Node.js + Prisma | Prisma Migrate | `prisma.$executeRaw`, `db push`, `ALTER TABLE` |
| Node.js + TypeORM | TypeORM Migrations | `queryRunner`, `changeColumn`, `addColumn` |
| Node.js + Sequelize | Sequelize CLI | ` queryInterface`, `addColumn`, `changeColumn` |
| Go + GORM | GORM Migrator | `Migrator().AddColumn`, `AutoMigrate` |
| Java + Hibernate | Flyway/Liquibase | `ALTER TABLE`, `@Column` |

## 工作流程

### 阶段 1：侦查

用 wakita-scout 定位运行时补丁。搜索模式见 `references/check-patterns.md`。

产出：补丁函数位置、每条 ALTER TABLE 的（表名, 列名, 操作类型）、调用入口。

### 阶段 2：构建迁移

将补丁逻辑转为迁移版本。代码模板见 `references/migration-templates/` 目录。

关键要求：
- 迁移必须**幂等**——能安全重复执行
- 用 `information_schema` 列存在性探测，兼容所有数据库版本
- `downgrade` 可为 `pass`（列由 ORM 模型管理）

### 阶段 3：删除补丁

1. 删除补丁函数体
2. 删除调用点（如 `init_db()` / startup event）
3. 清理不再使用的 import
4. 验证：`mypy` 0 errors / `tsc` 0 errors

### 阶段 4：验证

```bash
# Python + Alembic
alembic upgrade head --sql   # 离线验证 SQL
alembic upgrade head          # 在线执行
alembic current               # 确认到达 head
mypy app/ && pytest tests/    # 代码质量

# Node.js + Prisma
npx prisma migrate deploy     # 执行迁移
npx prisma migrate status     # 确认状态
npm run build && npm test     # 代码质量

# Django
python manage.py migrate      # 执行迁移
python manage.py showmigrations  # 确认状态
python manage.py test         # 代码质量

# TypeORM
npm run typeorm migration:run # 执行迁移
npm run typeorm migration:show  # 确认状态
npm run build && npm test     # 代码质量
```

## 注意事项

- **时序**：补丁在 `init_db()` 内执行，先于 ORM 建表。迁移到迁移工具后需在启动前手动执行迁移命令。
- **Worker 路径**：Worker 可能只调 `init_db()` 不调 ORM 建表，迁移后 Worker 启动前也需确保迁移已执行。
- **滚动升级**：如果无法保证所有实例在迁移前停止，保留补丁作为安全网直到全部升级完毕。
- **幂等性**：迁移脚本必须能安全重复执行（用列存在性探测包裹 ALTER）。

## 参考文档

- `references/check-patterns.md` — 搜索模式（grep 命令）和常见补丁形态
- `references/migration-templates/` — 各技术栈的迁移代码模板（幂等探测）
- `references/case-study.md` — 完整案例：从多轨并存到单一管理的收敛过程