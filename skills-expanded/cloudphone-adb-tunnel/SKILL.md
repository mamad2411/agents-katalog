---
name: cloudphone-adb-tunnel
description: Use when connecting a non-root Android cloud phone or device to a computer over the internet for ADB or scrcpy screen mirroring — deploying the Termux frpc tunnel (FRP STCP mode), setting up the VPS blind relay (frps), connecting the desktop visitor, hardening against the Android 13 phantom process killer, or diagnosing Termux failures such as missing /tmp, Go binary DNS "[::1]:53 connection refused", curl OpenSSL symbol errors, silent pkg hangs, and long-paste truncation. Triggers: 云手机 adb, termux frp, scrcpy 投屏, adb 隧道打不通, adb offline, 幽灵进程, frps 中继.
---

# 云手机 ADB 公网隧道（FRP STCP）

零信任远程 ADB：手机 Termux 内 frpc（stcp proxy → 设备 adbd `127.0.0.1:5555`）→ VPS frps 盲中继（只转发加密流量，不暴露 ADB）→ 电脑 frpc visitor → `adb connect 127.0.0.1:55556`。无需 root、无需公网 IP、无需在防火墙开 ADB 端口。

本 skill **自包含**：`scripts/` 是可直接使用的脱敏安装器与自愈脚本，`references/` 是服务端搭建与全量踩坑手册。深度细节按需读取：

- `references/frps-setup.md` — 服务端 frps 模板、systemd、防火墙、域名、健康检查
- `references/pitfalls.md` — 全量踩坑手册（每条都实机踩过），SKILL.md 只留速查表
- `tests/test_scripts_sync.py` — 一致性守卫：打包副本必须与安装器内嵌 heredoc 逐字节一致；包内不得出现凭据字面量（32 位十六进制/意外 IPv4）。改动 `scripts/` 后必须运行

> **密钥纪律**：本 skill 一律使用 `<占位符>` 与交互输入，不含任何真实凭据。真实实例的密钥只存放在操作者本机的私有部署目录（如 `~/project/cloudphone-frp/`），不提交任何仓库；改动流程后按 obsidian-doc-router 规则回写 vault 权威手册。

## 端口与角色约定

| 角色 | 端口 | 说明 |
|---|---|---|
| frps 盲中继 | `48721`（TCP，公网唯一暴露面） | token + 强制 TLS + allowPorts 限幅 |
| 设备 adbd | `127.0.0.1:5555`（仅设备本机） | 云手机需已开启 ADB 调试 |
| visitor 绑定 | `127.0.0.1:55556` | **默认不用 55555**：实机上 55555 常被隐形 root 进程占用（见 pitfalls §2.1） |
| frps dashboard | `127.0.0.1:7500`（仅环回） | SSH 隧道查看，不开公网 |

## 第一步：VPS 服务端 frps

已跑过 frps 的只需放行 `bindPort`；新部署用最小模板（完整说明、systemd 单元、防火墙与域名注意事项见 `references/frps-setup.md`）：

```toml
# /etc/frp/frps.toml
bindPort = 48721
auth.method = "token"
auth.token = "<openssl rand -hex 32 生成，绝不入库>"
transport.tls.force = true
allowPorts = [{ start = 48000, end = 48999 }]
webServer.addr = "127.0.0.1"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "<openssl rand -hex 16>"
```

验证：`systemctl is-active frps`；云防火墙放行该 TCP 端口（注意 Clash TUN 会让 `nc` 假通，须从外部主机实测）。

## 第二步：手机 Termux 部署

本仓库自带脱敏安装器 `scripts/install-termux.sh`（GitHub 官方/镜像优先、自建 CDN 兜底、固定 sha256 校验、15s 卡死换源、自动修复 curl 动态库、termux-chroot 解 Go DNS、15s 自愈 keepalive）。运行时交互输入三要素：**服务器入口**（域名/IP[:端口]）、**frps token**、**STCP secretKey**。

给法二选一：

```bash
# A. 免粘贴（推荐）：把 scripts/install-termux.sh 放到任意可下载处后
curl -fsSL <你的脚本URL> -o ~/install-termux.sh && bash ~/install-termux.sh

# B. 粘贴整段：必须用 cat 包装且外层定界符不能叫 EOF
#    （脚本内 frpc.toml 的 heredoc 也用 EOF，重名会被提前截断）
cat << 'INSTALL_EOF' > ~/install-termux.sh
<粘贴 scripts/install-termux.sh 全文>
INSTALL_EOF
bash ~/install-termux.sh
```

成功标志：`start proxy success`。脚本幂等，失败重跑即可。

## 第三步：电脑端 visitor

任一系统下载 [frp 客户端](https://github.com/fatedier/frp/releases)，配置（三要素与服务端/手机端一致）：

```toml
serverAddr = "<frps 域名或 IP>"
serverPort = 48721
auth.method = "token"
auth.token = "<与服务端一致>"

[[visitors]]
name = "cloudphone-adb-visitor"
type = "stcp"
serverName = "cloudphone-adb"
secretKey = "<与手机端一致>"
bindAddr = "127.0.0.1"
bindPort = 55556
```

```bash
./frpc -c frpc.toml        # 等 "start visitor success"
```

## 第四步：连接 + Android 13 加固（通了立即做）

```bash
adb connect 127.0.0.1:55556 && adb devices   # 期望 device（首次在手机屏上点"始终允许"）

# 防幽灵进程查杀 + 电池白名单（不做则 frpc/keepalive 活不长）
adb -s 127.0.0.1:55556 shell device_config set_sync_disabled_for_tests persistent
adb -s 127.0.0.1:55556 shell device_config put activity_manager max_phantom_processes 2147483647
adb -s 127.0.0.1:55556 shell dumpsys deviceidle whitelist +com.termux
adb -s 127.0.0.1:55556 shell cmd appops set com.termux RUN_IN_BACKGROUND allow
adb -s 127.0.0.1:55556 shell cmd appops set com.termux START_FOREGROUND allow
```

**每一条都要回读验证**（`device_config get` / `appops get` / `dumpsys deviceidle whitelist`），不要只看命令不报错。

## 投屏

```bash
scrcpy -s 127.0.0.1:55556 --video-codec=h265 --video-bit-rate=2M --max-size=1280 --max-fps=30
```

中继出口仅 3Mbps 时码率 ≤2M，卡顿降到 1.5M。

## 排障速查（全量细节见 references/pitfalls.md）

| 症状 | 方向 | 详情 |
|---|---|---|
| 所有下载源全失败 | Termux 无 `/tmp`，产物路径改 `~/frp/tmp` | pitfalls §1.1 |
| Go 程序 `[::1]:53: connection refused` | `$PREFIX/etc/resolv.conf` + `termux-chroot` 拉起（curl 能用而 frpc 不能用即此症） | pitfalls §1.2 |
| curl `cannot locate symbol "SSL_set_quic…"` | openssl/libcurl 错配，换清华源重装 | pitfalls §1.3 |
| pkg 安装黑屏无输出 | 输出被吞 + 源未配置；按需装 + 实时输出 + 自动换镜像 | pitfalls §1.4 |
| 粘贴脚本跑一半崩 | 外层 heredoc 定界符撞内层 `EOF`，改 `INSTALL_EOF` | pitfalls §1.5 |
| frpc 进程越积越多 | keepalive 探活缺 procps 时误判，需 ps 兜底 + pid 管理 | pitfalls §1.6 |
| 后台跑一阵被杀 | 幽灵进程 + 电池限制，回读验证加固 | pitfalls §1.7 |
| visitor `bind in use` 但 adb refused | 55555 被隐形 root 进程占用，用 55556 | pitfalls §2.1 |
| adb offline/假死 | `adb disconnect && connect`；再两端重启 frpc | pitfalls §2.2 |
| `nc` 通但业务不通 | Clash TUN 假握手，看应用层或外部主机实测 | pitfalls §2.3 |
| 发布脚本后对方拿到旧版 | `/pub/` 边缘缓存 24h，必须 CF purge；升级用新文件名 | pitfalls §3.3 |

## 健康判据（全链路）

```bash
adb devices                                        # 127.0.0.1:55556 device
adb -s 127.0.0.1:55556 shell getprop ro.build.version.release
adb -s 127.0.0.1:55556 shell "ps -A | grep -c [f]rpc"    # ≥1，设备内 frpc 存活
ssh <vps> 'curl -su <user>:<pw> http://127.0.0.1:7500/api/serverinfo'
# clientCounts=2（两端 frpc）、proxyTypeCount.stcp=1、curConns>=1
# 注意: /api/proxy 在 frp v0.71 恒 404，不能用作健康判断
```

## 二次分发纪律

1. 分享版发布前必跑**无密钥断言**：不含 token、secretKey、frps 域名、私网 IPv4（环回/公共 DNS 白名单除外）。
2. 脚本发布到 CDN 同名覆盖后**必须 purge**，否则边缘 24h 内是旧版。
3. 改动流程/端口/脚本后：更新私有部署目录 README + vault 权威手册（按 obsidian-doc-router），并回写本 skill 的速查表与 references。
