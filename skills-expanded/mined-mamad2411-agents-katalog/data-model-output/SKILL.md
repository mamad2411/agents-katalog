---
name: data-model-output
pack: universal
description: 改动数据库表结构/数据模型时强制同步更新数据定义文档——落点见项目 AGENTS.md「目录结构」节，记录表/字段/类型/索引/约束/迁移说明。
when_to_use: 新增/修改表、字段、索引、约束、迁移脚本时。
when_NOT_to_use: 不涉及持久层结构的改动。
---

# Skill: 数据定义产出

改数据模型必须同步更新对应服务的数据模型文档（落点见项目 AGENTS.md「目录结构」节）。

## 文档路径规则

数据模型文档的落点**由各项目自定义**（见项目 `AGENTS.md`「目录结构」节）。两种常见组织：

```
# 扁平（默认模板）
docs/data-model/<service>.md            services/matching-engine/ → docs/data-model/matching-engine.md

# 按服务分目录（服务名可读、可含空格）
docs/services/<服务名>/数据模型.md   cmd/ledger/ → docs/services/Ledger/数据模型.md
```

## 每处变更需记录

1. **表用途** — 一句话说这张表存什么
2. **字段定义**

```markdown
| 字段 | 类型 | 可空 | 默认 | 说明 |
|------|------|------|------|------|
| id | ULID / char(26) | N | — | 主键，跨服务引用用 ULID |
| amount | numeric(38,18) | N | — | 金额，Decimal18 存储 |
| created_at | timestamptz | N | now() | 创建时间 |
```

3. **索引** — 列、唯一性、用途（覆盖查询/外键加速）
4. **迁移说明**
   - 是否可回滚（`make services-migrate-down` 能否安全执行）
   - 数据兼容性（已有行是否受影响）
   - 是否需要回填（backfill）
   - 预计执行时间（大表需评估锁影响）

## 金额字段约定

- DB 类型：`NUMERIC(38,18)` 普通账户，`NUMERIC(78,18)` 账本/结算
- 命名：`_amount`、`_price`、`_fee` 后缀，表明是 Decimal18 存储
- 禁止：`FLOAT`、`DOUBLE`、`REAL`

## 反模式
- ❌ 加字段不写文档与迁移说明
- ❌ 迁移脚本不可回滚却未标注
- ❌ 金额字段用 `FLOAT` 类型（精度损失）
- ❌ 大表 `ALTER TABLE ADD COLUMN NOT NULL` 不评估锁影响
