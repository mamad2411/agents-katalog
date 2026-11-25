---
name: remote-dev-sync
description: "在算力更强的远端机器改代码、本地机器 git pull 后运行的同步工作流。覆盖首次环境配置（探测网络/配代理/对齐三端）与日常同步循环（远端 commit→push→本地 pull→run）。触发词：远端开发、远端改代码本地运行、远端机器开发本地跑、remote dev sync、本地拉远端代码跑、用远端算力开发。"
---

<role>
你是一个「远端开发 / 本地运行」的 git 同步工作流专家。帮助用户在一台算力更强的远端机器上改代码，本地机器只负责拉取并运行，全程用 git 做中转。
</role>

<purpose>
当用户想「在远端机器开发、本地机器跑」时，建立并驱动一条可靠的 git 同步链路：首次把两端环境探测、配通、对齐；之后每次一键完成「远端提交 → 推送 → 本地拉取 → 本地运行」。所有机器相关的具体值（host、路径、代理、分支、运行命令）都参数化，不写死在本 skill 里——本机已跑通的真实环境沉淀到 gitignored 的 `experience.local.md`，本 skill 可分享给任何人。
</purpose>

<trigger>
远端开发 / 远端改代码本地运行 / 用远端算力开发 / remote dev sync / 本地拉远端代码跑 / 远端机器开发本地跑
</trigger>

<yolo:config>
  <yolo:mode>auto-advance</yolo:mode>
  <yolo:safety-gates>
    <gate>push 到受保护分支（main / master / release*）或任何 force / --force-with-lease push</gate>
    <gate>三端对齐时出现「非 fast-forward / 分叉」（有覆盖丢提交风险）</gate>
    <gate>写入/修改远端机器的 git 全局配置（如配代理）前</gate>
    <gate>任何 reset --hard / clean -fd / 删除分支 等破坏性操作</gate>
    <gate>探测不到运行命令、或运行命令疑似有副作用（部署、迁移、发布）时</gate>
  </yolo:safety-gates>
</yolo:config>

<gsd:workflow>
  <gsd:meta>
    <name>remote-dev-sync</name>
    <trigger>远端开发、远端改代码本地运行、remote dev sync、用远端算力开发、本地拉远端代码跑</trigger>
    <requires>Bash(ssh/git), Read, Write, Edit, AskUserQuestion</requires>
    <constraints>
      <constraint>本 skill（SKILL.md）严禁出现任何真实的 host/IP、绝对路径、用户名、仓库名、分支名、代理端口、token —— 一律用 $VAR 或 &lt;占位符&gt;，真实值只存 experience.local.md（gitignored）</constraint>
      <constraint>每个外部依赖（ssh、git、远端仓库、代理、运行命令）都必须先探测、缺失给降级，不假设作者本机环境</constraint>
      <constraint>YOLO 模式下安全门（yolo:safety-gates）仍需人工确认</constraint>
      <constraint>绝不自动 force push、绝不自动 reset --hard、绝不向受保护分支自动 push</constraint>
      <constraint>对齐三端只用 fast-forward；一旦分叉立即停下交给用户决定（rebase/merge/放弃）</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>建立并驱动「远端改、本地拉、本地跑」的 git 同步链路，首次配置 + 日常同步全自动，关键风险点人工确认</gsd:goal>

  <gsd:phase name="load-config" order="1">
    <gsd:step>读取本机 experience.local.md，有配置→直接进入 sync，无→进入 setup</gsd:step>
  </gsd:phase>
  <gsd:phase name="setup" order="2" condition="无本机配置 或 --setup">
    <gsd:step>探测两端（ssh/git/仓库/分支/remote）、探测网络与代理、配通、fast-forward 对齐三端、探测运行命令、写入 experience.local.md</gsd:step>
  </gsd:phase>
  <gsd:phase name="sync" order="3">
    <gsd:step>远端 commit→push→本地 pull→本地 run，一气呵成，仅安全门阻塞</gsd:step>
  </gsd:phase>
  <gsd:phase name="sediment" order="4">
    <gsd:step>过程中发现新模式/踩坑，写回 experience.local.md 的「有效/失败模式」表</gsd:step>
  </gsd:phase>
</gsd:workflow>

---

# Remote Dev Sync — 远端开发 / 本地运行

> 一句话：在强机器（远端）改代码，弱机器（本地）`git pull` 后运行，git 做中转。本机的具体环境沉淀在 `experience.local.md`，本文件保持通用可分享。

## 一、模型与角色

```
[远端机器 = 开发端]  改代码 → commit → push ─┐
                                            ├─→ [中转: GitHub fork 或 点对点]
[本地机器 = 运行端]  pull ← ───────────────┘  → run
```

- **远端（开发端）**：算力/环境更强，跑编辑器或 AI 编码、build。仓库路径 `$REMOTE_REPO`，ssh 目标 `$REMOTE_SSH`。
- **本地（运行端）**：只 `git pull` 后运行 `$RUN_CMD`。仓库路径 `$LOCAL_REPO`。
- **中转方式 `$SYNC_VIA`**：
  - `github`：两端都 push/pull 同一个远程（如 fork 的 `origin`）。需要两端都能访问该 git 远程（可能要代理）。
  - `p2p`：本地直接把远端机器当 git remote（走内网/SSH），不经任何托管平台。远端连不上 GitHub 时这是最省事的兜底。

## 二、参数（全部来自 experience.local.md / 探测 / 询问，永不写死）

| 变量 | 含义 | 缺失时如何获得 |
|------|------|---------------|
| `$REMOTE_SSH` | 远端 ssh 目标 `user@host` | 询问用户 |
| `$REMOTE_REPO` | 远端仓库绝对路径 | ssh 后 `find`/询问 |
| `$LOCAL_REPO` | 本地仓库绝对路径 | 当前目录/询问 |
| `$BRANCH` | 工作分支 | `git rev-parse --abbrev-ref HEAD` |
| `$GIT_REMOTE` | git 远程名（如 origin） | `git remote`（多个则询问哪个可 push） |
| `$SYNC_VIA` | `github` 或 `p2p` | 由「远端能否访问该 git 远程」探测结果决定 |
| `$PROXY` | 远端访问 git 远程所需代理 URL（可选） | 探测远端代理进程/端口 |
| `$RUN_CMD` | 本地运行命令 | 探测 package.json/Makefile/询问 |

> **隐私边界**：以上变量的*真实值*只允许出现在 `experience.local.md`（gitignored）。本 SKILL.md 及任何会进 git 的产物里只能出现变量名或占位符。

## 三、Phase 1 — 加载本机配置

```bash
EXP="$(dirname "$0")/experience.local.md"   # 与 SKILL.md 同目录
```

- `experience.local.md` 存在 → 从中读出全部 `$VAR`，**跳到 Phase 3（sync）**。
- 不存在，或用户带了 `--setup` → 进入 Phase 2。

## 四、Phase 2 — 首次配置（setup）

逐项探测 → 配通 → 对齐 → 落盘。**每个外部依赖先探测，缺失给降级。**

### 2.1 探测两端基础

```bash
# ssh 连通（免密优先）
ssh -o BatchMode=yes -o ConnectTimeout=8 "$REMOTE_SSH" 'echo OK: $(hostname)'
# 远端仓库存在 + 分支 + remote
ssh "$REMOTE_SSH" "cd $REMOTE_REPO && git rev-parse --abbrev-ref HEAD && git remote -v"
# 本地仓库 + 分支 + remote
git -C "$LOCAL_REPO" rev-parse --abbrev-ref HEAD; git -C "$LOCAL_REPO" remote -v
```

- ssh 不通 → 提示配置免密（`ssh-copy-id`）或检查网络，不继续。
- 远端无仓库 → 询问是否 `git clone`（用 `$GIT_REMOTE` 的 URL），或让用户给已有路径。
- 两端分支/remote 不一致 → 记录，后续对齐时统一。

### 2.2 探测网络与代理（决定 `$SYNC_VIA`）

```bash
# 远端能否直接访问 git 远程？
ssh "$REMOTE_SSH" "cd $REMOTE_REPO && GIT_TERMINAL_PROMPT=0 git ls-remote --heads $GIT_REMOTE $BRANCH" ; echo "exit=$?"
```

- 成功 → 远端可直连，`$SYNC_VIA=github`，无需代理。
- 失败/超时 → **不要急着判定「没网」**（被墙的连接常要几十秒才超时）。按序探测：
  1. 远端通用外网是否通：`ssh "$REMOTE_SSH" 'curl -sS -m 8 -o /dev/null -w "%{http_code}" <一个本地区域可达的站点>'`
  2. 远端是否自带代理：
     ```bash
     ssh "$REMOTE_SSH" 'ps aux | grep -iE "clash|mihomo|v2ray|xray|trojan|sing-box|surge" | grep -v grep'
     ssh "$REMOTE_SSH" 'lsof -nP -iTCP -sTCP:LISTEN | grep -E ":(7890|7891|1080|1087|10808|10802|10888|8889)"'
     ```
  3. 探到代理监听端口 → `$PROXY=http://127.0.0.1:<port>`，走 2.3 配置；`$SYNC_VIA=github`。
  4. 通用外网都不通 / 无代理 → 退回 `$SYNC_VIA=p2p`（见 2.4 备选），本地直接从远端拉，绕开托管平台。

### 2.3 配置远端 git 走代理（仅 `$SYNC_VIA=github` 且需要代理）

> 🛑 **安全门**：写远端 git 全局配置前确认。

只对目标 git 主机走代理，不影响远端访问其它仓库：

```bash
# $GIT_HOST 形如 https://<git平台域名>/
ssh "$REMOTE_SSH" "git config --global http.$GIT_HOST.proxy $PROXY && git config --global https.$GIT_HOST.proxy $PROXY"
# 验证（不带 -c，靠持久化配置）
ssh "$REMOTE_SSH" "cd $REMOTE_REPO && GIT_TERMINAL_PROMPT=0 git ls-remote --heads $GIT_REMOTE $BRANCH"
```

### 2.4 fast-forward 对齐三端

目标：`$LOCAL_REPO`、`$REMOTE_REPO`、远程同步到同一 HEAD。先看清谁领先：

```bash
git -C "$LOCAL_REPO" rev-parse HEAD
ssh "$REMOTE_SSH" "cd $REMOTE_REPO && git rev-parse HEAD"
GIT_TERMINAL_PROMPT=0 git -C "$LOCAL_REPO" ls-remote --heads $GIT_REMOTE $BRANCH
```

- 落后端 fast-forward 追上领先端（领先端先 push 到远程，落后端再 pull）。
- 🛑 **安全门**：若两端各有独有提交（分叉，非 fast-forward）→ **停下**，把状态摆给用户，让其选择 rebase / merge / 放弃某端，**绝不自动覆盖**。
- `$SYNC_VIA=p2p` 时：本地 `git remote add <name> ssh://$REMOTE_SSH/$REMOTE_REPO`，用 `git pull <name> $BRANCH` 对齐（从远端拉是安全的；不要反向 push 到远端已 checkout 的分支）。

### 2.5 探测运行命令 `$RUN_CMD`

```bash
# Node: 读 package.json scripts；Make: 读 Makefile 目标；其它语言相应探测
node -e "const s=require('$LOCAL_REPO/package.json').scripts||{};Object.keys(s).forEach(k=>console.log(k))" 2>/dev/null
```

- 探到候选 → 让用户挑「运行入口」（如 `pnpm dev` / `pnpm cli`），存为 `$RUN_CMD`。
- 🛑 **安全门**：候选命令疑似部署/迁移/发布（`deploy`/`release`/`migrate`/`publish`）时确认，别误跑。

### 2.6 写入 experience.local.md

把上面解析出的真实值写入 `experience.local.md`（结构见第六节），并 `chmod 600`。完成后 setup 结束。

## 五、Phase 3 — 日常同步循环（sync · YOLO 一气呵成）

```bash
# ① 远端提交（有改动才 commit）
ssh "$REMOTE_SSH" "cd $REMOTE_REPO && git add -A && (git diff --cached --quiet || git commit -m '<message>')"
# ② 远端推送（feature 分支常规 push 放行；受保护分支/force → 安全门）
ssh "$REMOTE_SSH" "cd $REMOTE_REPO && git push $GIT_REMOTE $BRANCH"
# ③ 本地拉取（只接受 fast-forward；分叉则停）
git -C "$LOCAL_REPO" pull --ff-only $GIT_REMOTE $BRANCH
# ④ 本地运行
cd "$LOCAL_REPO" && $RUN_CMD
```

- `$SYNC_VIA=p2p`：跳过 ②，③ 改成 `git -C "$LOCAL_REPO" pull --ff-only <name> $BRANCH`（直接从远端机器拉）。
- ③ 若 `--ff-only` 失败（本地也有改动 → 分叉）→ 🛑 安全门，停下交给用户。
- commit message：用户没给就用简短祈使句概括远端 `git diff --stat`，不要写空消息。

## 六、experience.local.md —— 本机沉淀（gitignored，可写真实值）

仿 web-search 的两层分离：本文件装私货，**不进 git、不分享**。由本 skill 自动维护，只写验证过的事实。模板：

```markdown
setup-completed: <ISO8601>

# Remote Dev Sync 本机配置与经验
> 此文件由 LLM 自动维护，已被 .gitignore 忽略，不分享。只写经过验证的事实。

## 本机环境（已跑通）
| 变量 | 值 |
|------|-----|
| REMOTE_SSH | <user@host> |
| REMOTE_REPO | <远端仓库绝对路径> |
| LOCAL_REPO | <本地仓库绝对路径> |
| BRANCH | <分支> |
| GIT_REMOTE | <remote 名> |
| SYNC_VIA | github / p2p |
| PROXY | <代理 URL 或 无> |
| RUN_CMD | <运行命令> |

## 有效模式
| 结论 | 日期 | 场景 |
|------|------|------|

## 失败模式
| 陷阱 | 日期 | 正确做法 |
|------|------|---------|
```

## 七、常见陷阱（通用，可分享）

| 现象 | 真因 | 正确做法 |
|------|------|---------|
| 远端 `git push` 几十秒后超时，以为「没网」 | 目标 git 平台被墙，但远端通用外网正常 | 先探测远端代理进程/端口，给 git 配 host 专用代理，别直接判没网 |
| 远端配了全局代理，访问其它（区域内）仓库变慢/失败 | 全局代理影响所有 git 主机 | 用 `http.<git平台域名>.proxy` 只对目标平台走代理 |
| 本地 pull 报非 fast-forward | 本地也有独有提交，与远端分叉 | 停下，rebase 或 merge，绝不 force 覆盖 |
| 想从远端机器拉但 push 被拒 | 远端是非 bare 仓库且分支已 checkout | 用「本地 pull 远端」方向（p2p），而非 push 到远端 |
| 运行端跑的是旧代码 | 对齐没做或 pull 没成功 | 每次 sync 后核对 `git rev-parse HEAD` 两端一致 |

## 八、自检 / 维护规则（写回本 skill，不写个人记忆）

- 本 skill 位于分享仓库，行为偏差请改 SKILL.md 本身，**不要**写进个人 auto-memory。
- 任何真实环境值只进 `experience.local.md`；改 SKILL.md 时 grep 自查无 `/Users/`、IP、端口、token。
