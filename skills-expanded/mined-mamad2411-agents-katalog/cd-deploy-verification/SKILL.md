---
name: cd-deploy-verification
description: >
  CD 自动部署后的正确验证方式与回滚后的失败诊断手法。当部署完成（或看起来完成）后需要确认代码真的更新、
  CI/CD 流水线显示成功但服务行为照旧、自动回滚掩盖了部署失败、或回滚后失败容器日志已消失无法排查时使用。
  触发词：部署验证、CD 部署、自动回滚、rollback、healthy 但没更新、版本指纹、
  deployed_sha、部署后没生效。
---

# CD 部署验证与回滚后诊断

## 铁律：healthy ≠ deployed

带自动回滚的部署流水线里，"服务 healthy"只证明**某个版本**活着，不证明**新版本**上线了。
部署失败 → 回滚 → 服务照样 healthy，一切看起来岁月静好，但代码纹丝不动。

验证部署必须核对**版本指纹**，三者至少取一：

```bash
git rev-parse HEAD              # 服务器仓库的 HEAD 是否等于目标合并提交
cat .deployed_sha               # 若 CD 写了部署指纹文件
docker exec <db> mysql -e 'SELECT * FROM alembic_version'   # 含迁移时核对版本戳
docker images --format '{{.Repository}} {{.CreatedAt}}'     # 镜像构建时间是否为此刻
```

同时看流水线每步的真实状态（`gh run view <id>`），不要只看总结论——
回滚步骤"成功"会让整次运行显得波澜不惊。

## 回滚后的失败诊断：日志已被覆盖

回滚会重建容器，失败容器的日志随之消失，`docker logs` 只剩回滚后的干净启动日志。
此时不要盲猜，用**一次性诊断容器**复现失败，全程不碰在跑的服务：

```bash
# 1. 把目标版本代码取到旁路工作区（不动服务器仓库当前检出）
git worktree add /tmp/diag <目标SHA>

# 2. 从运行中的同类容器复制完整环境变量
docker inspect <运行中容器> --format '{{range .Config.Env}}{{println .}}{{end}}' > /tmp/diag.env

# 3. 构建诊断镜像（注意服务器可能要走镜像源 build-arg，与 compose 一致）
docker build --build-arg REGISTRY=m.daocloud.io/docker.io -t diag-test /tmp/diag/backend

# 4. 同一 network 起一次性容器，不发布端口（避免与在跑服务冲突）
docker run --rm --name diag-test --network <项目_network> --env-file /tmp/diag.env diag-test
```

关键约束：

- **不要发布端口**（不加 `-p`），诊断容器只用于看启动日志/迁移行为
- 用 `docker compose run` 替代时务必 `--no-deps` 且不带 `--service-ports`
- 诊断容器的 entrypoint 若含数据库迁移，等于对真实库执行了该迁移——
  只有确认该迁移是预期变更时才这么做，否则先在临时库里验证
- 用完清理：`git worktree remove`、`docker rmi`、删 env 文件

## 凭据轮换操作顺序（变更前检查清单）

部署涉及凭据变更时，顺序错误 = 全站故障。按此清单执行：

| 凭据 | 正确顺序 | 错误后果 |
|------|----------|----------|
| MySQL 密码 | 先 `ALTER USER ... IDENTIFIED BY` 改库内密码 → 再改 .env/compose → 重建容器 | 顺序颠倒：配置已变库未变，全站连接失败 |
| ENCRYPTION_KEY | 先跑"旧 key 解密 → 新 key 重加密"迁移脚本，或安排各平台数据重导入 | 直接换 key：全部 AES 加密数据无法解密 |
| JWT_SECRET | 直接换，无需前置操作 | 全部在线用户掉线重登（预期行为，选低峰期） |

另注意：MySQL 容器密码属"首次初始化数据卷才生效"，改 .env 不会改变已有数据卷里的
真实密码——这就是为什么必须先 ALTER USER。
