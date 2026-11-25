---
name: muicv-git
description: 把简历素材库放到用户自己的 git 仓库（GitHub / GitLab / 自建均可），用 git workflow 多端同步、留版本史、可分享。四个子任务：`init`（首次给素材库加 .git + .gitignore + 远程关联，**会问用户 public/private**）、`sync`（commit 当前改动并 push 到远程）、`clone`（换机器场景，把已有 repo 克隆到工作目录）、`status`（看本地状态）。使用场景：用户说「推到 GitHub」「git push 我的简历」「sync 到 GitLab」「从 GitHub 克隆我的素材」「换机器拉 git」「commit 一下」「git status」「我想用 git 管简历」「用 GitHub 当作品集」等。和 muicv-sync 是平行选项——后者是 muicv 平台 D1 黑盒（可加密）备份，本 skill 是用户掌控的 git workflow，可以同时用。
---

# muicv-git

把简历素材库（profile / experience / projects / 全部 .md）作为一个 git 仓库，托管在用户自己的 GitHub / GitLab / 自建 git server 上。这是 muicv-sync 的「白盒」对照：

| | muicv-sync（muicv 平台） | muicv-git（你自己的 git） |
|---|---|---|
| 后端 | muicv 云端 D1 | 你自己的 GitHub repo（也可以 GitLab / 自建） |
| 鉴权 | mui_ key | git credential / `gh auth` / SSH key |
| 历史 | 自动滚 5 份 | 完整 git log，永久 |
| 大小限制 | 1MB / 500 文件 | 由 git host 决定（GitHub 单文件 100MB / repo 软上限 5GB） |
| 协作 / 分享 | 私人 | 可加协作者、做 private/public repo、PR review |
| 学习曲线 | 0（说一句"同步"） | 要懂 git 基础（add / commit / push / pull） |

两者**不互斥**——同一份素材库可以**既**是 git repo **又**周期性 push 到 muicv 平台备份。

---

## 边界（重要）

- **skill 不替用户隐式 commit**：除非用户明确说「commit」「sync」「推到 GitHub」，否则不动 git。日常编辑素材时不要顺手 add。
- **commit message 必须有意义**：默认让用户给一句，**不**默认填「update」「sync」之类垃圾消息。如果用户说"随便"，就用一句具体描述（如"+1 段 ACME 经历"）。
- **不强推 / 不重写历史**：除非用户明确要求 `--force-with-lease` 之类，普通 push 失败（远程有新提交）就让用户先 `git pull --rebase` 自己合并。

---

## 前置检查

### 1. 工具是否就绪

```bash
git --version           # 必装
gh --version            # 可选；有的话能更省事（自动建 repo + OAuth）
```

`git` 没装：让用户去装（mac: `brew install git`；linux 一般自带；windows: https://git-scm.com）。**不要**自己 brew install。

`gh` 没装：可选，没有也行，下面 init 流程会给浏览器手动建 repo 的备选路径。

### 2. 素材库尺寸软提醒（init 前）

```bash
du -sh <素材库根>
find <素材库根> -type f -not -path '*/.*' -not -path '*/node_modules/*' | wc -l
```

- 总大小 > 50 MB **或** 文件数 > 1000 → 给用户**软提醒**（不阻断）：
  > repo 有点大（`<X> MB / <N>` 文件）。GitHub 单文件 100 MB / repo 软上限 5GB 都够用，但每次 push 会慢一些。
  > 建议把 `versions/*.pdf`（renderer 产物，能现拉现渲）和大照片塞进 `.gitignore`，让 git 只 track 真正源数据。
- 不超阈值就跳过这步。

### 3. 素材库根

prelude 已探查 `**/profile.md`：
- **init / sync / status** 必须有根
- **clone** 没有根也行——会把远程仓克隆下来填充工作目录

### 4. 是不是已经是 git repo

```bash
git -C <素材库根> rev-parse --is-inside-work-tree 2>/dev/null
```

- 输出 `true` → 已经是 git repo，跳过 init，直接 sync/status
- 不是 / 报错 → 走 init 流程

---

## 子任务：init（首次接入 git）

**触发**：用户说「我想用 git 管简历」「初始化 git」「绑到 GitHub」等；或 sync/status 时发现还没 .git。

### 流程

1. **确认意图**：跟用户说一句"我会在素材库根下 `git init`，加一份 .gitignore，然后帮你关联 GitHub（或 GitLab）远程仓。可以吗？"得到肯定再继续。

2. **`git init`**：

   ```bash
   git -C <素材库根> init -b main
   ```

3. **写 .gitignore**（如果还没）：

   ```
   # macOS
   .DS_Store

   # muicv-sync pull 时的本地备份
   .muicv-pull-backup-*/

   # 编辑器临时文件
   *.swp
   *.swo
   .vscode/
   .idea/

   # 渲染产物（按用户偏好可保留；问一次再决定）
   # versions/*.pdf
   ```

   `versions/*.pdf` 默认**不**忽略（PDF 也版本化，方便 review）；如果用户介意 repo 体积，问一次"PDF 要不要纳入版本？"再决定。

4. **问用户：repo 是 public 还是 private**

   不要默认就 private。问一句：
   > repo 用 **private**（推荐，简历是私人内容、有联系方式 / 薪资期望 / 离职原因这些不想公开的细节）还是 **public**（想公开当作品集 / 让 HR 直接搜到）？
   - 默认推荐 private 但接受用户选 public。
   - 如果用户已经在前一句话里明说了（"建个公开 repo"），跳过这一问直接照做。

5. **创建远程仓 + 关联**：

   **路径 A（用 gh，最丝滑）**：
   ```bash
   # 用户选 private
   gh repo create <repo-name> --private --source=<素材库根> --remote=origin --push
   # 或用户选 public
   gh repo create <repo-name> --public  --source=<素材库根> --remote=origin --push
   ```
   - `--source` 指素材库根，`--remote=origin --push` 一键关联并首推

   **路径 B（手动）**：让用户去 https://github.com/new 建一个 repo（**自己选 public 还是 private**；**不要勾**「Initialize with README」），然后：
   ```bash
   cd <素材库根>
   git remote add origin git@github.com:<user>/<repo>.git
   git add .
   git commit -m "init: 初始化简历素材库"
   git push -u origin main
   ```

   GitLab / 自建：把 origin URL 改成对应 host 的 SSH/HTTPS 地址即可。

6. **报告**：远程仓 URL + 是 public 还是 private + "以后跟我说『推到 GitHub』就能继续 sync"。

---

## 子任务：sync（commit + push 当前改动）

**触发**：用户说「推到 GitHub」「sync 到 git」「commit 一下」「git push」等。

### 流程

1. `git -C <根> status --short` 看有没有改动。
   - 没改动 → 告诉用户"工作区干净，不需要 commit"，可选 `git fetch` + 看是不是远程比本地新。
   - 有改动 → 列出改动文件给用户**先看一眼**，确认。

2. 让用户给 commit message。**不要默认填**。给两个建议：
   - 如果改动只涉及新加经历/项目，建议 "+1 段 ACME 经历" 这种具体语
   - 如果改动跨多个文件，建议总结性 "更新 google 简历版本 + 加一段 newco 经历"

3. 执行：
   ```bash
   git -C <根> add .
   git -C <根> commit -m "<用户给的 message>"
   git -C <根> push
   ```

4. push 失败处理：
   - **`rejected (non-fast-forward)`**：远程有新提交（比如另一台机器先 push 了）。**不要 force**——告诉用户：
     ```bash
     git -C <根> pull --rebase
     ```
     rebase 成功 → 重 push；冲突 → 让用户在编辑器解决冲突标记，然后 `git rebase --continue` 再 push。
   - **`Permission denied (publickey)`**：用户没配 SSH 或 token。引导：
     - HTTPS + PAT：让用户在 GitHub Settings → Developer settings → Personal access tokens 生成一个 `repo` scope 的 token，git push 时会要求输入 username + token 当密码（macOS Keychain / git credential helper 会缓存）
     - 或者更简单：用 `gh auth login` 一次配好
     - 或者 SSH key：`ssh-keygen -t ed25519` → 把 `~/.ssh/id_ed25519.pub` 加到 https://github.com/settings/keys

5. 报告：commit hash 短前缀 + 推到的 branch + 远程 URL（让用户能直接打开看）。

---

## 子任务：clone（换机器恢复）

**触发**：用户说「从 GitHub 拉简历」「换机器了，git clone 我的素材」等。

### 流程

1. 问用户 repo URL（或 `<user>/<repo>`）。
2. 确认目标目录：默认当前工作目录；如果当前目录非空且**不是**该 repo，问用户要不要 clone 到子目录或换个目录。
3. 执行：
   ```bash
   gh repo clone <user>/<repo> <target-dir>
   # 或
   git clone git@github.com:<user>/<repo>.git <target-dir>
   ```
4. 进 cloned 目录，跑 `glob_files("**/profile.md")` 验证素材库结构。
5. 告诉用户："素材已恢复在 `<target-dir>`，以后在这个目录里跟我说话，我能看到所有内容。"

---

## 子任务：status（看一眼本地状态）

**触发**：用户问「git 状态」「我有没有 commit 漏掉的」「跟远程同步了吗」。

```bash
git -C <根> fetch
git -C <根> status -sb
git -C <根> log --oneline -5
```

把这三个的输出综合给用户看：
- 有几个未 commit / 未 push 的改动
- 本地 vs 远程领先 / 落后多少 commit
- 最近 5 条提交记录

不主动建议 commit / push——让用户自己决定。

---

## 错误处理小抄

| 现象 | 给用户怎么说 |
|---|---|
| `git` 没装 | macOS：`brew install git`；其他平台见 https://git-scm.com。不要让 skill 自己装 |
| `gh` 没装 | 是可选项，可以走"手动在 GitHub.com 建 repo + git remote add"路径；想丝滑就 `brew install gh`（mac）或参考 https://cli.github.com/ |
| push rejected non-fast-forward | "远程有新 commit（你在另一台机器或网页上改过）。先 `git pull --rebase` 把远程的合到本地，再 push" |
| Permission denied (publickey) | 引导 HTTPS+PAT / `gh auth login` / SSH key 三选一（见 sync 流程） |
| repo 已存在（gh repo create） | 问用户：是要换名字新建，还是直接用现有那个 repo（这种情况 skip create，只 `git remote add` 关联）|
| `fatal: not a git repository` | 还没 init，走 init 流程 |

---

## 与其他 skill 的协作

- `muicv-core` 加经历 / 项目 / 整理素材 → 改完后跟 `muicv-git` 说「推到 GitHub」
- `muicv-sync`（muicv 平台云同步）：和 muicv-git **可以同时用**。muicv-sync 是 1MB 黑盒备份，muicv-git 是白盒版本管理；建议正式以 git 为准，muicv-sync 当二级备份。
- `muicv-render` / `muicv-jobs`：产出的 .pdf / targets/*.md 同样会被 git tracked（除非你在 .gitignore 里排除）

---

## 调用示例

### 例 1：第一次接入

```
用户：我想用 GitHub 管这个素材库
Claude:
  1. git -C ~/cv rev-parse → 不是 git repo
  2. du -sh ~/cv → 12 MB / 80 文件，没超 50 MB / 1000 阈值，不提醒
  3. 走 init 流程，确认意图
  4. git init -b main
  5. 写 .gitignore（默认不排除 PDF；问用户要不要排除 → 不要）
  6. 问用户：repo 是 public 还是 private？→ 用户回 "private"
  7. gh 已装 → gh repo create meathill/my-resume --private --source=. --remote=origin --push
  8. 报告：✓ 已推到 git@github.com:meathill/my-resume.git（private），以后跟我说"推到 GitHub"继续 sync
```

### 例 2：日常 sync

```
用户：今天加了段 newco 的经历，commit 一下
Claude:
  1. git status → 多了 experience/newco-2026.md
  2. 让用户给 message 或问"用『+1 段 newco 经历』可以吗？"
  3. git add . && git commit -m "+1 段 newco 经历" && git push
  4. 报告：✓ a1b2c3d 推到 origin/main（github.com/meathill/my-resume/commit/a1b2c3d）
```

### 例 3：换机器恢复

```
用户：换了 mac，把我的素材从 GitHub 拉回来。repo 是 meathill/my-resume
Claude:
  1. 当前目录空 → 直接 clone 进来
  2. gh repo clone meathill/my-resume .
  3. glob **/profile.md → ✓ 素材库结构完整
  4. 告诉用户：素材已恢复，你现在可以继续用 muicv-core 编辑了
```
