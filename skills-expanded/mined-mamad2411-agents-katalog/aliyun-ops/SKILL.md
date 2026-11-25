---
name: aliyun-ops
description: "统一查询阿里云 DMS、SLS、MSE/Nacos 与 ACK 运维数据。当需要查询线上数据库、执行只读 SQL、预览或提交 DMS 数据变更工单、拉取 SLS 日志或指标、核对 Nacos 配置、查看 ACK 集群和节点、通过 Workbench 查询私网 Kubernetes 资源、ConfigMap 与 Secret 键名，或在用户确认后受控切换 Deployment 镜像与环境变量、等待发布结果时使用。"
---

# 阿里云运维查询

统一使用本 Skill 的脚本查询 DMS、SLS、MSE 和 ACK。先判断目标产品，再只读取对应参考资料，避免把无关协议与排障经验全部加载进上下文。

## 能力路由

| 场景 | 脚本 | 必读参考 |
| --- | --- | --- |
| 线上数据库查询、DMS 实例/库、数据变更工单 | `scripts/dms.py` | `references/dms.md` |
| SLS 日志、metricstore 指标、LOG V1 签名 | `scripts/sls_get_logs.py` | `references/sls.md` |
| MSE 集群、Nacos 配置与配置历史 | `scripts/mse.py` | `references/mse.md` |
| ACK 集群、节点、KubeConfig、Kubernetes 资源只读查询；Deployment 切镜像、改环境变量、等待发布 | `scripts/ack.py` | `references/ack.md` |

DMS 与 MSE 复用 `scripts/aliyun_rpc_v1.py`。SLS 使用独立的 LOG V1 签名，ACK 使用 `scripts/ack_roa_v3.py` 的 ACS3-HMAC-SHA256 签名，禁止混用三种协议。新增其它产品时，业务参数、响应解析和安全边界继续放在产品脚本与 reference 中。

## 公共流程

1. 从用户问题确认产品、地域、实例、时间窗口或配置标识。信息不足时先列资源，不猜生产目标。
2. 读取对应 reference，确认命令、最小 RAM 权限与产品专属风险。
3. 优先使用进程环境变量；需要文件时使用 `~/.config/aliyun-ops/env`。旧 DMS/SLS 文件会长期只读回退，无需迁移。
4. 先执行只读或预览命令，核对实例、地域、环境和结果范围，再给出结论。
5. 输出中不得出现 AK/SK、签名 URL或无关配置正文；服务端错误只保留错误码与截断消息。

## 配置纪律

- AK/SK 只允许来自进程环境变量或用户主动创建、权限为 `600` 的私有 ENV 文件。
- 不自动创建、复制、合并、改写、改权限或删除任何真实 ENV 文件。
- 显式 `--env-file`、产品级 `ALIYUN_*_ENV_FILE` 或 `ALIYUN_OPS_ENV_FILE` 指向的文件不存在时立即失败，不回退其它凭证。
- 默认读取顺序为进程环境 → `~/.config/aliyun-ops/env` → 产品旧路径；后读文件只补空值，不覆盖已有变量。
- DMS 写操作只能走工单，且真实提交必须显式带 `--yes`。MSE 本期只提供读命令。
- MSE 当前配置与历史配置无 `--grep` 时只输出摘要；不得为了方便绕过这一边界输出完整配置。
- ACK 查询命令只读。私网 APIServer 使用短期内网 KubeConfig 加 Workbench 跳板；不提供任意远程 shell 或 `apply/delete/patch/scale`。
- ACK 写入只能通过 `set-image` / `set-env`：默认只预览，用户确认后显式带 `--yes` 才执行；`ALIYUN_ACK_WRITE_NAMESPACES`、`ALIYUN_ACK_IMAGE_PREFIXES` 配置时强制白名单。禁止绕过这两个命令，直接用 `workbench exec`、手工 KubeConfig 或临时脚本执行任何写操作；需求超出这两个命令时，先向用户说明，不要自行变通。
- ACK 查询先列资源摘要，再按用户明确目标读取单个对象。Secret 只输出键名和脱敏值，KubeConfig 默认不回显正文。

配置模板位于 `assets/env.example`。初始化新文件时由用户主动执行：

```bash
mkdir -p ~/.config/aliyun-ops
install -m 600 assets/env.example ~/.config/aliyun-ops/env
```
