---
name: claude-code-guard
description: >
  给客户机器配置 Claude Code 防封：先探测对方电脑上实际在跑的梯子和系统（macOS / Windows），再让客户选定固定节点后才落地时区、本地代理绑定、Hook、指纹浏览器，并清理旧账号残留凭证与 machineID。
  触发：Claude 防封、Claude Code 被封、秒封、台湾节点、Windows、Clash、v2rayN、Camoufox、指纹浏览器、清理凭证、chain key、machineID、/claude-code-guard。
---

# Claude Code 防封配置

把 Claude Code 绑到**客户自己梯子上的一个固定出口**。梯子品牌、端口、控制口、操作系统都**先探测，禁止写死成作者这台 Mac / Clash Verge**。

**先让客户选定一个固定节点。** 没拿到完整叶子名之前，禁止改配置、装 Hook、开登录。

权威细节：

- 分层：`references/layers.md`
- 客户端差异：`references/clients.md`
- 指纹浏览器：`references/fingerprint.md`
- 旧身份：`references/identity-purge.md`

脚本是跨平台 Python，在 `scripts/`。

## 硬性门槛

1. 先探测并列出节点，然后**停住**。
2. 必须等客户回复**一个固定叶子的完整名字**。推荐台湾，但不替他选、不默认第一项。
3. 自动切换 / 负载均衡 / 策略组名一律不收。
4. 列不出节点时：客户先在自己客户端里点好固定节点，再把那个名字发过来（仍要 `--node`，没有「跳过选节点」）。
5. 换号 / 曾被封：先扫描身份，客户确认后再清。

## 流程

### 1. 探测，不要假设

```bash
python3 "<SKILL>/scripts/ccg_detect.py"
```

Windows 用 `py -3` 或 `python`。看 JSON 里的：

- `os`：`darwin` / `windows`
- `family`：`clash-mihomo`（能列节点）或 `local-proxy`（只能绑端口）
- `clients`：实际进程
- `recommended_nodes`：名字像台湾/家宽的叶子
- `bind_port` / `controller` / `notes`

```bash
python3 "<SKILL>/scripts/ccg_detect.py" --list
```

把清单发给客户，问：「选一个固定节点，回复完整名字。」**在这里停，不要往下装。**

### 2. 选节点（客户点名之后才继续）

- 台湾叶子：`expected_region=TW`，`TZ=Asia/Taipei`
- 客户坚持其他地区：区域码跟出口 `loc` 一致，时区跟该 IP 的 GeoIP 一致，并说明风险更高
- 名字必须和列表里的叶子一致（能列出时）

### 3. 旧身份

```bash
python3 "<SKILL>/scripts/ccg_identity.py" scan
```

macOS 查钥匙串，Windows 查凭据管理器。有残留且客户确认换号/曾被封：

```bash
python3 "<SKILL>/scripts/ccg_identity.py" purge --yes
```

换号加 `--purge-browser`。先退出 Claude。

### 4. 按探测结果安装

```bash
python3 "<SKILL>/scripts/ccg_install.py" --node "<客户回复的完整叶子名>" --region TW
```

没有 `--node` 会失败。安装写入 `~/.claude-guard/state.json`。

### 5. 指纹浏览器

代理必须是 state 里的 `upstream_port`，不是系统默认浏览器。见 `references/fingerprint.md`。

### 6. 验收

1. `python3 ~/.claude-guard/ccg_guard.py --fast`
2. `python3 ~/.claude-guard/ccg_guard.py --status` 地区正确
3. 清身份后 scan 不再报旧 oauth / 凭据
4. 用 wrapper 启动（Windows：`wrapper.ps1`，无进程沙箱）
5. 登录后再 `--status` 一次

## 不要做

- 把作者的 Hinet 名、`/tmp/verge/...`、7897 写进客户配置
- 把自动选组当成固定节点
- 未探测就按 Mac + Clash Verge 施工
- 打印 token / machineID / 邮箱
- 在 Windows 上假装有 Seatbelt
