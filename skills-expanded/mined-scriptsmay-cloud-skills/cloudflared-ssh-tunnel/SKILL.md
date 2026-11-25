---
title: "Cloudflared SSH Tunnel"
type: skill
tags: [cloudflare, tunnel, ssh, cloudflared, egress-proxy, sandbox, self-healing]
created: 2026-10-02
updated: 2026-10-06
author: scriptsmay
status: active
---

# Cloudflared SSH Tunnel

在"敌对"沙箱网络环境中，用 Cloudflare Tunnel 建立稳定的 SSH 入口：强制 TCP 传输、绕过 DNS 污染、经出站代理、无 sudo 时照常工作，VM 重启后自动重建。

A stable SSH ingress via Cloudflare Tunnel in a hostile sandbox network: forced TCP transport, DNS-poisoning bypass, egress-proxy traversal, works without sudo, and self-heals after VM replacement.

## 为什么需要这个技能 / Why

某些容器型 VM 的网络环境对入站连接极不友好，实测约束如下：

| 约束 | 影响 | 对策 |
|---|---|---|
| 沙箱禁 UDP | cloudflared 默认 QUIC 不可用 | `TUNNEL_TRANSPORT_PROTOCOL=http2` 强制 TCP |
| 沙箱 DNS 污染 | `region1/2.v2.argotunnel.com` 解析到黑洞 | mount namespace 内 bind-mount 假 `/etc/hosts` 指向本地 shim |
| 直连 Cloudflare edge TCP 被墙 | cloudflared 无法直连 | shim 经 `$HTTPS_PROXY` 做 HTTP CONNECT |
| `--protocol` CLI 参数已移除 | 无法用命令行切换传输协议 | 环境变量 `TUNNEL_TRANSPORT_PROTOCOL=http2` 仍有效（实测） |
| 容器 NoNewPrivs | sudo/su 永远无法提权 | SSH 用户直接设为 uid 0（root 等效） |
| VM 重启清空非家目录一切 | units、sshd、用户全丢 | 全部源文件放家目录，`restore.sh` 一键重建 + 外部巡检自救 |

If your sandbox bans UDP, poisons DNS for the tunnel edge, and blocks direct TCP to Cloudflare, plain `cloudflared` will never connect. This skill stacks four workarounds (http2 transport, fake hosts in a mount namespace, a CONNECT shim through the egress proxy, a uid-0 SSH user) and makes the whole thing rebuildable with one script.

## 架构 / Architecture

```
client --ssh--> Cloudflare Edge --tunnel--> cloudflared (mount ns, 假 hosts)
  ProxyCommand: cloudflared access ssh --hostname <PUBLIC_HOSTNAME>
                                                     |
                                              127.0.0.1:7844
                                                     v
                                              edge shim (Python)
                                                     | HTTP CONNECT（无鉴权）
                                                     v
                                              egress proxy ($HTTPS_PROXY)
                                                     |
                                                     v
                                              region1/2.v2.argotunnel.com:7844
                                              （TLS 端到端，shim 只做字节转发）
```

## 前置条件 / Prerequisites

- Cloudflare 侧：Named Tunnel 已创建，Public Hostname `<PUBLIC_HOSTNAME>` → Service Type `SSH` / URL `localhost:22` 已配置，拿到 tunnel token
- 出站 HTTP 代理可用：`CONNECT region1.v2.argotunnel.com:7844` 无鉴权返回 `200` 即可（见"关键细节"）
- 目标机：Linux + systemd，有 root 权限

## 部署变量 / Variables

| 占位符 | 含义 | 去哪里找 / 怎么定 |
|---|---|---|
| `<PUBLIC_HOSTNAME>` | Zero Trust Public Hostname，SSH 入口域名 | Tunnel → Public Hostnames 里配置，如 `ssh.example.com` |
| `<SSH_USER>` | 登录用户名（uid 0，root 等效） | 自己定，如 `myuser` |
| `<EGRESS_PROXY_HOST:PORT>` | 出站代理，`host:port` 形式，**不带**用户名密码 | 目标机 `HTTPS_PROXY` 环境变量去掉 userinfo 部分 |
| `<TUNNEL_TOKEN>` | tunnel token | Dashboard 复制；只存 600 权限本地文件，**不进仓库** |

## 文件布局 / Layout

```
references/
  restore.sh                 # 一键重建（8 步，幂等，可重复执行）
  healthcheck.sh             # 自救巡检（输出 HEALTHY / RESCUED / FAILED）
  proxy.env.example          # 出站代理模板（单行 host:port）
  ssh_user.example           # SSH 用户名模板（单行）
  ws_ssh_e2e.py              # 端到端验证：经代理 websocket upgrade，读取 SSH banner
  files/
    cloudflared-edge-shim.py       # 127.0.0.1:7844 → CONNECT 代理 → 真实 edge
    cloudflared-ns.sh              # mount namespace wrapper（假 hosts + http2 + token）
    hosts.edge                     # 假 /etc/hosts：edge 域名 → 127.0.0.1
    cloudflared.service            # 静态 unit（不要用 cloudflared service install）
    cloudflared-override.conf      # drop-in：清空并替换 ExecStart 为 ns wrapper
    cloudflared-edge-shim.service  # 模板，__HTTPS_PROXY__ 由 restore.sh 替换
    cloudflared-watchdog.sh        # VM 内每分钟巡检
    cloudflared-watchdog.service / .timer
    sshd-keyonly.conf              # 仅密钥登录加固
```

`cloudflared-ns.sh` 开头 `PERSIST_HOME` 指向持久家目录，部署时改成自己的（也可用环境变量覆盖）。

## 部署步骤 / Deployment

1. Cloudflare Dashboard 建 Named Tunnel，复制 token，配好 Public Hostname → `ssh://localhost:22`
2. 把 `references/` 内容拷到目标机家目录 `~/cloudflared-setup/`（保持 `files/` 子目录结构）；把 cloudflared 的 `.deb` 安装包放到该目录（目标机已安装 cloudflared 则不需要），可选把 openssh 三个 `.deb` 放进 `debs/` 做离线兜底
3. 写入变量：
   - `~/.cloudflared/token`（权限 600）
   - `~/.cloudflared/user.pub`（允许登录的 SSH 公钥，可多行）
   - `~/cloudflared-setup/ssh_user`（单行用户名）
   - `~/cloudflared-setup/proxy.env`（单行 `http://<EGRESS_PROXY_HOST:PORT>`）
4. root 下跑 `bash ~/cloudflared-setup/restore.sh`，8 步：
   `[1/8]` 装 cloudflared → `[2/8]` openssh-server + 建 uid-0 用户 → `[3/8]` 主机密钥持久化 + sshd 加固 → `[4/8]` 装脚本/静态 unit → `[5/8]` 生成 units（替换占位符）→ `[6/8]` 启动服务 → `[7/8]` 自检 → `[8/8]` 完成
5. 按"验证"一节验收，按"自救系统"部署巡检

`restore.sh` 幂等，可重复执行；加新公钥时追加到 `user.pub` 后重跑即可。

## 验证 / Verification

```bash
# 三个服务都应 active
systemctl is-active cloudflared cloudflared-edge-shim ssh

# tunnel 注册：期望两条，protocol=http2
journalctl -u cloudflared --since '2 min ago' | grep 'Registered tunnel connection'

# 期望 ha_connections=2
curl -s http://127.0.0.1:20241/metrics | grep '^cloudflared_tunnel_ha_connections'

# 端到端：期望 HTTP/1.1 101 + SSH-2.0- banner
HTTPS_PROXY="http://<EGRESS_PROXY_HOST:PORT>" python3 ws_ssh_e2e.py <PUBLIC_HOSTNAME>
```

## 自救系统 / Self-healing（两层，缺一不可）

VM 重启会清空一切非家目录内容，所以**触发器必须在 VM 之外**：

- **内层**：VM 内 watchdog（`cloudflared-watchdog.timer` 每分钟）：检查 shim 端口可达、cloudflared 进程存在、sshd active、metrics 非零；异常重启对应服务
- **外层**：VM 之外的调度器每 5 分钟跑 `healthcheck.sh`：检查 6 项（3 个 unit、用户存在、无 `/run/nologin`、`ha_connections==2`）；健康则静默，异常则 `flock` 单例执行 `restore.sh`，90 秒后复验；输出 `HEALTHY` / `RESCUED` / `FAILED`，只有后两者需要告警
- **整机替换后的凭证回退**：整机替换会清空 `$HOME`（如 `/root`，token / user.pub / 主机密钥全丢）。持久化副本放在替换后保留的家目录；`restore.sh`、`healthcheck.sh`、`cloudflared-ns.sh`、`cloudflared-watchdog.sh` 在 `$HOME/.cloudflared/token` 不存在时自动回退到 `PERSIST_HOME`（默认 `<YOUR_PERSISTENT_HOME>`，部署时改成自己的持久家目录，也可用环境变量覆盖），保证自救仍能拿到凭证

## 客户端 / Client

```ini
# ~/.ssh/config（需安装 cloudflared）
Host <ALIAS>
    HostName <PUBLIC_HOSTNAME>
    User <SSH_USER>
    ProxyCommand cloudflared access ssh --hostname %h
```

首次连接核对主机密钥指纹；主机密钥已持久化（`~/.cloudflared/ssh_host_keys/`），重建后不变。

## 多主机模式 / Multi-host

**同一 tunnel 能否接两台主机？** 技术上可以（同一 token 跑两台 = 官方高可用模式，流量在副本间负载均衡），但有两个限制：

1. 同一 Public Hostname 的流量会被随机分到两台，**无法指定连哪一台**
2. Dashboard 的 ingress 是 tunnel 级别的，做不到"hostname A 只到主机甲、hostname B 只到主机乙"的确定性路由

**推荐模式（已验证）：一机一 tunnel** —— 每台独立 tunnel + 独立 Public Hostname，各跑一套本技能，互不干扰。第二台只需换 token 和 hostname，其余照搬（`proxy.env` 换成新机器自己的出站代理）。

Use one tunnel per host when each host needs a fixed entry point; share one token across hosts only for HA where any replica will do.

## 关键实现细节 / Key Details

- **shim 从不发送代理鉴权**：出站代理密码几分钟一轮换，存下来的立刻过期（过期密码 → 407）；实测无鉴权 CONNECT 直接返回 `200`。`proxy.env` 只存 `host:port`，`restore.sh` 自动剥离 URL 中的 `user:pass@`
- **CONNECT 目标必须用域名**：代理用自己的 DNS 解析（未被污染）；IP 字面量会被拒绝/超时
- **假 hosts 只影响 cloudflared**：`unshare --mount` + `mount --bind`，系统其他部分的解析不受影响
- **不要用 `cloudflared service install`**：无配置文件时直接退出 `1`；本方案用静态 unit 文件
- **sshd 细节**：重建后删除 `/run/nologin`（否则报 `System is booting up` 拒绝登录）；`/run/sshd` 每次重建（tmpfs 重启会丢）
- **apt 源兜底**：VM 替换后 `/etc/apt/sources.list.d/ubuntu.sources` 常缺 `URIs` 行（apt 报 Malformed entry）；`restore.sh` 先按 azure 镜像补齐，且 `debs/` 缓存的 openssh-client/server/sftp 三个包一起装，避免 apt 不可用时安装失败

## 故障排查 / Troubleshooting

| 现象 | 原因 | 处理 |
|---|---|---|
| `bad handshake` / 连接被关 | VM 重启，tunnel 全丢 | 等自救（≤5 分钟）或手动 `restore.sh` |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | 客户端残留旧 key | `ssh-keygen -R <PUBLIC_HOSTNAME>` |
| `System is booting up` | 沙箱遗留 `/run/nologin` | `restore.sh` 已自动删除 |
| `Permission denied (publickey)` | 公钥未装 / 用户名不对 | 检查 `user.pub` 与 `User` |
| `ha_connections=0` 但 unit active | token 失效 / tunnel 被删 | 检查 token，看 `journalctl -u cloudflared` |
| `Provided Tunnel token is not valid` | token 截断/复制不全 | 重新复制**完整** token（base64 应解出含 `a`/`t`/`s` 的完整 JSON） |
| shim 报 407 / tunnel 重连失败 | shim 带了过期代理密码 | 确认 `proxy.env` 为纯 `host:port`，重跑 `restore.sh` |

## 检查清单 / Checklist

- [ ] token 完整（base64 解出 `a`/`t`/`s` 三字段的合法 JSON）
- [ ] `proxy.env` 为纯 `host:port`，无鉴权信息
- [ ] `restore.sh` 8 步全过，无报错
- [ ] `Registered tunnel connection` × 2，`protocol=http2`
- [ ] `ha_connections == 2`
- [ ] E2E：`101` + `SSH-2.0-` banner
- [ ] 主机密钥已快照到 `~/.cloudflared/ssh_host_keys/`
- [ ] 内外两层自救都已部署

## 实测记录 / Field Notes

- 2026-10-02：在易失容器 VM 上按本文档从零部署，一次跑通；`TUNNEL_TRANSPORT_PROTOCOL=http2` 在新版 cloudflared（2026.9.x）依然有效，日志确认 `protocol=http2`，两条连接分别经不同 edge PoP 注册
- 同一 deployment 中发现：`ubuntu.sources` 缺 `URIs` 行会导致 apt 全灭，补可用镜像源恢复；`restore.sh` 里对可能空文件的 `grep` 管道需加 `|| true`（`set -e` 下 grep 无匹配返回 1 会 abort）；`/run/sshd` 需每次重建（tmpfs）
- token 复制教训：base64 串截断后 cloudflared 报 `Provided Tunnel token is not valid` 并无限重启；写入前先解码校验 JSON 完整性
