---
name: gith-fork-push-rewr-wrkr
description: Recover when forking/pushing to GitHub fails because global git url.insteadof rewrite rules corrupt remotes into malformed https://github.com:OWNER/REPO.git URLs. Use a fresh gh-cloned fork and re-apply changes.
---

# GitHub fork/push rewrite workaround

用于此类场景：
- 已 fork，但 `git push` / `git fetch` 仍失败
- 报错含 `URL rejected: Port number was not a decimal number between 0 and 65535`
- `git remote -v` 出现畸形地址，如 `https://github.com:OWNER/REPO.git`
- 本地 repo 经历过 remote rename / add 后，仍被全局 rewrite 污染

## 先验判断

先查：

```bash
git remote -v
git config --global --get-regexp '^(credential|http|url)\.' || true
git config --local --get-regexp '^remote\..*\.url$' || true
```

若看到类似规则，基本命中：

```bash
url.git@github.com:.insteadof https://github.com/
url.https://github.com/.insteadof ssh://git@github.com/
url.https://.insteadof git@
```

## 核心策略

不要在污染 repo 上硬修 remote。直接走干净副本，最快。

## 步骤

1. fork 目标仓库：

```bash
gh repo fork OWNER/REPO --clone=false
```

2. 用 `gh repo clone` 单独克隆你名下 fork 到临时目录：

```bash
gh repo clone YOURUSER/REPO /tmp/REPO-clean
```

3. 确认远端正确：

```bash
git -C /tmp/REPO-clean remote -v
```

理想状态：
- `origin` 指向你名下 fork
- `upstream` 指向原仓库

4. 将已改文件从旧工作副本复制到新副本，或重新应用 patch。

5. 在干净副本提交并推送：

```bash
git -C /tmp/REPO-clean checkout -b feat/my-change
git -C /tmp/REPO-clean add .
git -C /tmp/REPO-clean commit -m "feat: ..."
git -C /tmp/REPO-clean push -u origin feat/my-change
```

6. 建 PR：

```bash
gh pr create --repo YOURUSER/REPO --base main --head YOURUSER:feat/my-change
```

## 何时用此法优于修配置

优先用此法，当：
- 用户当前目标是“先把 commit / PR 发出去”
- 机器上 git 全局规则复杂，不宜当场拆雷
- 原 repo 已改 remote 多次，状态不可信

## 何时再修环境

仅当用户明确要求“顺手修 git 环境”时，再处理全局 `url.*.insteadof` 规则。默认先完成 repo 任务。

## 结果验证

至少验证三项：
- `git remote -v` 正常
- `git push` 成功
- PR URL 已产出
