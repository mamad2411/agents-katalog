---
name: compose-cd-deploy-pitfalls
description: >
  Docker Compose 生产 CD 部署的三类隐蔽陷阱与修复范式——迁移阻塞健康检查致误回滚、
  纯 build 服务镜像 tag 漂移不重建容器（healthy≠deployed）、大表
  FULLTEXT 迁移整表拷贝。当用户在 CI/CD（GitHub Actions 等）中用
  docker compose 部署到服务器、部署"成功"但代码没更新、部署触发回滚、或容器
  entrypoint 带数据库迁移时，必须参考本 skill。
---

# Docker Compose CD 部署陷阱（生产实战三连事故沉淀）

来源：2026-09-07 某舆情平台三期部署，同一轮暴露三层问题，每一层都"看起来成功"。

## 铁律：healthy ≠ deployed

带自动回滚的流水线里，"服务 healthy"只证明**某个版本**活着。部署失败→回滚→服务照样 healthy。
部署验证必须核对**版本指纹**，至少取二：

```bash
ssh user@server 'docker inspect <容器> --format "image={{.Image}} started={{.State.StartedAt}}"'
# started 必须是本次部署时间窗内；image ID 必须是本次构建产物
ssh user@server 'docker exec <容器> ls /app/<新文件>'          # 代码特征抽查
ssh user@server 'docker exec <db> mysql -e "SELECT * FROM alembic_version"'  # 迁移戳
```

workflow 全绿不算数——本事故中"成功"的 CD 跑了三遍，容器始终是旧镜像。

## 陷阱 1：entrypoint 迁移阻塞启动 → 健康检查误判 → 误回滚

**机理**：容器 entrypoint 先跑 `alembic upgrade head` 再启动应用。大表迁移（见陷阱 3）耗时分钟级，
期间应用不监听端口，镜像 healthcheck（如 start_period 40s + 3×30s）在迁移完成前判 unhealthy，
`docker compose up -d` 报 `dependency failed to start: container <backend> is unhealthy`，
流水线触发回滚。

**修复范式：迁移先行一次性容器**。在 build 与 up 之间显式跑迁移，up 时 entrypoint 迁移变 no-op：

```yaml
# Deploy 步骤（在服务器上执行）
docker compose -f docker-compose.yml build --parallel --build-arg BUILDKIT_INLINE_CACHE=1

# 迁移先行：--no-deps 不拉依赖、-T 禁 TTY（CI 必须）、--entrypoint 绕过 shell 入口避免迁移跑两遍
docker compose -f docker-compose.yml run --rm --no-deps -T \
  --entrypoint python backend -m alembic upgrade head

docker compose -f docker-compose.yml up -d --build --force-recreate <应用服务清单>   # 见陷阱 2
```

回滚兼容性：旧代码不引用新列时，多余列无害（SQLAlchemy 显式列查询），回滚安全。

## 陷阱 2：heredoc 管道脚本被 `docker compose run` 吃掉 stdin（假成功部署）

**机理**：部署脚本经 `ssh host 'bash -s' <<EOF` 以 **stdin** 传入；脚本中间的
`docker compose run ...` **默认 `-i` 保持 stdin 打开**，把脚本剩余所有行吃成容器 stdin。
后果：迁移执行了（exit 0），但 `up -d`、`.deployed_sha` 写入等后续行**从未执行**，
步骤却显示 success——健康的旧容器让健康检查照过，形成「假成功部署」。

**识别信号**：`.deployed_sha`（或等价指纹文件）没更新 + 容器 StartedAt 未刷新 + 日志里
迁移行之后没有任何 up 输出。

**修复**：stdin 定向死——

```yaml
docker compose -f docker-compose.yml run --rm --no-deps -T \
  --entrypoint python backend -m alembic upgrade head < /dev/null   # ← 关键

docker compose -f docker-compose.yml up -d --build
```

注意：`-T` 只禁 pseudo-TTY，**不关 stdin**，必须显式 `< /dev/null`。

**教训**：先在容器/脚本执行语境里排查（stdin、TTY、信号），再怀疑 compose 行为。
本事故中一度误判为「纯 build 服务 tag 漂移不重建」并加了 force-recreate（幻影修复），
后来用「回滚的纯 up -d 却正常重建了容器」这条反证才定位到真根因——**保留反证意识**。

## 陷阱 3：带 FULLTEXT 索引的大表，ADD COLUMN 不可走 INSTANT

**机理**：MySQL 8.0 下表带 FULLTEXT 索引时 `ADD COLUMN` 退化为整表 COPY
（实测 22K 行/112MB ≈ 6 分钟/列，桌面机）。迁移逐列 `op.add_column` 写 N 列 = N 次整表拷贝。

**修复范式**：多列合并为**一条** ALTER，一次拷贝：

```python
# alembic 迁移：列定义白名单 + 逐列幂等守卫，缺失列拼一条 ALTER
def upgrade() -> None:
    conn = op.get_bind()
    missing = [name for name, ddl in _COLUMN_DEFS.items() if not _column_has(conn, "t", name)]
    if missing:
        op.execute(sa.text(
            "ALTER TABLE t " + ", ".join(f"ADD COLUMN {_COLUMN_DEFS[m]}" for m in missing)
        ))
```

## 部署失败的杂项经验

- 服务器 git fetch 走 ssh://github.com 偶发 `Connection timed out`——先重跑，别慌着改流水线
- 回滚会重建容器，失败容器的日志随之消失；要诊断失败版本用一次性诊断容器复现（不发布端口）
- 流水线日志可能被构建刷屏截断，看不到 `up -d` 输出不等于没执行——以服务器指纹为准

## 关联

- 验证与回滚后诊断的完整流程见 skill `cd-deploy-verification`（healthy≠deployed 的指纹核对法、
  一次性诊断容器操作法、凭据轮换顺序）
