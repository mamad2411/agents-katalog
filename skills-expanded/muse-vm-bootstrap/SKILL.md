---
title: "Muse VM 基建初始化与灾后恢复"
type: skill
tags: [infrastructure, muse-vm, systemd, disaster-recovery, ephemeral-vm]
created: 2026-09-30
updated: 2026-10-01
author: scriptsmay
status: active
---

## 目标

Muse VM（muse.ai 助手的宿主）是一台**随时会被整机替换的容器型 VM**：替换后 `/etc`、`/opt`、`/tmp` 全丢，只有 `/home` 保留。本技能沉淀"初始化即考虑恢复"的基建工程方法——**所有服务按"可一键重建"标准部署**，配合看门狗实现无人值守自愈。

## 前置认知（动手前先确认）

1. **VM 会丢东西**：2026-09-29 一天被整机替换 3 次，09-30 又发生 2 次。`/etc` 下自建 systemd unit、apt 源修改都会消失。
2. **出站走代理**：经 HTTP 代理出站（带认证），systemd 服务**不继承**代理环境变量，必须用 `EnvironmentFile` 注入。
3. **TLS 中间人**：出口代理对部分站点做 TLS MITM，Python（httpx）需 `SSL_CERT_FILE` 指向系统 CA 包，否则报 `CERTIFICATE_VERIFY_FAILED`。
4. **Tailscale 仅 outbound**：本机（Tailscale 分配的 `100.x.x.x` 地址）不能被 tailnet 主动连入；访问 tailnet TCP 服务走 3130 隧道代理。
5. **无 Docker**：内核限制，容器内起不来 Docker，已卸载。别装。

## 步骤

### 1. 部署新 systemd 服务：必须遵守 .bak 规范

每个自建 unit 在 `/etc/systemd/system/` 落盘的同时，**必须在 `~` 下留一份 `.bak`**：

| 服务 | unit 名 | .bak 位置 |
|---|---|---|
| komari-agent | `komari-agent.service` | `~/.komari/komari-agent.service.bak` |
| kuma-push | `kuma-push.service` + `kuma-push.timer` | `~/bin/kuma-push.service.bak` 等 |
| frp-relay | `frp-relay.service` | `~/.frp/frp-relay.service.bak` |
| frpc | `frpc.service` | `~/.frp/frpc.service.bak` |
| demo-site | `demo-site.service` | `~/workspace/demo-site.service.bak` |
| hermes-gateway | `hermes-gateway.service` | `~/.hermes/hermes-gateway.service.bak` |
| ops-collect | `ops-collect.service` + `ops-collect.timer` | `~/workspace/ops-collect.service.bak` 等 |

.bak 与线上 unit 内容**必须完全一致**（`cmp` 校验），否则恢复后行为漂移。

### 2. 需要出站的服务：代理环境注入

systemd 服务看不到 shell 的代理变量，unit 里加：

```ini
EnvironmentFile=/home/hatch/.frp/proxy.env   # 或 ~/.hermes/proxy.env，600 权限
```

注意两点：

- **密码轮换陷阱**：用 `printenv` 抓到的代理密码只在当前 exec 会话有效，别 baked 进脚本长期用；`proxy.env` 里老的硬编码密码反而长期有效。
- **curl 经 systemd 连代理会 hang**（CONNECT 后卡死，exit 56）：需要访问 tailnet 的服务改走 3130 隧道代理：`curl --proxy "${https_proxy%:*}:3130"`。

### 3. Python 服务的 TLS 信任

凡经出口代理访问外网 HTTPS 的 Python 进程（Hermes 网关的 Telegram adapter 等），环境里加：

```ini
Environment=SSL_CERT_FILE=/run/hatch/egress-tls/ca-bundle.pem
```

症状对照：Telegram adapter 日志出现 `CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain` 即是此问题。

### 4. 维护 restore-infra.sh（幂等重建脚本）

`~/workspace/restore-infra.sh` 是恢复的总入口，约定：

- 幂等：逐个 `cmp` 比对 unit 与 .bak，只恢复不一致的
- 输出契约：`OK: ...`（无需动作，看门狗静默）/ `RESTORED: ...`（重建过，需通知）
- 重建后 `daemon-reload`，长驻服务 ensure `enable + active`，timer 类只 ensure enable
- 每次新增服务时**同步更新此脚本**的 unit 列表，否则新服务不在恢复范围内

### 5. 看门狗（Muse 调度侧，跨重建存活）

cron `infra-watchdog-restore`（每 10 分钟；其他调度器可用 systemd timer / cron 替代）：

- 正常时静默，只写 daily log
- `RESTORED` 时三路通知：Muse 聊天 + QQ DM（`~/workspace/qq-notify.py`）+ Telegram DM（`~/workspace/tg-notify.py`，Telegram 最稳定、无时间窗口限制）
- Telegram 通知附带 ops 状态卡片：`~/workspace/ops-card.py` 从 `status.json` 渲染手机友好的 PNG，经 `tg-notify.py --photo` 发送

## 附属物

本技能附带可直接部署的脚本与 unit 模板（均已脱敏，`<PLACEHOLDER>` 需按实际环境填写）：

- `references/scripts/restore-infra.sh` —— 幂等重建脚本（无密钥，可直接用）
- `references/scripts/kuma-push.sh` —— Kuma 心跳推送（`<KUMA_PUSH_TOKEN>`、`<KUMA_BASE_URL>` 待填）
- `references/scripts/frp-relay.py` + `frpc.toml` —— frp 中继与客户端配置（`<FRPS_HOST>`、`<FRPS_PORT>`、`<FRP_AUTH_TOKEN>` 待填）
- `references/scripts/qq-notify.py` / `tg-notify.py` —— QQ/Telegram 通知脚本（从 `~/.hermes/` 配置读密钥，无硬编码）
- `references/scripts/ops-collect.py` / `ops-card.py` —— ops 面板数据采集与状态卡片生成
- `references/systemd-units/` —— 9 个服务的 unit/timer `.bak` 模板（`komari-agent.service.bak` 的 `<KOMARI_PANEL_URL>`、`<KOMARI_AGENT_TOKEN>` 待填）

新 VM 重建流程：复制脚本到对应路径 → 填写占位符 → 按 `.bak` 规范部署 unit → 跑 `restore-infra.sh` 验证幂等。

## 检查清单

- [ ] 新增/修改 unit 后，.bak 已同步（`cmp` 无差异）
- [ ] `restore-infra.sh` 的 unit 列表包含新服务
- [ ] 需要代理的服务有 `EnvironmentFile`（600 权限）
- [ ] Python 出站服务配了 `SSL_CERT_FILE`
- [ ] 在测试环境（或模拟删除 unit）跑过一次 `restore-infra.sh`，确认输出 `RESTORED` 且服务恢复
- [ ] 密钥类（token/密码/secret）只在 600 文件里，不进文档不进 git

## 案例

- **2026-09-29**：一天 3 次整机替换。首次手动恢复时发现 `/etc` 全丢，确立 .bak 规范；当晚写出 `restore-infra.sh` 并用模拟删除验证幂等。
- **2026-09-30 08:33**：第 4 次替换，看门狗自动恢复 9 个 unit 并经 QQ 通知用户——首次实战验证。
- **2026-09-30 17:13**：第 5 次替换，看门狗恢复 + 三路通知（含 Telegram 状态卡片）全部正常。
- **教训**：`curl` 经 systemd 走 egress 代理 hang（kuma-push 曾静默失败数小时）；Telegram TLS MITM 导致 adapter 连不上（加 `SSL_CERT_FILE` 解决）；代理密码 per-session 轮换，别把刚抓的密码写进长期脚本。
