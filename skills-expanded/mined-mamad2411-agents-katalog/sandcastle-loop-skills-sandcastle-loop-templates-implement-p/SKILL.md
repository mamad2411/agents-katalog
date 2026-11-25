# 本轮任务

实现 issue **#{{TASK_ID}}**: {{ISSUE_TITLE}}

- **BRANCH**: `{{BRANCH}}`
- **WORKTREE_PATH**: `{{WORKTREE_PATH}}`

## 第一步：cwd 守卫（防越界）

```bash
cd "{{WORKTREE_PATH}}"
pwd
git branch --show-current        # 必须 = {{BRANCH}}，⛔ 不能是 main
git rev-parse --show-toplevel    # 必须 = {{WORKTREE_PATH}}
```

⛔ branch = main → `gh issue comment {{TASK_ID}} --body "sandcastle-implementer: cwd 守卫失败"` + 直接结束（**不**输出 COMPLETE）。

## 第二步：测试 / typecheck 命令（调用方已注入，不要自己探测）

- **test**：`{{TEST_CMD}}`
- **typecheck**：`{{TYPECHECK_CMD}}`
  - ⚠️ 若上面 typecheck 一栏为空 → 本项目无 typecheck，**跳过所有 typecheck 步骤**；test 仍必跑
- ⛔ 不准自己改用 `test:integration` / `e2e` / `smoke` 类命令（多数项目这类需 binary 下载 / 环境隔离，不入红绿循环）

## 第三步：拉 issue + Agent Brief

```bash
gh issue view {{TASK_ID}} --comments
```

**优先**读 `## Agent Brief` 评论：
- **Acceptance criteria** — 完工判定（你要逐条 ✅/⏭️/❌）
- **Key interfaces** — 改哪些文件
- **Out of scope** — ⛔ 绝不准越界

## 第四步：项目硬约束

读 cwd 下 `CLAUDE.md` + `CONTEXT.md`。fallback：

{{PROJECT_RULES}}

## 第四步 b：项目 override（sandcastle-loop 行为补丁，如本仓有的话）

{{PROJECT_OVERRIDES}}

## 第五步：执行（按 system prompt 流程）

RGR → typecheck + test → Conventional Commits + docs 联动 → AC self-check 评论 → `<promise>COMPLETE</promise>`

关键 reminder：
- ⚠️ 如项目 `CLAUDE.md` 规定 feat/fix 触发文档联动（changelog / lessons / ADR 等），按项目规则做
- ⚠️ COMPLETE 前**必须** `gh issue comment {{TASK_ID}}` 留 `## AC self-check` 评论
- ⚠️ RED 测试连续 2 次修复仍失败 → 留 issue comment 说明 + 直接结束（不输出 COMPLETE）

## 完工后

- ✅ commits 留在 `{{BRANCH}}` 上
- ✅ AC self-check 评论已留
- ⛔ **不准** `gh issue close` / `git checkout main` / `git merge` / `git push`
