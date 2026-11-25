---
name: config-file-versioning
description: 给小型本地配置文件设置自动版本备份，便于回滚被覆写/误改。当用户希望给某几个 config 文件（如 ~/.ssh/config、~/.zshrc、应用 dotfile 等）加版本史/防覆写/可一键回滚时使用。统一架构：separate-git-dir + 白名单 .gitignore + 操作系统级文件监听 + 自动 commit 脚本。一个被保护的 config 域 = 一个独立小仓库。原生支持 macOS（launchd），Linux/其他可参照同思路换用 systemd path unit / inotifywait / gitwatch 实现监听层。
license: MIT
---

# Skill: Config File Versioning

给"小型 + 重要 + 不希望被悄悄覆盖"的本地配置文件做自动版本备份。

每次被监听文件**实际内容变化**时，10 秒内自动产生一条 git commit，保留在一个本地 separate-git-dir 仓库里。一键回滚到任意历史版本。

---

## 何时使用

用户出现下列任一**触发信号**就用本 skill：

- "给 \<某文件\> 加自动版本/备份/防覆写"
- "我不想哪天某程序又把我的 \<某 dotfile\> 覆盖了"
- "自动 commit 当 \<某 config\> 有变化"
- "参考 \<已有备份目录\> 给我备份 \<其他文件\>"
- 用户提到关键 config 被某工具/手贱覆盖丢失，问怎么以后预防

**不适用**于：

- 大型代码仓库（直接用普通 git workflow 就行）
- 跨机器同步（本 skill 只做本地版本史；要同步加 syncthing 或手动 git push 到私有 remote）
- 频繁高速变动的文件（`.bash_history`、`history.jsonl` 之类——会产生海量 commit）

---

## 架构总览

```
   <被保护文件>           (实际位置，例 ~/.ssh/config)
        │ 修改
        ▼
   OS 级文件监听
   ┌──────────────────────────────┬──────────────────────┬─────────┐
   │ macOS: launchd WatchPaths    │ Linux: systemd .path │ 其他    │
   └──────────────────────────────┴──────────────────────┴─────────┘
        │ 触发（10s 节流后）
        ▼
   auto-commit.sh
        │ git add -A → 仅当 staged diff 非空时 commit
        ▼
   <BACKUP_ROOT>/<domain>-config.git/   ← 真正的 git repo（separate-git-dir）
        ▲
        │ 由 worktree 根的 ".git"（一行 gitdir: 文本）连接
```

**关键设计点：**

| 设计 | 理由 |
|---|---|
| **每个 config 域独立仓库**（不合并到一个大仓库） | 历史干净；可独立启用/禁用/迁移 |
| **separate-git-dir** | worktree 整个被某程序删光时，历史依然在 `<BACKUP_ROOT>` 里活着 |
| **白名单 `.gitignore`**（`*` + `!<被保护文件>`） | 不会误吞同目录下的运行时数据/缓存/临时文件 |
| **事件驱动监听 + 节流**（默认 10s） | 平时无常驻进程；避免一次写入产生多条 commit |
| **commit 脚本里 `git diff --cached --quiet` 检查** | 内容真无变化（仅 mtime 改）时静默退出 |

---

## 实施步骤

### 步骤 0：跟用户对齐 4 个变量

| 变量 | 含义 | 推荐默认值 |
|---|---|---|
| `<DOMAIN>` | 配置域简称（仅小写字母数字短横线，作目录名/Label 后缀） | 跟用户讨论；例：`ssh` / `zsh` / `vscode` / `claude` |
| `<WORKTREE>` | 被保护文件所在的目录绝对路径（git worktree 根） | 通常等于被监听文件所在目录 |
| `<FILES>` | 要监听的绝对路径列表（≥ 1） | 由用户指定 |
| `<BACKUP_ROOT>` | 仓库 + 脚本 + 服务模板的存放根目录 | **必问**：默认建议 `~/.local/share/config-versioning/<DOMAIN>/`（XDG 数据目录约定）；若用户已有专属备份/同步目录（如 `~/Documents/backups/`、`~/Sync/...`、自己的沙盒目录），让用户决定 |

### 步骤 1：建数据目录 + 起 git 仓库

```bash
mkdir -p "<BACKUP_ROOT>"

mkdir -p "<WORKTREE>"
cd "<WORKTREE>" && git init -q -b main
```

### 步骤 2：写白名单 `.gitignore`

复制 [`templates/gitignore-whitelist`](templates/gitignore-whitelist) 到 `<WORKTREE>/.gitignore`，然后把 `<FILES>` 里每一项相对 `<WORKTREE>` 的路径加 `!<rel-path>` 一行。

例：worktree=`~/.ssh`，要保护 `~/.ssh/config` 和 `~/.ssh/known_hosts`，就加：

```
!config
!known_hosts
```

### 步骤 3：初始 commit

```bash
cd "<WORKTREE>"
git add -A
git commit -q -m "chore: initial snapshot of <DOMAIN> config"
```

> 不要用 `-c user.name/-c user.email` 强制覆盖——让 git 用用户全局配置。仓库纯本地，不 push，提交人无关紧要。

### 步骤 4：把 `.git` 目录搬到 `<BACKUP_ROOT>` 并留 gitdir 指针

```bash
GITDIR="<BACKUP_ROOT>/<DOMAIN>-config.git"
mv "<WORKTREE>/.git" "$GITDIR"
echo "gitdir: $GITDIR" > "<WORKTREE>/.git"
git -C "$GITDIR" config core.worktree "<WORKTREE>"
```

### 步骤 5：复制 + 改写 auto-commit 脚本

复制 [`templates/auto-commit.sh`](templates/auto-commit.sh) 到 `<BACKUP_ROOT>/auto-commit.sh`，替换 2 个占位符：

| 占位符 | 替换为 |
|---|---|
| `__WORKTREE__` | `<WORKTREE>` 绝对路径 |
| `__LOG__` | 日志路径，建议 `~/Library/Logs/config-file-versioning.log`（macOS）或 `~/.local/state/config-file-versioning.log`（Linux） |

`chmod +x` 它。

### 步骤 6：装监听层（按操作系统分支）

#### 6a. macOS（launchd LaunchAgent）

复制 [`templates/launchagent.plist`](templates/launchagent.plist)，替换占位符：

| 占位符 | 替换为 |
|---|---|
| `__LABEL__` | `local.<USER>.<DOMAIN>-config-watch`（`local.` 前缀避免冲突；`<USER>` 用 `$USER`） |
| `__SCRIPT_PATH__` | `<BACKUP_ROOT>/auto-commit.sh` 绝对路径 |
| `__WATCH_PATHS__` | `<FILES>` 里每个文件包一对 `<string>...</string>`，整体放在 `<array>` 里 |
| `__LOG__` | 同步骤 5 |

写两份（保证目录可迁移）：

1. `<BACKUP_ROOT>/<LABEL>.plist`（备份模板）
2. `~/Library/LaunchAgents/<LABEL>.plist`（实际生效）

加载：

```bash
launchctl unload "$HOME/Library/LaunchAgents/<LABEL>.plist" 2>/dev/null
launchctl load   "$HOME/Library/LaunchAgents/<LABEL>.plist"
launchctl list | grep "<LABEL>"   # 验证已注册
```

#### 6b. Linux（systemd path unit）

复制 [`templates/systemd.path`](templates/systemd.path) 和 [`templates/systemd.service`](templates/systemd.service) 到 `~/.config/systemd/user/`，改名为 `<DOMAIN>-config-watch.path` 和 `<DOMAIN>-config-watch.service`，按文件内的占位符替换。然后：

```bash
systemctl --user daemon-reload
systemctl --user enable --now <DOMAIN>-config-watch.path
```

#### 6c. 其他 / 兜底

任何能"watch + run command"的工具都行：

- **gitwatch**（跨平台 shell）：`brew install gitwatch` 或 `apt install gitwatch`
- **fswatch + 自管 daemon**：`fswatch <FILES> | xargs -n1 <BACKUP_ROOT>/auto-commit.sh`
- **inotifywait（Linux）+ shell 循环**

把 watcher 进程托管到对应平台的服务管理器（OpenRC、runit、launchd、systemd）。

### 步骤 7：端到端测试（必做，不可跳）

改一个被监听文件，等比节流间隔多 2 秒，确认日志和 git log 各加一条。先注入临时字段，再清掉，期望产生 2 条 commit：

```bash
# 例：JSON 文件加临时键 _autoCommitTest
# sleep 12 (假设节流=10s)
tail -2 "<LOG>"
git -C "<WORKTREE>" log --oneline | head -3
```

### 步骤 8：写 README

每个 `<BACKUP_ROOT>` 都自带一份 README.md，便于以后迁移。最少包含：

- 目的（为什么有这套）
- 文件清单表
- 日常命令（看历史、回滚、查 watcher 状态、看日志）
- 维护（加新监控文件、改节流间隔）
- 在新机器上重建步骤
- 完整卸载步骤

---

## 反模式（明确避免）

| ❌ 错的做法 | ✅ 正确 |
|---|---|
| 多个 config 域塞同一个 git 仓库 | 一个域一个仓库 |
| `.git` 留在 worktree 内 | 搬到 `<BACKUP_ROOT>` 用 gitdir 指针 |
| 用黑名单 .gitignore | 用白名单 |
| 跳过端到端测试就交付 | 必做，确认 commit 真的产生 |
| 把 plist/service 单元只放系统目录，不在 `<BACKUP_ROOT>` 留模板 | 两处都放，保证目录自包含可迁移 |
| commit 时 push 到公共远端 | **禁止**——配置可能含 token / 机敏信息，纯本地仓库 |
| 在 `auto-commit.sh` 里硬编码 git user.name/email | 留给 git 全局配置；脚本不该带个人信息 |
| 用 KeepAlive=true 跑 fswatch 常驻 | 优先用事件驱动（WatchPaths / .path unit），无常驻进程 |

---

## 边界情况处理

- **worktree 目录不存在**：先 `mkdir -p`。如果是首次，被监听文件本身可能也不存在——确认是否要先建空文件。
- **被监听文件是符号链接**：在 watcher 里同时监听链接路径**和**目标真实路径，避免某些写入方式不触发其中一种。
- **被监听文件是 binary**：照样工作（git 存 blob），但 diff 看不出内容。
- **同 Label/服务已存在**：先 unload/disable 旧的再 load 新的。
- **节流期内多次写入**：节流窗口内的多次变更合并为单次 commit（这是想要的）。
- **原子写（write-temp + rename）**：launchd WatchPaths 通常能正确触发；如个别程序的写法导致漏 commit，提示用户改用 KeepAlive + gitwatch / fswatch 主循环。

---

## 模板文件

- [`templates/auto-commit.sh`](templates/auto-commit.sh) —— 自动 commit 脚本骨架
- [`templates/gitignore-whitelist`](templates/gitignore-whitelist) —— 白名单 .gitignore 模板
- [`templates/launchagent.plist`](templates/launchagent.plist) —— macOS LaunchAgent
- [`templates/systemd.path`](templates/systemd.path) + [`templates/systemd.service`](templates/systemd.service) —— Linux systemd path unit

---

## 设计哲学

1. **可见 + 可读 + 可手改**：版本史是文本 git，任何懂 git 的人都能定位/回滚，不依赖任何 GUI。
2. **事件驱动 ≫ 轮询**：减少 idle CPU/磁盘消耗。
3. **失败安全**：commit 脚本无副作用——cd 失败、diff 为空都静默退出，不会破坏 worktree。
4. **目录自包含**：`<BACKUP_ROOT>` 里同时含数据 + 脚本 + plist/unit 模板 + README，整目录拷走能在新机器复活。
5. **不 push**：避免把私密配置上传到任何远程；想异地备份用文件级方案（Time Machine / Backblaze / 加密 syncthing）。
