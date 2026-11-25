---
name: middleware-ops
description: 部署、调优、迁移或检查 Redis、Kafka、RabbitMQ、Elasticsearch、MongoDB 等中间件，用 Docker Compose 部署 gRPC 服务（健康检查、优雅关闭），以及搭建可观测性（存活探测、错误追踪、主机监控、Telegram 告警）与数据卷的备份还原。用户说「部署 Redis／Kafka／RabbitMQ／ES／MongoDB」「中间件调优」「Redis 迁移」「新库上线」「加监控告警」「搭监控」「错误追踪」「中间件巡检」「gRPC 负载不均」「备份」「还原演练」时使用。应用代码如何使用这些中间件属于 backend-dev 场景，不使用本 skill。
---

# 中间件运维

**先问资源上限。** 规划实例规格、节点数、内存上限前，先询问用户可用的资源上限，再结合业务现状评估，给出建议方案与计算过程；最终配置由用户或负责的工程师决定。

按任务读取对应的参考文件，不需要全部读完：

| 任务 | 参考 |
|---|---|
| 起步阶段的可观测性：拓扑、组件、日志、错误追踪、Telegram 告警、Go 容器参数 | `references/observability.md`（部署文件在 `assets/observability/`） |
| 升级到 Prometheus 后的监控告警基线 | `references/monitoring.md` |
| Redis 架构选择、内存与淘汰、持久化、巡检、数据迁移 | `references/redis.md` |
| Kafka 集群参数、topic 管理、安全加固 | `references/kafka.md` |
| RabbitMQ vhost / 队列管理、内存水位 | `references/rabbitmq.md` |
| Elasticsearch 系统参数、分片与索引设置 | `references/elasticsearch.md` |
| MongoDB 新库上线清单、备份与时间点恢复、安全基线、巡检指标 | `references/mongodb.md` |
| Docker Compose 数据卷的备份分类、备份、存放与还原演练（Postgres 与其他卷） | `references/backup-restore.md` |
| gRPC 服务的负载均衡、健康检查、优雅关闭、keepalive、排障 | `references/grpc.md` |

## 通用约定

- 参数修改写进 IaC（compose 文件、Terraform、Ansible），不在机器上手改；变更前先展示差异，确认后再执行（见 `CLAUDE.md`）。
- 中间件资源（topic、队列、vhost、数据库账号）由运维统一创建，业务方通过工单或合并请求提交申请，申请中写明用量评估及计算方式。
- 新中间件实例必须先接入监控与告警再交付使用（起步阶段见 `references/observability.md`）。
- 管理端口与数据端口不暴露到公网，只对集群内部和指定业务开放。
- 用某个 Compose 项目名首次 `up` 前，先查同名项目已有的卷与容器：`docker volume ls --filter label=com.docker.compose.project=<名>`、`docker ps -a --filter label=com.docker.compose.project=<名>`。`docker compose ls`（含 `-a`）查不到已 `down` 只剩卷的项目，不能代替这两条。有结果时向用户说明：容器的 `com.docker.compose.project.working_dir` 标签指出它属于哪个目录（卷没有这个标签，只能按卷名判断），确认是同一环境再继续，否则换项目名。
- 验证 Compose 配置用 `docker compose config --quiet`；需要看结构时加 `--no-interpolate --no-env-resolution`，写死在文件内的值仍会显示；不用 `--environment`，它会打印整个 shell 环境。
- 参考文件中的数值是常见的起点，按实际压测结果与版本文档调整，并在变更说明中写明依据。
