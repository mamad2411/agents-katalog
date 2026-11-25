---
title: "Komari Agent Auto Discovery"
type: skill
tags: [komari, monitoring, agent, auto-discovery, systemd]
created: 2026-11-02
updated: 2026-11-02
author: scriptsmay
status: active
---

# Komari Agent Auto Discovery

用自动发现密钥（auto discovery key）把一台新机器 self-register 到已有的 Komari 主服务上，不需要面板管理员事先逐台创建节点、逐台发 token。适合批量接管、以及把接管步骤交给另一个 agent 执行。

Register a new machine to an existing Komari server with an auto discovery key: the agent enrolls itself, no per-node token needs to be created in the panel beforehand. Suitable for batch onboarding and for handing the onboarding step to another agent.

> **本技能不含任何真实地址与密钥。** 面板地址与自动发现密钥必须由面板管理员通过私密通道单独交给执行方，本文档里的所有地址与 key 均为占位符。
> This skill contains no real endpoint or key. The panel owner must hand both values to the executor through a private channel; every address and key below is a placeholder.

## 为什么用自动发现 / Why

Komari 有两种接管方式，容易混淆：

| 方式 | 面板侧操作 | Agent 侧参数 | 适用场景 |
| :--- | :--- | :--- | :--- |
| 逐台 token（`-t`） | 管理员先在面板建节点，逐台发 token | `-e <endpoint> -t <NODE_TOKEN>` | 机器少、逐台可控 |
| 自动发现（`--auto-discovery`） | 管理员只保管一个自动发现密钥 | `-e <endpoint> --auto-discovery <AD_KEY>` | 批量部署、交给另一个 agent 执行 |

自动发现的关键结论（对照 Komari 官方文档 Agent Auto Discovery 核实）：

1. 自动发现让 agent **自己向主服务注册**，注册成功后节点出现在面板里，之后按面板里的节点管理。
2. 需要 Komari 主服务 **1.0.4 或以上版本**，低于该版本没有此功能。
3. 只有两个必填参数：`-e / --endpoint`（主服务地址）与 `--auto-discovery`（自动发现密钥）。
4. 自动发现密钥是**主服务级别的注册凭证**：拿到它的人可以往面板里注册节点。因此它与节点 token 同等敏感，用完一批后请面板管理员在后台更换/作废，绝不能进仓库、进日志、进群聊记录。

## 前置条件 / Prerequisites

- 一台已部署且可通过 HTTPS 访问的 Komari 主服务（版本 ≥ 1.0.4）。
- 面板管理员已通过私密通道提供两项值：主服务地址、自动发现密钥。
- 执行方在目标机器上有 root（Linux/macOS）或管理员（Windows）权限。
- 目标机器能直接访问主服务地址；若目标机器走出站代理，按自己的部署在环境里补代理变量（见 references 模板注释）。

## 变量 / Variables

| 占位符 / 环境变量 | 含义 | 说明 |
|---|---|---|
| `<KOMARI_ENDPOINT>` / `KOMARI_ENDPOINT` | Komari 主服务根地址，如 `https://komari.example.com` | 不要带尾随路径；必须是 agent 能访问的地址 |
| `<AUTO_DISCOVERY_KEY>` / `KOMARI_AD_KEY` | 自动发现密钥 | 只放环境变量或权限 600 的本地文件，**不进仓库、不进日志、不回显** |
| `KOMARI_AD_KEY_FILE` | 密钥文件路径（可选） | 文件内容为单行密钥；读取时去掉尾随换行 |

## 给 Agent 的执行约定 / Agent Guide

另一个 agent（或自动化脚本）按本技能接管时，按以下顺序执行，不要跳步：

1. **先备齐两个变量再动手**：从环境变量或 600 权限文件解析 `KOMARI_ENDPOINT` 与 `KOMARI_AD_KEY`。缺任何一项就停下来向面板管理员索取，不要猜地址、不要用示例域名发真实请求。
2. **全程不回显密钥**：密钥不打印、不写日志、不拼进可分享的命令记录；向用户汇报时只说“已注册/未注册”，不贴完整命令。
3. **优先用官方安装脚本**：官方 `install.sh` / `install.ps1` 会处理二进制下载与服务安装；手写 systemd 单元时用 `references/komari-agent.service` 模板，密钥走 `EnvironmentFile`，不要把密钥写进 `ExecStart`（进程列表可见）。
4. **注册后以面板为准验收**：节点出现在面板且指标开始上报才算成功；只看 agent 进程存活不算。
5. **密钥用后处理**：批量接管完成后提醒面板管理员更换/作废该密钥；本机留下的密钥文件按管理员意见保留或删除，不要自行扩散。

## 步骤 / Steps

### 1. 准备变量

```bash
export KOMARI_ENDPOINT="https://<KOMARI_ENDPOINT>"
# 方式 A：直接放环境变量（仅当前 shell）
export KOMARI_AD_KEY="<AUTO_DISCOVERY_KEY>"
# 方式 B：放 600 权限文件（推荐，systemd 模板即用此方式）
cat > /etc/komari/ad-key.env << 'EOF'
KOMARI_ENDPOINT="https://<KOMARI_ENDPOINT>"
KOMARI_AD_KEY="<AUTO_DISCOVERY_KEY>"
EOF
chmod 600 /etc/komari/ad-key.env
```

### 2. 一键安装（Linux / macOS，推荐）

```bash
bash <(curl -sL https://raw.githubusercontent.com/komari-monitor/komari-agent/refs/heads/main/install.sh) \
  -e "$KOMARI_ENDPOINT" \
  --auto-discovery "$KOMARI_AD_KEY"
```

生产向可加常用选项（含义见下表）：

```bash
bash <(curl -sL https://raw.githubusercontent.com/komari-monitor/komari-agent/refs/heads/main/install.sh) \
  -e "$KOMARI_ENDPOINT" \
  --auto-discovery "$KOMARI_AD_KEY" \
  --disable-web-ssh \
  --interval 5.0 \
  --max-retries 5 \
  --reconnect-interval 10 \
  --info-report-interval 15
```

### 3. Windows

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "iwr 'https://raw.githubusercontent.com/komari-monitor/komari-agent/refs/heads/main/install.ps1' -UseBasicParsing -OutFile 'install.ps1'; & '.\install.ps1' '-e' 'https://<KOMARI_ENDPOINT>' '--auto-discovery' '<AUTO_DISCOVERY_KEY>'"
```

### 4. 手动安装（已有二进制、需自写服务时）

```bash
# 先放好 references/komari-agent.service 模板并填好 EnvironmentFile，再：
systemctl daemon-reload
systemctl enable --now komari-agent
```

### 5. 验收清单

- [ ] 面板里出现新节点，名称与目标机器一致。
- [ ] 节点开始上报 CPU / 内存 / 磁盘 / 流量指标（等一个上报间隔，默认约 3 秒一次，基础信息约 5 分钟一次）。
- [ ] `systemctl status komari-agent` 为 active（Linux），或服务管理器中状态正常（Windows）。
- [ ] 日志无持续重连报错：`sudo journalctl -u komari-agent -f`（Linux）。

## 参数对照 / Parameters

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `-e, --endpoint` | 必填 | Komari 主服务地址 |
| `--auto-discovery` | 必填 | 自动发现密钥，用于 agent 自注册 |
| `--disable-auto-update` | `false` | 关闭 agent 自动更新（版本需与主服务配对时用） |
| `--disable-web-ssh` | `false` | 关闭 Web SSH / 远程执行等远程控制功能 |
| `-u, --ignore-unsafe-cert` | `false` | 忽略无效 TLS 证书——**生产环境不要用** |
| `-i, --interval` | `1.0` | 监控上报间隔（秒） |
| `--info-report-interval` | `5` | 基础信息上报间隔（分钟） |
| `-r, --max-retries` | `3` | 最大重试次数 |
| `-c, --reconnect-interval` | `5` | 重连间隔（秒） |
| `--month-rotate` | `0` | 月流量重置日，`0` 为关闭 |
| `--install-dir`（仅安装脚本） | Linux `/opt/komari`，Windows `$Env:ProgramFiles\Komari` | agent 安装目录 |
| `--install-service-name`（仅安装脚本） | `komari-agent` | 系统服务名 |

## 故障排查 / Troubleshooting

| 现象 | 先查什么 |
| :--- | :--- |
| agent 起不来 / 反复重连 | 目标机器能否访问 `$KOMARI_ENDPOINT`（先 curl 面板地址）；再核对密钥是否正确（错一个字符即注册失败） |
| 提示权限不足 | 安装脚本是否以 root / 管理员身份运行 |
| 节点迟迟不出现在面板 | 看 agent 日志（`journalctl -u komari-agent -f`），确认它连的是正确的 endpoint，而不是示例域名 |
| 证书报错 | 不要图省事加 `-u`；先修主服务的证书或系统 CA 信任链 |
| 版本不匹配 | 确认主服务 ≥ 1.0.4；agent 与主服务版本跨度大时先对齐再升级，不要单边升 agent |

## 参考 / References

- Komari 官方文档：Agent Auto Discovery（`komari-document`，install/agent-ad）
- 本仓库模板：`references/komari-agent.service`（systemd 单元，密钥走 EnvironmentFile）
