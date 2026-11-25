---
name: git-repo-recovery
description: git仓库本地状态损坏时用:残留锁、unborn分支、批量误删的恢复。
metadata:
  imported_from: hermes
---

# Git Local Repo Recovery

Trigger: git 本地仓库状态损坏——提交时报 lock 写入错误、`git log` 报
"does not have any commits yet"、commit 里出现大量意外 delete、push 报
"src refspec <branch> does not match any"。目标：**用远程分支作锚点恢复本地，
不丢工作区未提交改动，绝不 force push 污染远程**。

## 症状链（2026-08-11 实测，resume 仓库）

一次瞬时 I/O 错误可连锁引发全部症状：

1. `git commit` 报 `fatal: sha1 file '<repo>/.git/index.lock' write error:
   Operation timed out` —— 瞬时的 APFS/磁盘写入超时，**不是**锁被占用。
   git 在崩溃中留下 `.git/refs/heads/main.lock` 残留（注意：refs 锁与
   index.lock 是两个位置）。
2. 之后 `git log` / `git reflog` 报 `your current branch 'main' does not
   have any commits yet`；`git status` 显示 "No commits yet" + 一堆
   `new file:` / `??` —— 分支变成 unborn，HEAD 无法移动。
3. 残留锁导致 `git reset` 无效：即使 `git reset --mixed origin/main`，
   HEAD 仍不移动（reset 更新 ref 时被 main.lock 挡住，只更新了 index）。
4. 最危险的一步：在 unborn 状态下 commit，git 把"index 相对空 HEAD 的
   差异"整包提交——**仓库里几乎所有已跟踪文件显示为 delete mode**，
   且只新增你刚 add 的那一个文件。push 报 `error: src refspec main does
   not match any`（本地无该 ref）——**这个失败是保护**：坏 commit 没上远程，
   远程 `origin/main` 仍是完整锚点。

## 诊断（先看再动）

```bash
git status && git log --oneline -3          # unborn? log 报 fatal?
git branch -avv                             # 远程 ref 是否完好
ls -la .git/refs/heads/                     # 找 *.lock 残留
cat .git/HEAD                               # 确认指向 refs/heads/main
git fsck --lost-found 2>&1 | head           # dangling commit 是孤儿对象，可忽略
```

关键判断：**远程 ref（`refs/remotes/origin/<branch>`）完好 + 工作区文件
物理存在**（表现为 `??` 未跟踪）→ 可无损恢复。

## 修复

```bash
# 0. 确认没有 git 进程在跑（pgrep git），锁不是被活进程持有
# 1. 删残留锁
rm -f .git/refs/heads/main.lock .git/index.lock
# 2. HEAD + index 回到远程，工作区不动（未提交改动全部保留）
git reset --mixed refs/remotes/origin/main
# 3. 验证：git log 恢复历史；git status 只剩真实改动（M）
# 4. 重新 add 具体文件 + commit + push（只 add 明确路径）
git add <changed-file>
git commit -m "fix: ..."
git push origin main
```

要点：
- **`git reset --mixed <remote-ref>` 不动工作区**——本地未提交改动（如刚
  编辑的源文件）保留为 `M`，这是无损恢复的关键，不要用 `--hard`。
- 恢复后 `git status --short` 应只剩预期改动；若 commit 里出现大量
  `delete mode` 或 `A`（new file），立即停止——index 状态仍异常。
- 远程锚点版本就是真相：本地 refs 全坏了没关系，`origin/main` 在就能救。

## 并发分支切换吞掉 staged 改动（2026-08-13 实测，CUpedia）

症状：并行 subagent 在 `git add` 之后、`git commit` 之前 checkout 了别的分支，
commit 只包含部分文件（如只有新增测试文件），实现代码改动在工作区消失
（`git status` 干净、`grep` 特征符号为 0）。reflog 能看到
`checkout: moving from <你的分支> to <别的分支>` 夹在 commit 前后。

恢复（改动可能在 dangling commit 里）：

```bash
git reflog -10                    # 确认 checkout/commit 时序
git fsck --lost-found 2>&1 | grep 'dangling commit'   # 找快照
# 逐个看消息：git log -1 --format="%H %s" <sha> —— 并行 agent 的
# "wip: staged for branch split" / "wip+arrival-states" 类提交常是完整快照
git show --name-only --format="" <dangling-sha>       # 确认含你要的文件
git show <dangling-sha>:<path> | grep -c "<特征符号>"  # 验证版本对不对
git checkout <dangling-sha> -- <file1> <file2> ...     # 只恢复需要的文件
```

要点：
- **并行 agent 的 staged 快照 commit（消息含 "wip" / "staged for branch
  split"）是完整工作区快照**——即使它随后拆成了多个分支 commit，dangling
  对象仍保留合并前的全部内容，是最可靠的找回源。
- 恢复后若历史出现两个同标题 commit（一个只有测试、一个只有实现），用
  `git reset --soft <父提交>` 合并成单个干净 commit 再提交，别留拆碎的记录。
- 恢复文件时用 `git checkout <sha> -- <路径>`（覆盖工作区），不要
  cherry-pick 整个 dangling commit（会带上并行 agent 的无关改动）。
- **防御**：与并行 agent 同仓工作时，`git add` 后立刻 `git commit`
  （一条命令串起来，不给 checkout 插缝）；或先确认没有别的进程在切分支。
  发现工作区"该在的改动没了"先查 reflog + fsck，别直接重写。

## 防御

- **push 失败 = 保护信号**：`src refspec does not match any` /
  `failed to push some refs` 出现时先查本地分支状态，别急着 force。
- 提交前扫一眼 staged 范围：`git diff --cached --stat` 若出现与本次改动
  无关的大量文件变更，说明 index/HEAD 已损坏。
- 常规操作遵守：`git add <具体路径>`（禁 `add .`/`-A`）、commit 后立即
  push、push 成功后再做下一步。
- git 仓库目录出现 `.DS_Store` 会触发 `fsck` 的 `badRefName` 噪音
  （`refs/.DS_Store`），无害但可清理。
