---
name: trellis-push
description: "Commit + push across configured repos with optional merge-to-target and pre-push PRD-sync reminder."
---
# Push — 提交并推送（可选合并到目标分支）

一键完成 commit → push → 可选 merge 到目标分支（通常是测试线）→ push 目标分支 → 切回。

支持多仓库（frontend / backend），merge 目标分支记录在 `.trellis/config.yaml` 的 `packages.<name>.merge_target` 中。

---

## 配置

目标分支存储在 `.trellis/config.yaml` 的 packages 配置中：

```yaml
packages:
  frontend:
    path: iqs-front-human
    git: true
    merge_target: test      # 首次 push 时询问后自动写入
  backend:
    path: iqs
    git: true
    merge_target: test
```

> 首次运行时如果 `merge_target` 不存在，会在 merge 步骤询问目标分支并回写到 `config.yaml`。
> 如需修改，直接编辑 `config.yaml` 或通过 `/trellis-push` 传入 `--reconfigure` 语义。

---

## 执行步骤

### Step 0: 读取配置

读取 `.trellis/config.yaml` 中的 `packages` 配置，识别所有 `git: true` 的仓库及其 `merge_target`（如果已配置）。

### Step 1: 检测变更

读取 `.trellis/config.yaml` 中的 `packages` 配置，对每个 git 仓库检测变更：

```bash
# 对每个 package
cd <package_path>
git status --short
```

列出有变更的仓库。如果所有仓库都没有变更，提示用户并终止。

如果只有部分仓库有变更，只处理有变更的仓库。

**收集所有变更文件列表** —— 用于 Step 1.5 的 PRD 同步判断：

```bash
# 聚合每个仓库的变更文件（相对于仓库根的路径）+ 仓库名前缀
# 例如：["iqs-front-human/src/pages/inquiry/...", "iqs/src/main/java/..."]
```

### Step 1.5: PRD 同步检查（智能判断）`[AI]`

在进入 Step 2 逐仓库 commit 前，先判断本次变更是否需要先同步 PRD。

#### 判断条件

1. **有激活任务**：仓库根下 `.trellis/.current-task` 文件存在，内容是任务目录相对路径
2. **任务有 PRD**：`<current_task>/prd.md` 存在
3. **变更命中任务相关文件**（relatedFiles 交集）：
   - 读取 `<current_task>/task.json` 的 `relatedFiles` 字段（数组，条目可能是文件或目录）
   - 计算 Step 1 收集的变更文件清单与 `relatedFiles` 的交集（前缀匹配即算命中：变更文件路径以某个 `relatedFiles` 条目开头）
   - `relatedFiles` 未配置或为空 → 跳过交集判断，**只要条件 1+2 成立就提示**

#### 处理分支

**不满足条件 1 或 2**（无激活任务 / 无 prd.md）：静默跳过，直接进入 Step 2。

**满足条件 1+2+3**（交集非空 / 无 relatedFiles 配置）：展示提示，等待用户选择：

```markdown
⚠️ 检测到当前任务 `<task-slug>` 下存在 prd.md。
本次变更 <N>/<M> 个文件命中 task.relatedFiles：
  - <命中文件 1>
  - <命中文件 2>
  - ...

本次变更可能涉及 PRD 范围，建议先确认 PRD 是否与实际实现一致：

1. 先同步 PRD —— 暂停 push，调用 trellis-sync-prd
2. PRD 已同步 —— 继续 push
3. 与 PRD 无关（小改动 / hotfix）—— 跳过同步
```

- 用户选 **1** → 立即停止本次 push 流程，调用 trellis-sync-prd skill；完成后提示用户重新运行 `/trellis-push`
- 用户选 **2 或 3** → 继续进入 Step 2

> **[!] 这一步只是提示，不阻塞流程** —— 如果用户确认"与 PRD 无关"，立刻继续；不要反复确认。

### Step 2: 逐仓库处理

对每个有变更的仓库，依次执行以下操作：

#### 2.1 展示变更摘要

```bash
cd <package_path>
git diff --stat
git diff --name-only
```

#### 2.2 暂存文件

展示要暂存的文件列表，**获得用户确认后**再暂存。

```bash
git add <具体文件列表>
```

> **[!] 禁止使用 `git add -A` 或 `git add .`**
> 必须明确列出文件，避免误提交敏感文件（.env、credentials 等）。

#### 2.3 生成 commit message 并提交

分析变更内容，生成符合项目风格的 commit message：
- 读取最近 5 条 commit 参考风格
- 类型前缀：`feat` / `fix` / `chore` / `refactor` 等
- 简短描述变更内容
- 使用中文描述

```bash
git commit -m "<type>(<scope>): <description>"
```

#### 2.4 Push 当前分支

```bash
git push origin <current_branch>
```

如果远程没有该分支，使用 `-u` 建立跟踪：

```bash
git push -u origin <current_branch>
```

#### 2.5 询问是否 Merge 到目标分支（可选）

Push 完成后，检查该 package 是否已配置 `merge_target`：

**已配置 `merge_target`**：

```markdown
<package> 已推送到 <current_branch>。是否合并到 <merge_target>？

1. 是，合并到 <merge_target>
2. 否，跳过
```

**未配置 `merge_target`（首次）**：

```markdown
<package> 已推送到 <current_branch>。是否需要合并到其他分支（如测试线）？

1. 是，请输入目标分支名
2. 否，跳过
```

如果用户输入了目标分支名，**将其回写到 `.trellis/config.yaml`** 对应 package 的 `merge_target` 字段，下次自动使用。

**如果用户选择合并**：

```bash
# 切换到目标分支并拉取最新
git checkout <target_branch>
git pull origin <target_branch>

# 合并当前开发分支
git merge <current_branch> --no-edit

# Push 目标分支
git push origin <target_branch>

# 切回开发分支
git checkout <current_branch>
```

> **[!] 如果 merge 出现冲突：**
> 1. 立即停止，展示冲突文件列表
> 2. 询问用户：手动解决 / 中止 merge
> 3. **绝对不能** `git merge --abort` 后静默跳过

**如果用户选择跳过**：直接进入下一个仓库或输出结果。

### Step 3: 输出结果

```markdown
## Push 结果

| 仓库 | 分支 | 目标 | commit | 状态 |
|------|------|------|--------|------|
| frontend | v1.3 | test | abc1234 feat(...): ... | ✅ 已合并 |
| backend | v1.3 | test | def5678 fix(...): ... | ⏭️ 跳过合并 |

所有变更已推送到目标分支。
```

---

## 语义参数（通过自然语 / skill args 传入）

| 语义 | 说明 | 用户怎么说 |
|------|------|-----------|
| 默认 | 自动检测所有有变更的仓库并处理 | `/trellis-push` |
| 指定仓库 | 只处理指定仓库 | 「只 push 前端」/「push frontend」 |
| 重新配置 | 重新询问目标分支 | 「重新配置 push 目标分支」/「reconfigure push」 |
| 临时目标 | 临时指定目标分支（不修改配置） | 「push 到 hotfix 分支」 |
| 跳过 PRD 检查 | 明确本次与 PRD 无关 | 「这次 hotfix 不用检查 PRD」 |

---

## 安全机制

1. **暂存确认** — 每个仓库暂存前展示文件列表，用户确认
2. **commit message 确认** — 展示生成的 message，用户可修改
3. **merge 冲突处理** — 冲突时暂停，不静默跳过
4. **不碰主分支** — 如果目标分支是 `master` / `main`，额外警告确认
5. **不使用 force push** — 始终使用普通 push
6. **PRD 同步提示** — Step 1.5 智能检测任务相关变更，提示先同步 PRD

---

## 反模式（避免）

- ❌ `git add -A`（可能误提交敏感文件）
- ❌ merge 冲突后静默 abort（用户需要知道）
- ❌ 未经确认直接 commit（必须让用户看到 message）
- ❌ force push 到目标分支
- ❌ 在目标分支上直接开发（只 merge，不在目标分支上改代码）
- ❌ 跳过 Step 1.5 PRD 同步检查（即使只是提示，也是给用户一次"想起来"的机会）
- ❌ Step 1.5 提示后反复追问（用户明确 "跳过" 就继续，不要第二次确认）
