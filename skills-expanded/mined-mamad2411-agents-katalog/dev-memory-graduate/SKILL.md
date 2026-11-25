---
name: dev-memory-graduate
description: 归档分支记忆：提炼跨分支知识到 repo 共享层，然后归档分支目录。触发词："归档"、"分支收尾"、"需求做完了"、"merge 完了清一下"。
---

# Dev Memory Graduate

把已完成分支的开发记忆做"毕业"处理：

1. **提炼上提**：从分支记忆里挑出跨分支可复用的知识（剥离业务名词），写到 repo 共享层
2. **归档**：把 branch 目录搬到 `branches/_archived/<branch>__<date>/`，append `INDEX.md`

这是显式用户动作，不要 implicit 触发 —— destructive move 需要用户授权。

**Announce at start:** 用一句简短的话说明将先 dump 当前 branch+repo 内容（优先看 pending-promotion），再让用户确认上提哪些条目。

## DO / DON'T

**Do:**

- 用户明确说"归档"、"分支收尾"、"需求做完了"、"merge 完了清一下"、"这个分支可以归档了"、"把分支知识沉淀一下"
- 用户刚合完 PR 到 main 并明确要清理分支记忆

**Don't:**

- **永远不要 implicit 触发**。destructive 操作必须显式确认
- no-git 模式（无分支概念）
- 当前分支还在开发中，用户只是顺口提到"以后要归档"

## v2 改造：优先扫 pending-promotion

v1 graduate 要全量审核 branch 目录里所有 markdown。v2 里 capture 在写入时已经用 `is_cross_branch_candidate()` 自动打标 `pending-promotion.md`，graduate 的 dry-run 会：

- **primary_sources**（主审核面）：`pending-promotion.md` + `decisions.md`
- **cross_check_sources**（漏网之鱼检查）：progress / risks / glossary / overview

通常只看 primary_sources 就够。cross_check_sources 用来补抓 capture heuristic 漏判的跨分支经验。

## Workflow

### Step 1: Pre-flight check

```bash
npx dev-memory-cli graduate dry-run \
  [--repo <repo-path>] [--branch <branch-name>]
```

输出：
- `git_status.ahead`：当前分支领先 default_base 的 commit 数。如果 >0，用户多半还没 merge — 提示确认
- `git_status.uncommitted`：true 表示工作区还有未提交改动，提示先 commit/stash
- `primary_sources.pending-promotion.md`：capture 自动标记的跨分支候选（主审核）
- `primary_sources.decisions.md`：稳定决策，通常也值得提升
- `cross_check_sources.*`：其他文件，只做漏网检查
- `archive_destination`：分支目录会搬到哪

### Step 2: 生成 harvest.json

```json
{
  "repo_overview": [
    {"section": "长期目标与边界", "body": "...", "mode": "append"}
  ],
  "repo_decisions": [
    {"section": "跨分支通用决策", "body": "...", "mode": "append"}
  ],
  "repo_glossary": [
    {"section": "长期有效背景", "body": "...", "mode": "append"},
    {"section": "共享入口", "body": "...", "mode": "append"}
  ],
  "notes": "从 xxx 分支提炼",
  "archive": true
}
```

**提炼原则：**
- 剥离业务名词（分支专用实体改成通用表述）
- 保留 Why 和影响范围
- pending-promotion 里的原条目是**候选**，不是必选 — 审核时该丢就丢
- mode 默认 append（避免覆盖已有 shared 条目）

### Step 3: apply

```bash
npx dev-memory-cli graduate apply \
  --harvest-file /tmp/graduate-harvest.json \
  [--repo <repo-path>] [--branch <branch-name>]
```

执行后：
- harvest 条目 append 到 repo_overview / repo_decisions / repo_glossary
- 在 branch_dir 生成 `archive_summary.md`（含 harvest notes + 归档时元数据 + git log）
- 如 `archive: true`（默认），分支目录搬到 `branches/_archived/<branch>__<date>/`
- `_archived/INDEX.md` 追加一行索引

并发语义：`apply` 会先做 harvest/schema/branch pre-flight；pre-flight 失败会立即返回。pre-flight 通过后，真正写 repo 共享层和归档 branch 的阶段按 repo memory 目录串行排队，后发会话会等待前一个 `apply` 释放队列锁后再继续。

### Step 4: 查索引

```bash
npx dev-memory-cli graduate index
```

列出所有已归档分支。

## Always / Never

**Always:**

- dry-run 优先看 primary_sources.pending-promotion
- 上提时剥离业务名词
- 上提 decisions 时保留 Why

**Never:**

- 不经过 dry-run 直接 apply
- apply 后不看 archive_summary 就关会话
- 在当前分支还未 merge 时强行归档（除非用户明确要求）

## Triggering note

skill-creator description optimizer（3 iterations × 24 queries × 3 runs each）在 2026-04-22 跑过一次。原因是 graduate 的核心动作（mv 目录、写文件、调脚本）在 Claude 看来"自己直接能做"，所以即使 description 命中了关键词，Claude 仍然倾向不调 skill 而直接动手——这是 Claude Code 触发策略对操作型 skill 的结构性偏好，不是 description 写法的问题。

实践建议：当用户希望确保走完整 graduate 流程（harvest 上提 + dry-run + 归档 + INDEX 登记）而不是裸 mv 时，**显式输入 `/dev-memory-graduate`** 作为 slash command，绕过 implicit 触发判定。
