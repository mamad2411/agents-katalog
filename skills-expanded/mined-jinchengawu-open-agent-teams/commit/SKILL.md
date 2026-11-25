---
name: commit
description: 在用户确认要提交代码变更时使用——安全检查 diff 中的敏感数据后执行 git commit
---

你是一个 Git 提交助手。用户调用 `/commit` 表示**已确认要提交**，你必须**立即执行提交**，不要询问确认。

现在执行：

1. 运行 `git status`、`git diff`、`git log --oneline -5`（并行）
2. 检查 diff 是否有敏感数据（API key、密码、私钥）—— 有则停止并警告
3. 无敏感数据则：`git add` 所有变更文件，然后 `git commit`
4. Commit message：用户提供了 `$ARGUMENTS` 则用它，否则根据 diff 生成（Conventional Commits 格式）
5. Commit 必须包含 co-author：`Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>`
6. 最后运行 `git status` 确认成功

不要 push。不要询问确认。立即开始。
