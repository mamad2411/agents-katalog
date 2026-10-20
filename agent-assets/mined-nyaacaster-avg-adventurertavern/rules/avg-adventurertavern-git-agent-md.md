---
globs: "**/*"
regex: 提交|推送|commit|push|git push|提交代码|上传代码|同步代码
description: 当用户要求提交、推送、commit、push、git push、提交代码、上传代码、同步代码时，执行提交前检查与推送流程。
alwaysApply: false
---

在执行任何 Git 提交/推送前，先运行 `npx tsc --noEmit`，若失败则停止并反馈错误；通过后依次执行 `git status`、`git diff --name-only`、`git diff --cached --name-only` 检查工作区与差异，确认或获取 commit message（建议 `[类型] 简短描述`），再执行 `git add`、`git commit -m`、`git push`（新分支用 `git push -u origin <branch>`），最后反馈结果并在失败时提示 pull/冲突/网络权限排查，同时注意敏感信息与 .gitignore。