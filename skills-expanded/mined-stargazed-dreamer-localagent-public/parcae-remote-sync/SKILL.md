---
name: parcae-remote-sync
description: Parcae 主仓库与 origin/master 分叉时，安全完成"和远端合并"的完整流程。两种场景：① 落后且工作区脏（有 WIP，含 CHANGELOG.md）→ 备份/stash/快进/pop/消解冲突；② 领先且工作区干净（改动已提交）→ merge/消解 CHANGELOG 冲突/提交 merge。两种场景都要判"远端那笔是否发版"来决定冲突消解规则，并全程保持 CHANGELOG 的 CRLF。当用户说"和远端合并一下 / 同步一下远端 / pull 一下"时使用。
agent_created: true
task_type: dev.parcae_remote_sync
---

# Parcae 与远端同步（CHANGELOG 冲突 + 分叉合并）

## 适用场景

用户说「和远端合并一下 / 同步一次」之类。先 `git fetch origin` 看 `git rev-list --left-right --count origin/master...master`（左=远端独有，右=本地独有），分两种场景：

**场景 A — 本地落后、工作区脏**（`左>0 右=0`，且有未提交改动含 `CHANGELOG.md`）
走下面「操作步骤（场景 A）」的 stash 流程。

**场景 B — 本地领先、工作区干净**（`右>0`，`git status` 无未提交）
本地已提交的活儿与远端新提交**分叉**，`--ff-only` 不适用（必然失败）。
不要 stash（没东西可 stash），直接 `git merge origin/master` → 消解冲突 → **提交 merge**。
实测（2026-09-19：本地 ahead 6 / 远端 1 笔，29 个改动文件里只有 `CHANGELOG.md` 重叠）。

## 核心认知（决定成败的两点）

1. **`CHANGELOG.md` 是冲突高发点，且消解规则取决于"远端那笔是否发版"——先判这一点，别默认撞的是发版。**

   **情形 1（发版）**：远端提交把 `[Unreleased]` 整段「上抬」为 `## [x.y.z] - 日期`，旧版本段挪进 `docs/changelog-archive.md`。
   本地未提交的 `[Unreleased]` 补记几乎必然与远端发版提交**撞在同一锚点**（都插在 `### Fixed` 首行）。
   消解规则：**远端条目留在新版本段；本地未提交的条目上移到 `[Unreleased]` 下新建对应小节**（判据 = 内容日期 vs 发版日期）。

   **情形 2（未发版，实测 2026-09-19）**：远端只是往 `[Unreleased] ### Added` 顶部追加了 1 条普通条目。
   判据：`git show origin/master:CHANGELOG.md | head -8` 里 `## [Unreleased]` **仍在**、无新 `## [x.y.z]` 段。
   此时**不存在"上移"问题**——两侧条目都属未发布内容，正确消解 = **两者并存**：
   把远端条目置于该段首（最新在前），本地条目紧随其后。**不要**因为看到冲突就去抬版或建新版本段。

   两情形的共同点：冲突块内两侧内容都要保留（冲突从来不是二选一），差别只在"要不要把本地条目挪进 `[Unreleased]`"。

2. **`CHANGELOG.md` 磁盘上是纯 CRLF**（`core.autocrlf=true`，实测 65 CRLF / 65 LF）。
   用 Python 改它**必须**：`open(p,'rb')` → `decode('utf-8')` → `split('\r\n')` → `'\r\n'.join(...)` → `encode` → `open(p,'wb').write(...)`。
   **绝不能**用默认 `open(p,'w')`——会把整个文件重写行尾，制造假的全文件 diff。

## 操作步骤（场景 A：本地落后 + 脏工作区）

前置：所有 git 命令必须用用户自装 Git（`export PATH="/e/System_Programes/Git/cmd:$PATH"`）。

```bash
export PATH="/e/System_Programes/Git/cmd:$PATH"
cd /f/<project_root>

# 0) 摸清状况
git fetch origin
git rev-list --left-right --count origin/master...master   # 右为 0 才可 ff
git remote -v   # 确认是 Stargazed-Dreamer/localAgent（还有嵌套仓 workspace/model_data，别混）

# 1) 找出远端改动 ∩ 本地改动 —— 交集就是冲突面
#    ⚠ 必须用三点 diff（master...origin/master）！两点 diff（master..origin/master）算的是
#    "两棵树之间的差异"，会把本地独有提交的改动**反向**算进来，交集瞬间变成"几乎全部文件"。
#    2026-09-19 实测踩过：两点 diff 报出 29 个重叠文件，三点 diff 后真实重叠只有 CHANGELOG.md。
git diff --name-only master...origin/master | sort > /tmp/r.txt      # 远端独有改动
#    场景 A 用工作区；场景 B 用本地独有提交
git status --porcelain | awk '{print $2}' | sort > /tmp/l.txt        # 场景 A：未提交改动
# git diff --name-only origin/master...master | sort > /tmp/l.txt    # 场景 B：已提交改动
comm -12 /tmp/r.txt /tmp/l.txt

# 2) 备份（文件副本 + stash 双保险），记录 stash 哈希
mkdir -p temp/git_merge_backup_$(date +%Y%m%d)
cp CHANGELOG.md temp/git_merge_backup_$(date +%Y%m%d)/CHANGELOG.md.local
git stash push -m "wip before merge $(date +%F)"
git rev-parse "stash@{0}"

# 3) 快进合并（本地领先 0 时 --ff-only 最干净，不产生无谓 merge commit）
git merge --ff-only origin/master

# 4) 恢复本地改动 → 预期仅 CHANGELOG.md 冲突
git stash pop
```

5. 消解 `CHANGELOG.md` 冲突：用 `temp/fix_changelog_conflict.py` 这类脚本（按上面 CRLF 规则）——
   冲突区只保留上游条目，把本地那条上移到 `[Unreleased]` 下新建的 `### Fixed`。

6. 硬验证（**不要只看文件长得对**）：
```bash
git diff --numstat origin/master -- CHANGELOG.md        # 应恰等于本地新增的行数（如 3 增 0 删）
git diff --numstat "stash@{0}" -- <本地其他改动路径>     # 应为空 → 证明 pop 没丢内容
```
   再跑一下与被保留 WIP 相关的测试（如 `workspace/gh_mirror/tests/...`）确认改动 + 合并后代码能共存。

7. 收尾：标记解决 + **把索引还原成未暂存**（保持与合并前一致，不擅自替用户暂存/提交/推送）：
```bash
git add CHANGELOG.md
git ls-files -u | wc -l      # 必须是 0
git reset -q
git status --short --branch  # ## master...origin/master（无 ahead/behind）
```

## 操作步骤（场景 B：本地领先 + 工作区干净）

改动都已提交，本地与远端**分叉**（`右>0`）——`--ff-only` 必然失败，也不需要 stash。
2026-09-19 实测（本地 ahead 6、远端 1 笔）：

```bash
export PATH="/e/System_Programes/Git/cmd:$PATH"
cd /f/<project_root>

# 1) 摸清 + 记下载要，便于事后核对
git fetch origin
git rev-list --left-right --count origin/master...master     # 如 1  6（左远端/右本地）
git show --name-only --format='' origin/master | sort > /tmp/r.txt   # 远端那笔的真实改动
git diff --name-only origin/master...master | sort > /tmp/l.txt      # 本地那批的真实改动
comm -12 /tmp/r.txt /tmp/l.txt                                # 真实重叠面（本次只有 CHANGELOG.md）

# 2) 先备份（哪怕工作区干净，CHANGELOG 是必冲突文件，留个副本零成本）
mkdir -p temp/git_merge_backup_$(date +%Y%m%d)
cp CHANGELOG.md temp/git_merge_backup_$(date +%Y%m%d)/CHANGELOG.md.local

# 3) 合并（本次用 merge，仓库历史里本就有 merge commit；不需 --ff-only）
git merge origin/master        # 预期：仅 CHANGELOG.md CONFLICT
```

4. **先判"远端那笔是否发版"再消解**（见「核心认知 1」两情形）：
```bash
git show origin/master:CHANGELOG.md | head -8 | tr -d '\r'
```
   `## [Unreleased]` 仍在 + 无新 `## [x.y.z]` → **情形 2**：两侧条目并存，远端条目置段首。
   脚本按 CRLF 字节级写：`read_bytes → split('\r\n') → join → write_bytes`；
   取冲突块时把远端侧的尾部空行留在段末，别挤进两条条目之间。

5. 硬验证（两个方向都要量）：
```bash
git diff --numstat <合并前本地HEAD> -- CHANGELOG.md   # 应恰=远端新增行数（如 1 增 0 删）
git diff --numstat origin/master -- CHANGELOG.md      # 应全为插入、0 删（证明本地条目一条没丢）
git diff origin/master -- CHANGELOG.md | grep '^-[^-]'   # 空 = 零删除
```
   再扫无冲突标记、CRLF 纯正（`裸LF=0`）、无 U+FFFD。

6. 提交 merge 并跑机械防线（两侧改动共存验证）：
```bash
git add CHANGELOG.md
git ls-files -u | wc -l        # 必须是 0
git commit -F - <<'EOF'        # 正文写清：冲突面 / 判定依据（是否发版）/ 两个 numstat / 防线结果
…merge message…
EOF
```
   防线 = 本地那侧的测试 + 远端新增测试 + `tests/server_endpoints/test_smoke_endpoints.py` + `uv run pyright`。

7. **不 push**（除非用户明确说"推"）。收尾报告写清 ahead 几笔，并提示用户可 push。

## 若用户接着说「提交掉」

1. 按路径显式 `git add`（不用 `-A`），扫一遍 `git diff --cached` 有无 `keys.json` / token 字面量。
2. 跑机械防线：`uv run pyright <改动文件显式路径>`（workspace 脚本不在 `pyrightconfig.json` 的 `include` 里）+ `uv run python -m pytest tests/server_endpoints/test_smoke_endpoints.py -q`。
   ⚠️ **必须用 `uv run pyright`**，`.venv/Scripts/python.exe -m pyright` 会因缺 `truststore` 报假阳性。
3. **`uv.lock` 漂移（钩子已阻断，但仍要复查）**：`scripts/hooks/pre-commit` 跑 `uv run`，而本机全局 uv 配置 `index-url` 是阿里云镜像、仓库 uv.lock 记的是官方 pypi 源 → uv 判定 lock 过期并整文件重写（3109+/3109-），撤销远端 `f7ab2a2`；`docs/release-policy.md` L13 又明文 uv.lock 会进分发包，不该把地区镜像固化进去。
   **2026-09-10 起钩子已改为 `exec env UV_FROZEN=1 uv run ...`，正常 `git commit` 不再弄脏 uv.lock**（实测：钩子输出与退出码不变、lock 保持干净）。但用户手动 `uv run` / `uv sync` 仍会漂——提交前照旧 `git status` 瞄一眼，漂了就 `git restore uv.lock`（生成物，还原零风险）。
   `--locked` / `UV_LOCKED=1` 在本机**不可用**（全局索引≠lock 源，uv 判 lock 需更新，直接报错）；要冻结只能 `UV_FROZEN=1`（它不校验 lock 与 pyproject 的一致性，本场景只做静态检查，影响可忽略）。
4. 提交信息用项目风格 `type(scope): 中文摘要` + 正文（`git commit -F -` + heredoc）。pre-commit 会跑 `check_hard_rules`（C1 BOM / C2 密钥 / C3 路径 / C4 import）。
5. 提交后**不 push**（除非用户明确要求）；`git rev-list --left-right --count origin/master...master` 应显示本地领先 N。

## 边界与注意

- **不要自行 commit / push**。项目规范默认不发版不 push；本地 WIP 保持未提交，由用户决定何时提交。
- ⛔ **shell 脚本必须保持 LF**：本机 `core.autocrlf=true`（来自**系统级** `<data_drive>:/<apps_root>/Git/etc/gitconfig`），靠仓库 `.gitattributes` 兜底（2026-09-10 新增：`scripts/hooks/* text eol=lf` + `*.sh text eol=lf`）。改 `scripts/hooks/*` 后**不要**让编辑器写成 CRLF——`#!/bin/sh\r` 与末行 `--staged\r` 会让钩子直接失效。复核用 `git ls-files --eol <path>`（应为 `w/lf`）；`git add` 时若冒出「LF will be replaced by CRLF」警告，说明该路径还没被 `.gitattributes` 覆盖。
- **两类文件行尾要求相反**：`CHANGELOG.md` 要 CRLF，`scripts/hooks/*` 与 `*.sh` 要 LF，别搞反。
- `UV_FROZEN=1 uv run ...` 可完全避免 uv.lock 漂移（已实测）。
- stash 条目 pop 冲突后会**保留**——留着当后备，在最终回复里告诉用户 `git stash drop` 何时可用。
- `workspace/model_data` 是**独立嵌套仓库**（非 submodule、无 `.gitmodules`），主仓合并不影响它；它 `git fetch` 偶发 502，重试即可。
- 修改 `workspace/gh_mirror/loop_actions.py` 后需**重启后端**才生效（`importlib.import_module` 启动时加载一次）；`repos.json` 每次重读、无需重启。
