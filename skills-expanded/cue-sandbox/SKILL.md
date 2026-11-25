---
name: cue-sandbox
description: Cue 沙盒的 SSH、EasyTier mango-mesh TUN、Komari 探针与 overlay 挖矿接入 SOP。用于用户提到 cue、mesh-cue、cue-tunnel、Cue 探针、Cue EasyTier、Cue reverse-ssh、10.144.144.81、easytire/easytier Cue、印度中继兜底，或要把无公网入站的 Cue 接到 mesh / Komari / 挖矿中枢时。日常走 mesh，不要把印度 VPS 当登录机。自包含执行：先探测本机，一次性向操作者索取所需配置，直接落地。
---

# Cue 沙盒接入（SSH / EasyTier / 探针）

Cue 没有公网入站。日常登录走 EasyTier TUN。印度 VPS 只反弹 SSH 兜底。探针跑在 Cue 本机。挖矿走 Hub overlay 口，不走公网 7019。

本 skill 是**完全自包含的独立操作规程**。所有配置均由本机探测结果与操作者输入的参数构成，无需任何外部文档库或知识库。探测本机 → 一次性列出缺的输入 → 操作者补齐后立即落地。严禁停下来索取外部文档。

```text
操作者  ssh mesh-cue  ──EasyTier──►  Cue ubuntu@<CUE_OVERLAY>:22
                                      │
                                      ├ easytier-mango-mesh (TUN: <CUE_INSTANCE_NAME>)
                                      ├ komari-agent → <KOMARI_ENDPOINT>
                                      └ srb-xel → <HUB_OVERLAY>:7019   ← 仅用户明确要求
                                      │
Cue ssh -R 0.0.0.0:<TUNNEL_REMOTE_PORT>:localhost:22 ─► 印度 <INDIA_USER>@<INDIA_PUBLIC_IP>:<TUNNEL_REMOTE_PORT>   ← 仅兜底
```

深度细节按需读，不要一上来全读：

- `references/ssh.md`：两把钥、GatewayPorts、sshd、SSH config
- `references/easytier.md`：TUN 模板、systemd 单元、验收命令
- `references/probe.md`：token 签发、ICMP、挖矿三件套（默认跳过）

## 步骤 1：探测本机环境

在当前机器上跑，保存输出，用来决定自己是 Cue 还是操作者本机：

```bash
hostname; whoami; uname -m
ip -4 addr show tun0 2>/dev/null || echo "no tun0"
test -e /dev/net/tun && echo "tun-ok" || echo "no-tun"
systemctl is-active easytier-mango-mesh 2>/dev/null || echo "no-easytier-unit"
systemctl is-active komari-agent 2>/dev/null || echo "no-komari"
systemctl is-active srb-xel 2>/dev/null || echo "no-miner"
ss -tlnp | grep -E ':22 |:2222 ' || true
```

判定：

- 有 `/dev/net/tun`、用户是 `ubuntu`（或即将成为 Cue 的 Linux 沙盒）→ **你在 Cue 上**。直接按下面「Cue 本机落地」步骤执行。
- 有 `ssh mesh-cue` / `~/.ssh/cue-access-key` → **你在操作者本机**。写 SSH config、装访问钥，不要在本机起 EasyTier 当 Cue。
- 两边都不是 → 问操作者：目标是「把当前这台接成 Cue」还是「从这台登录已有 Cue」。只问这一句。

**挖矿默认跳过。** 只有用户明确说挖矿 / srb-xel / overlay 7019 才读 `references/probe.md` 的矿池段。已在跑的矿不要重装。

## 步骤 2：一次性收集所需配置

把缺的项列成一张表，一次发给操作者。已探测到的不要再问。私钥、token、mesh secret、钱包只写路径或让操作者在目标机本地粘贴，**不要**让他们发到聊天。

| 占位符 | 谁提供 | 何时必需 | 不要问的情况 |
|---|---|---|---|
| `<CUE_INSTANCE_NAME>` | 默认 `cue`；多机填 `cue-2` 等 | EasyTier | 已有 `config.toml` 的 `instance_name` |
| `<CUE_OVERLAY>` | 操作者，首台沿用 `10.144.144.81/24`，多台递增如 `.82` | EasyTier | 本机 `tun0` 已持有有效 overlay |
| `<MESH_NAME>` | 默认 `mango-mesh` | EasyTier | 已有 `config.toml` 的 `network_name` |
| `<MESH_SECRET>` | 操作者从现网模板抄，禁止手编 | EasyTier | 已有匹配的 `network_secret` |
| `<TENCENT_HUB>` `<HK_HUB>` | 操作者：两个 Hub 的 `host:11010` | EasyTier | 已有双 `[[peer]]` |
| `<ACCESS_PUBKEY>` | 操作者本机 `cue-access-key.pub` 一行 | SSH | Cue `authorized_keys` 已能登录 |
| `<INDIA_PUBLIC_IP>` `<INDIA_USER>` | 操作者；用户默认 `azureuser` | 只要兜底 | 用户只要 mesh、不要兜底 |
| `<TUNNEL_REMOTE_PORT>` | 兜底端口：首台 `2222`，多机递增（如 `2223`） | 只要兜底 | 用户只要 mesh、不要兜底 |
| `<KOMARI_ENDPOINT>` | 操作者：Hub HTTPS 入口 | 探针 | 用户明确不要探针 |
| Komari token | Hub `admin:addClient`，只写入 Cue env | 探针 | 已有 `/etc/komari-agent.env` |
| `<HUB_OVERLAY>` | 矿池宿主 Overlay IP，默认 `10.144.144.2` | 仅用户明确要求挖矿 | 默认跳过挖矿 |
| 钱包 / worker | 操作者 | 仅用户明确要求挖矿 | 默认跳过挖矿 |

## 先决定

1. **日常入口是 mesh。** `ssh mesh-cue` 通了就不要改印度。印度挂了只断 `cue-tunnel`。
2. **Cue 有 TUN。** 不要抄 Muse VM / Bohrium 的 `--no-tun` + SOCKS5。
3. **两把钥。** 访问钥只在操作者本机，公钥只装 Cue 登录用户。隧道钥只在 Cue，公钥只装印度 `<INDIA_USER>`。不要用 `id_rsa` 当隧道钥，不要在印度建 `ubuntu`，不要把访问钥放到任何 VPS。
4. **操作者笔记本不是隧道的一端。** Cue 自己连出 `-R`。不要等 Windows，也不要为这条隧道改 Mac。
5. **挖矿已在跑就不要重装。** 排障不要 `journalctl` SRBMiner，不要 `SRBMiner --version`。

## Cue 本机落地（按序，可中途停）

每一步的命令在对应 `references/`。做完一步立刻验收，失败不要跳到下一步。

1. **EasyTier TUN** — 读 `references/easytier.md`。Hub `easytier-cli peer` 能看到本机 overlay。没有 Hub 操作权就在 Cue 上看 `tun0` + `systemctl is-active easytier-mango-mesh`。
2. **访问钥** — 读 `references/ssh.md`。公钥进 Cue 登录用户 `authorized_keys`。操作者本机写 `Host mesh-cue`。先 mesh 登录成功。
3. **印度兜底（可选）** — 用户没提 2222 / cue-tunnel 就跳过。要做：隧道钥只在 Cue 生成；印度 `GatewayPorts clientspecified`（不要 `yes`）+ 云防火墙 2222。
4. **探针（可选）** — 用户没提 Komari / 探针就跳过。要做：读 `references/probe.md`。Hub loopback `admin:addClient` → `/etc/komari-agent.env` 600 → systemd → `ping_group_range`。
5. **挖矿（可选，默认不做）** — 池写成 overlay `<HUB_OVERLAY>:7019`，白名单 `_static_ips`，探针带 miner URL + `{action}`，且 **不要** `--disable-web-ssh`。

## 铁律

- 私钥、token、secret、钱包不进仓库、文档、skill、聊天；只写路径和指纹。
- `GatewayPorts clientspecified`；Cue 公网面 `PasswordAuthentication no`。
- Komari token 只从 Hub 签发，不发明。API Key 是 admin 全权：只用在 Hub 必要节点，用完清临时文件。
- 挖矿节点禁止 `AGENT_DISABLE_WEB_SSH=true`。
- 白名单用 Hub `tcpdump` 和 `_static_ips`，不用 ipify，不改 `hub.env`。
- GitHub `releases/latest` 对 prerelease 404，二进制钉 snapshot 标签。
- 严禁停工索取外部文档或知识库。直接依据探测结果与操作者提供的参数执行配置。

## 验收

最少集（mesh only）：

- Cue：`ip -4 addr show tun0` 持有 `<CUE_OVERLAY>`；`systemctl is-active easytier-mango-mesh` 为 `active`。
- 操作者：`ssh mesh-cue 'hostname; ip -4 addr show tun0'` 落到 Cue。

按需追加：

- Hub peer 列表有本机 hostname、p2p、0% loss。
- 探针日志 `Basic info uploaded` + `WebSocket connected`；Ping 任务 loss=0。
- 挖矿节点：`miner_configured` 与 `miner_controllable` 均为 true；`--pool` 是 overlay 不是公网 7019。

向用户汇报时写：做了哪几步、跳过了哪几步、缺的输入还剩什么。不要因为跳过可选步骤而宣称失败。
