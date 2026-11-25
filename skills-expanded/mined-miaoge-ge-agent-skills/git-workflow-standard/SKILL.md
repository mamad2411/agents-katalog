---
name: git-workflow-standard
description: "按统一规范执行 Git 操作：Conventional Commits 提交信息、分支命名、提交粒度、变基与合并、标签发布和历史安全。用于编写或审查提交信息、创建分支、整理历史、发起评审、准备发布，或排查误提交与强制推送风险时。"
metadata:
  version: "1.0.1"
---

# Git 工作流规范

以 Conventional Commits 为核心，覆盖从分支创建到发布打标签的完整流程。需要改写历史、强制推送、删除分支时，先读[安全与恢复](references/safety.md)并取得明确确认。

## 执行流程

1. 读取仓库现状：`git status --short --branch`、`git log --oneline -10`、`git remote -v`，并查找 `CONTRIBUTING.md`、`.gitmessage`、`.commitlintrc*`、`lefthook.yml` 等既有约定。仓库已有规则优先于本技能默认值。
2. 判断场景，只做该场景需要的事：提交、建分支、同步、整理历史、评审、合并或发布。不顺手混合无关操作。
3. 规划原子提交：一个提交只表达一个逻辑变更，能独立说明“改了什么、为什么”。重构与行为变更、格式化与功能修改分开。
4. 精确暂存：用显式路径或 `git add -p`；提交前用 `git diff --cached` 自查，确认没有密钥、构建产物、无关文件和调试代码。
5. 按[提交信息规范](references/commit-message.md)编写信息，并运行 `scripts/commit_msg_lint.py` 校验。
6. 推送后核对远端状态与 CI。改写历史或强制推送前，先读安全规则并取得确认。

## 提交信息

格式：

```text
<type>(<scope>)!: <description>

<body>

<footer>
```

- `type` 必填、小写，取 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert` 之一。`feat` 对应 MINOR，`fix` 对应 PATCH。
- `scope` 可选、小写，用模块、目录或功能名，不用人名和工单号。
- `description` 紧跟 `: `，动词开头；英文用祈使句小写，中文直接写动作，不加句号，标题总长不超过 72 字符。
- `body` 与标题之间空一行，说明动机、影响和取舍，不重复代码已经表达的内容；每行建议不超过 72 字符。
- `footer` 与正文空一行，使用 `BREAKING CHANGE:`、`Refs:`、`Closes:`、`Co-authored-by:` 等键；破坏性变更推荐同时用 `!` 和 `BREAKING CHANGE:` 标明。
- 不提交 `WIP`、`update`、`fix bug` 这类无信息量的标题；临时提交在合并前用交互式变基整理。

示例：

```text
feat(auth): add device authorization flow

Support headless login on CI by polling the device token endpoint and
backing off on slow_down responses.

Refs: #412
```

```text
feat(api)!: drop the legacy /v1/session endpoint

BREAKING CHANGE: /v1/session is removed; use /v2/auth/session instead.
  Clients pinned to v1 must upgrade before 2026-06-01.
```

类型选择、正反例和页脚细则见[提交信息规范](references/commit-message.md)。

## 分支与历史

- 从最新的默认分支创建短生命周期分支，命名 `<type>/<kebab-case-summary>`，如 `feat/oauth-device-flow`、`fix/123-null-pointer`、`release/v1.4.0`。
- 先 `git fetch --prune`，再用 `git rebase origin/main` 同步；拉取用 `git pull --rebase`，保持线性历史。
- 只在自己尚未共享的功能分支上改写历史。`main`、`develop`、`release/*` 等共享分支禁止变基、禁止强制推送。
- 必须强推时，先审查本地与远端双方独有提交，再用 `--force-with-lease=<ref>:<已审查SHA>` 固定预期远端位置；完整流程见分支与历史参考。不要用 `--force`。
- 已经推送的错误提交用 `git revert` 生成反向提交；只有未推送的本地提交才用 `reset`。
- 合并默认 squash：PR 标题即最终提交信息，保留一个可回滚、可解释的提交；只有发布同步才用 merge commit。

分支命名、同步、冲突处理、合并策略和标签规则见[分支与历史](references/branching-and-history.md)。

## 评审与发布

- PR 标题同样遵循 Conventional Commits；描述写清变更、动机、验证方式、风险与回滚方案，关联 issue（如 `Closes #123`）。
- 提交前自查完整 diff，确认无密钥、调试代码、无关格式化和被注释掉的代码。
- 版本遵循 SemVer：破坏性变更升 MAJOR，`feat` 升 MINOR，`fix` 升 PATCH。
- 在默认分支的发布提交上创建带注释标签：`git tag -a v1.2.0 -m "v1.2.0"`；已发布的标签不移动、不删除。
- 变更日志按类型分组、破坏性变更置顶，从 `git log v1.1.0..v1.2.0` 生成后人工校对。

评审清单、PR 模板和发布步骤见[评审与发布](references/review-and-release.md)。

## 安全红线

- 不提交任何密钥、令牌、私钥、`.env`、证书或含敏感信息的日志；提交前用下方脚本扫描。已经提交的密钥先轮换，再清理历史。
- 不直接向受保护分支推送；不在未知状态下执行 `git reset --hard`、`git clean -fd`、`git push --force`、`git branch -D`。
- 不用 `git add -A` 或 `git add .` 盲目暂存；不在分离 HEAD 上直接提交。
- 不绕过 pre-commit / commit-msg 钩子（`--no-verify`）；钩子报错先修问题或修钩子。
- 破坏性操作前先 `git status`，分别保存未提交内容与提交位置；临时分支不能代替 stash 或文件备份。执行范围必须已有明确授权，不重复索取相同授权。

恢复误操作、清理密钥和危险命令清单见[安全与恢复](references/safety.md)。

## 自动检查

校验脚本只依赖 Python 3 标准库，支持 `--json` 输出机器可读结果。

```bash
# 校验单条提交信息
python scripts/commit_msg_lint.py --message "feat(auth): add login"

# 校验提交信息文件（commit-msg 钩子的用法）
python scripts/commit_msg_lint.py --file .git/COMMIT_EDITMSG

# 校验一段提交区间
python scripts/commit_msg_lint.py --range origin/main..HEAD

# 提交前扫描暂存区：密钥、敏感文件、大文件、冲突标记、空白错误
python scripts/git_guard.py --staged

# 校验分支名
python scripts/git_guard.py --branch feat/oauth-device-flow

# 安装 commit-msg 与 pre-commit 钩子（已存在他人钩子时拒绝覆盖）
python scripts/install_hooks.py
```

`commit_msg_lint.py` 返回 0 表示通过、1 表示有错误、2 表示用法或 IO 错误；默认放行 merge 和 `fixup!` / `squash!` 提交，`--no-merge`、`--no-fixup` 可收紧。`git_guard.py` 返回 1 表示存在阻断项，默认对受保护分支只告警，加 `--protect-main` 变为阻断。钩子安装在 `git rev-parse --git-path hooks` 指向的目录，可用 `install_hooks.py --uninstall` 卸载。

## 验证

修改技能后运行：

```bash
python -m unittest discover -s tests -v
```

在本仓库内修改时，再运行仓库级校验：

```bash
python ../../scripts/validate_skills.py
```

单元与集成测试覆盖提交信息解析、密钥与文件扫描、钩子安装和真实 Git 仓库提交；测试只使用标准库，可在任意平台运行。

## 工具边界与升级

- 文本扫描覆盖大小限制内的完整暂存内容，包括 JSON/YAML 的带引号键名；已超限文件直接阻断，不把截断扫描当作通过。二进制文件不做文本凭据扫描，通用凭据匹配默认告警，`--strict` 可阻断；启发式工具不能证明没有密钥。
- 钩子配套脚本通过哈希清单记录归属。卸载只删除哈希仍匹配的已登记文件，保留额外文件、用户修改、备份和链接；没有清单的旧版本目录保留并报告。
- 旧版本升级或已有同名脚本时先检查差异；确需替换可用 `--force`，脚本会先备份。不要直接删除整个 hooks 或 git-standard 目录。
