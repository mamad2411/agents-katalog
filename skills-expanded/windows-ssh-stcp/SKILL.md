---
name: windows-ssh-stcp
description: 把一台没有公网入站端口的 Windows 机器（天翼云电脑、云桌面、NAT 后的办公机）经 FRP STCP 接到已有 frps，使控制机可以用 ssh 登录。用于用户提到天翼云电脑、Windows 云桌面 SSH、STCP、frpc visitor、OpenSSH for Windows、127.0.0.1:2222，或要把内网 Windows 接到现有 frps 中继时。先复用已有 frps，不要新建一台、不要新开 7000。
---

# Windows SSH over FRP STCP

零入站远程 SSH：Windows 上的 frpc 主动连出到 frps，把本机只监听环回的 sshd 登记成 STCP。控制机上的 visitor 把它映射到 `127.0.0.1:2222`。公网只暴露 frps 已有端口，不开放 22，也不为这台机器新增防火墙规则。

```text
Windows sshd 127.0.0.1:22
        ^
Windows frpc (stcp proxy) ----出站----> frps 已有端口
                                            ^
控制机 frpc (visitor) ------出站----------┘
        |
控制机 127.0.0.1:2222
        |
ssh -p 2222 <user>@127.0.0.1
```

本 skill 不含真实地址、token、secretKey、用户名或公钥。连接三要素一律用占位符，由操作者交互提供或放在私有目录。深度细节按需读：

- `references/windows-provider.md`：Windows 侧 OpenSSH、frpc.toml、计划任务、公钥 ACL、清理清单
- `references/visitor.md`：macOS / Linux visitor 与 SSH config
- `references/pitfalls.md`：这次部署和复用中继时实机踩过的坑

## 先决定，不要直接装

1. **已有 frps 就复用。** 读它的 `bindPort`、`auth.token`、`transport.tls.force`。STCP 不占公网端口，`allowPorts` 不用改，防火墙不用加规则。
2. **版本跟 frps 走。** 两端都用 frps 的版本（当前生产验证过的是 0.71.0）。不要因为旧教程写 0.61 就降级。
3. **每台机器单独的 STCP secretKey。** `openssl rand -hex 16`。不要复用另一台设备的密钥。proxy 名全局唯一，例如 `win-ssh-<短名>`。
4. **visitor 端口避开本机占用。** 默认 `2222`，先确认没人监听。55555 一类端口在有些机器上会被隐形进程占用。

## 连接三要素

| 占位符 | 谁持有 | 作用 |
|---|---|---|
| `<FRPS_ADDR>` | 三端 | 域名或 IP。纯 TCP，Cloudflare 必须灰云 |
| `<FRPS_PORT>` | 三端 | 已有 frps 端口，不是 22 |
| `<FRPS_TOKEN>` | 三端 | 登录 frps。泄露等于别人能接入这台中继 |
| `<PROXY_NAME>` | Windows + visitor | 两端字符串必须一致 |
| `<STCP_SECRET>` | 仅这两端 | 点对点配对，frps 不保存它 |
| `<SSH_USER>` | SSH | Windows 上启用且能进 Administrators 或普通用户的账户 |

## 执行顺序

1. 在 Windows 上装 OpenSSH，**只听 `127.0.0.1:22`**，不加公网防火墙规则。系统能力包失败时用官方 Win32-OpenSSH 便携版，功能等价。完整命令见 `references/windows-provider.md`。
2. 装与 frps 同版本的 `frpc.exe`，写入无 BOM 的 `C:\frp\frpc.toml`。服务端有 `transport.tls.force = true` 时才加 `transport.tls.enable = true`，否则不要加。日志用 `log.maxDays`，不要把 stdout 追加到文件。
3. Windows 侧优先用 NSSM 服务常驻：`AppExit Default Restart`、`AppRestartDelay 5000`。没有 NSSM 时再用「开机 + 每 5 分钟」计划任务；那种任务不能恢复被强制结束后仍显示 Running 的实例。
4. 控制机写 visitor，映射到 `127.0.0.1:2222`。macOS 用 LaunchAgent，程序、配置和工作目录都写绝对路径。见 `references/visitor.md`。
5. 先读横幅确认链路，再装公钥。横幅应是 `SSH-2.0-OpenSSH_for_Windows_...`。
6. 公钥写到 sshd 实际读取的文件。Administrators 组成员通常是 `C:\ProgramData\ssh\administrators_authorized_keys`，写完必须断继承并只留 SYSTEM 与 Administrators 完全控制。
7. 端到端：`ssh <host-alias> whoami` 返回 `计算机名\用户`。然后删掉 `C:\frp` 里的安装脚本、zip 和解压目录。

## 验收

- frps dashboard 的 `/api/proxy/stcp` 里该 proxy 为 `online`。v0.71 没有 `/api/proxy`，请求它会 404，不能用来判断健康。
- `ssh -p 2222` 能登录，且 Windows `netstat` 里 22 只出现 `127.0.0.1`。
- 计划任务在 frpc 进程被结束后 5 分钟内重新出现 `frpc.exe`。
- `C:\frp` 只剩 `frpc.exe`、`frpc.toml`、启动脚本和 frpc 自己写的日志。

## 分享纪律

分享前搜索本目录，确认没有 32 位十六进制密钥、私网 IPv4、真实域名、Windows 用户名和公钥正文。真实值只留在操作者自己的 `~/project/<部署目录>/` 和 SSH config。
