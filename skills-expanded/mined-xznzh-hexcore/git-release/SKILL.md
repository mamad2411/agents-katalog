---
name: Git Release
description: 开版本分支、提交前自检、合并回 main 并打 tag。涉及开分支/提交/合并/发版/打 tag/热修时使用。
---

# Git Release

按仓库规范执行分支与发布流程，**不要凭记忆改流程**。动手前先读 `docs/04-规范/Git分支与发布规范.md`，
命令细节以 `scripts/release.mjs` 为准。

## 铁律（违反即停止并向用户说明）

1. 永远不在 `main` / `master` 上提交、推送、`git commit --amend` 或 `git reset`。
2. 不执行 `git push --force`，不改写已推送的历史，不移动已有 tag。
3. 合并、打 tag、推送、删除远端分支，必须先得到用户明确同意；没有同意只做到「自检通过」为止。
4. **只有 `.release-owner` 里的维护者能合并 `main`、打 tag、推 tag。** `pnpm release:status` 显示「维护者：不是」时，
   立即停止，不要运行 `release:finish` / `release:tag`，改为「推分支 + 开 MR」。
5. 不把 `.env.local`、`data/`、`.next/`、日志、临时脚本加入提交。
6. 不夹带与本轮迭代无关的改动；工作区有别人的未提交内容时停下询问。

## 判断当前该做什么

| 用户诉求 | 动作 |
|---|---|
| 开始新一轮迭代 / 改一批功能 | 走「开分支」 |
| 改完要提交 | 走「提交」 |
| 自测 / 验收 | 走「自检」 |
| 验收通过要发布 | 走「发布」（先征求同意） |
| 线上紧急 bug | 走「热修」 |
| 只是问状态 | 跑 `pnpm release:status`，不要改任何东西 |

## 开分支

```bash
pnpm release:status                  # 确认当前分支与工作区
pnpm hooks:install                   # 若 core.hooksPath 为空，每个 clone 一次
pnpm release:start 1.1.0             # 版本号由用户确认，禁止自行编造
```

- 已在 `release/vX.Y.Z` 且版本一致 → 不要重复开分支。
- 用户没说版本号 → 问；参考上一版 tag 再给建议。
- `release:start` 会自动改 `package.json` 的 version，不要手动再改一遍。

## 提交

```bash
git add <明确的文件>                 # 不用 git add -A，除非用户要求且已确认无脏文件
git commit -m 'fix(rag): 中文问句两轮召回'
```

- 提交信息：`<type>(<scope>): <描述>`，type 见规范 §3；中文描述可以。
- 钩子会自动跑 `tsc --noEmit`（改到 `app/`、`components/` 时加跑界面规范）；失败先修，不要 `--no-verify`。
- 一个提交只做一件事；顺手重构与功能混在一起时提醒用户拆分。

## 自检

```bash
pnpm release:check
```

- 四项全绿才算过：typecheck、界面规范、单测、文档链接。
- 改了登录 / 对话 / 知识库 / 发布主流程 → 追加 `pnpm e2e`。
- 改了 `docs/` → 同步 `docs/README.md` 索引。
- 失败时只修根因，不删测试、不放宽断言、不注释掉检查项。

## 多人协作（非维护者）

`pnpm release:status` 显示「维护者：不是」，或用户明确不是仓库管理员时：

```bash
git fetch origin
git switch -c feature/<主题> origin/release/v1.2.0   # 从当前 release 切，不从 main 切
# 开发、提交、pnpm release:check
git push -u origin feature/<主题>
# 网页开 MR：feature/<主题> → release/v1.2.0
```

- 不合并 MR、不推 `main`、不打 tag、不改 `package.json` 的 version。
- 不要对着 `main` 开 MR；由维护者把整条 release 合入 main。
- 权限矩阵、保护分支配置、审查清单见规范 §11。

## 发布（需用户明确同意）

先确认仓库是否已开保护分支：

```bash
pnpm release:notes                   # 先把发布说明给用户看
```

**未开保护分支**（本地合并）：

```bash
pnpm release:finish 1.1.0            # 默认交互确认；不要自动加 --yes
```

**已开保护分支 / 走 MR**（推荐）：

```bash
git push -u origin release/v1.1.0    # 推分支
# 在 GitHub 网页开 PR 合入 main，等合并完成
git switch main && git pull --ff-only
pnpm release:tag 1.1.0 --push        # 只打 tag，不推送 main
```

- 不要在开了保护分支后跑 `finish --push`：远端会拒绝直接推 main，脚本会停在推送这一步。
- `release:finish` / `release:tag` 会校验 `.release-owner`；邮箱不匹配时停止，不要用 `--as-maintainer` 绕过他人限制。
- tag 只由维护者创建并推送；非维护者连推 tag 都会被 `pre-push` 拦。
- 用户说「发版 / 合并 / 打 tag / 推上去」都算同意；只说「继续」不算。
- 用户要求推送才加 `--push`；网络或权限失败时把恢复命令原样给用户，不要强推。
- 合并后确认：`git tag --list "v1.1.*"`、`git log --oneline -3`、release 分支已删除。
- 在 MR 描述里贴：本轮目标、门禁结果、影响面、回滚方式（`git revert <merge-sha>`）。

## 热修

```bash
git switch --detach v1.1.0
git switch -c hotfix/v1.1.1
# 只改 bug + 补一条回归用例
pnpm release:check
```

合入 main 的步骤同「发布」，版本号递增 PATCH；修完提醒用户把修复同步回仍在开发的 release 分支。

## 结束后回报

用 3–6 行说明：当前分支、版本号、门禁结果、是否已推送、下一步命令。不要贴大段 git 输出。
