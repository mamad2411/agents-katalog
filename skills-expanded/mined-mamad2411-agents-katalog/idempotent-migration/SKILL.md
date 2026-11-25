---
name: idempotent-migration
description: >
  多步 DDL 迁移的幂等守卫规范与验收方法。当编写或审查包含多个对象（列/索引/表）的数据库迁移（alembic/Prisma/裸
  SQL）、遇到 1060 Duplicate column、迁移中断后重跑失败、部署因迁移卡死回滚、
  或库里出现"对象存在但版本戳没推进"的半个迁移时使用。触发词：写迁移、migration、ADD
  COLUMN、CREATE INDEX、Duplicate column、迁移中断、部分应用、
  非事务 DDL、idempotent migration。
---

# 幂等迁移守卫

## 为什么：半个迁移的真实成因

MySQL（以及若干其他数据库）的 DDL 隐式提交、不可回滚。一个含多步 DDL 的迁移
被外部因素中断——部署健康检查超时杀容器、OOM、连接断开——已经执行的语句留在库里，
版本戳却没推进。下次部署重跑整个迁移，第一条撞见已存在对象就报错
（1060 Duplicate column / 1050 Table exists），启动失败，自动回滚，再部署再失败，死循环。

实战案例（2026-08-31）：迁移第一条 `ADD COLUMN` 完成后容器被杀，生产库遗留未登记的列；
后续每次部署都撞 1060 回滚。修复方式就是把迁移改为幂等。

## 规则

**迁移含 ≥2 个 DDL 对象时，每个对象分别做存在性检查再创建。** 单对象迁移不需要
（失败即整体未应用，重跑安全）。alembic 写法：

```python
def upgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)  # Inspector 无状态，每次调用现查 information_schema

    cols = {c["name"] for c in insp.get_columns("crawled_data")}
    if "platform_content_id" not in cols:
        op.add_column("crawled_data", sa.Column("platform_content_id", ...))

    idx = {i["name"] for i in insp.get_indexes("crawled_data")}
    if "ix_crawled_data_platform_content_id" not in idx:
        op.create_index(...)

    if not insp.has_table("crawler_comments"):
        op.create_table(...)  # PK/UniqueConstraint 随表一次创建，无需单独守卫

    # 表与索引分开守卫：覆盖"表已建但索引未建"的中断位置
    t_idx = {i["name"] for i in insp.get_indexes("crawler_comments")}
    for name, cols in [("ix_a", ["a"]), ("ix_b", ["b"])]:
        if name not in t_idx:
            op.create_index(name, "crawler_comments", cols, unique=False)
```

注意点：

- 守卫的是**对象粒度**（列、索引、表各自独立），对应各种可能的中断位置
- 终态 schema 必须与不中断的执行路径**完全一致**（类型/默认值/注释/索引名/约束名），
  不能为省事简化对象定义
- 这不是"运行时 schema 补丁"——守卫在迁移文件里，仍由迁移工具唯一管理，
  与 schema-migration-convergence 的约束不冲突
- 已在版本戳上的环境不受影响：alembic 按版本戳跳过该 revision，文件内容变化不触发重跑

## 验收方法（合并前必做）

1. **部分应用路径**：测试库升到目标迁移的前一版本，手动执行目标迁移的**第一条 DDL**
   （模拟中断现场），然后 `upgrade head`——必须成功且版本戳推进
2. **全新路径**：空库直接 `upgrade head`——必须成功
3. **终态比对**：两条路径的 `SHOW CREATE TABLE` 与一个"从未中断"的参照库逐字 diff
   （去掉 `AUTO_INCREMENT=` 等随数据变化的项），必须零差异
