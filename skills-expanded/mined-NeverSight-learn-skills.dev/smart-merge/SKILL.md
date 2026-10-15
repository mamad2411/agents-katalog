---
name: smart-merge
description: Intelligent branch merge assistant that automatically detects logical conflicts between branches, auto-resolves safe text conflicts, and guides the user through logical conflicts interactively. Trigger this skill when the user says "merge", "合并分支", "smart merge", "把 X 合并到 Y", "merge X into Y", or any variation of merging branches. Also trigger when the user mentions resolving merge conflicts intelligently or wants help with a branch merge that might have issues.
---

# Smart Merge

Intelligent branch merge tool that goes beyond Git's text-level conflict detection. It analyzes semantic and logical compatibility between branches, auto-resolves safe conflicts conservatively, and surfaces logical conflicts for human decision-making.

**All user-facing output MUST be in Chinese.** The operator interacts in Chinese. Never output English text to the user except for code, file paths, branch names, and git commands.

## When to Use

- User wants to merge one branch into another
- User says `/smart-merge`, "合并分支", "merge X into Y"
- User is dealing with merge conflicts and wants intelligent resolution

## Workflow

### Phase 1: Preparation

Parse the user's input to determine:
- **Source branch**: The branch whose changes are being merged in (defaults to current branch if merging into a target)
- **Target branch**: The branch receiving the changes

If the user says `/smart-merge main`, interpret as: merge `main` into the current branch.
If the user says `/smart-merge feat/foo into main`, interpret as: merge `feat/foo` into `main`.
If ambiguous, ask the user to clarify (in Chinese).

Run these commands in parallel to gather context:

```bash
# Current branch
git branch --show-current

# Merge base (common ancestor)
git merge-base <target> <source>

# Commits coming in from source (relative to merge base)
git log <merge-base>..<source> --oneline

# Commits on target since divergence
git log <merge-base>..<target> --oneline

# File-level change summary from source
git diff <merge-base>..<source> --stat

# File-level change summary from target
git diff <merge-base>..<target> --stat

# Check for potential conflicts without actually merging
git merge-tree $(git merge-base <target> <source>) <target> <source>
```

Present a brief summary to the user:

```
正在分析分支合并情况...

源分支: <source> (<N> 个提交)
目标分支: <target> (<M> 个提交)
分叉点: <merge-base-short-hash>

源分支变更: <X> 个文件
目标分支变更: <Y> 个文件
重叠文件: <Z> 个
```

### Phase 2: Logical Conflict Detection

This is the core analysis phase. Before performing the actual merge, analyze the changes from both branches for semantic incompatibilities.

#### What to Analyze

For each file modified in both branches (overlapping files), and for symbols that are deleted/renamed in one branch but referenced in the other:

**1. Deleted or Renamed Symbols**
- Functions, methods, types, structs, interfaces deleted in one branch
- Check if the other branch adds new references to those symbols (imports, calls, type usage)
- Variables or constants removed in one branch, used in the other

**2. Function Signature Changes**
- Parameters added, removed, or reordered
- Return type changes
- Check if callers in the other branch use the old signature

**3. API Contract Changes**
- Proto/API definition changes in one branch
- Service layer or handler changes in the other branch that assume old API shape
- Request/response field changes where the other branch reads/writes old fields

**4. Type and Interface Changes**
- Struct field additions/removals/renames
- Interface method changes
- Check if the other branch implements or uses the old shape

**5. Dependency and Import Changes**
- Package imports changed in one branch
- The other branch adds new usages of the old import path
- Go module dependency version conflicts

**6. Configuration and Schema Conflicts**
- Database schema changes (Ent schemas, migrations) in both branches
- Configuration file changes that could be semantically incompatible
- Wire/DI provider changes that affect dependency graph

#### How to Detect

1. Get the detailed diff from both branches relative to the merge base:
   ```bash
   git diff <merge-base>..<source> -- <overlapping-files>
   git diff <merge-base>..<target> -- <overlapping-files>
   ```

2. For deleted symbols, search the other branch's diff for new references:
   ```bash
   # If source deletes function Foo, check if target adds calls to Foo
   git diff <merge-base>..<target> | grep '+.*Foo'
   ```

3. Read the actual files on both branches when deeper analysis is needed:
   ```bash
   git show <source>:<file-path>
   git show <target>:<file-path>
   ```

4. For Go projects, leverage the project structure:
   - Check `internal/biz/` for interface changes → verify `internal/data/` implementations
   - Check `api/` proto changes → verify `internal/service/` handlers
   - Check `internal/data/ent/schema/` → verify dependent code

#### Classification

Categorize each finding as:

- **LOGICAL_CONFLICT**: Semantic incompatibility that cannot be auto-resolved. Both sides made changes that are structurally incompatible. Merging them as-is would produce broken code.
- **TEXT_CONFLICT_SAFE**: Git-level conflict where one side's change is clearly an addition or the intent is unambiguous. Can be auto-resolved.
- **TEXT_CONFLICT_AMBIGUOUS**: Git-level conflict where both sides meaningfully changed the same region with different intent. Needs human decision.
- **NO_CONFLICT**: Clean merge, no action needed.

### Phase 3: Report and Decision

#### Case A: No Conflicts at All

If no text conflicts and no logical conflicts are found:

```
分析完成！未发现任何冲突。

源分支 <source> 的变更可以干净地合并到 <target>。
正在执行合并...
```

Proceed directly to Phase 4 (auto-merge and commit).

#### Case B: Only Safe Text Conflicts (No Logical Conflicts)

If there are text conflicts but all are classified as TEXT_CONFLICT_SAFE:

```
发现 <N> 个文本冲突，均可安全自动解决：

  1. <file-path> — <brief description of conflict and resolution>
  2. <file-path> — <brief description>

未发现逻辑冲突。正在自动解决并提交...
```

Proceed to Phase 4 with auto-resolution.

#### Case C: Logical Conflicts or Ambiguous Text Conflicts Found

Present each logical conflict clearly with options. Use the AskUserQuestion tool to let the user decide.

For each conflict, present:

```
发现逻辑冲突，需要你来决定如何处理：

冲突 1/N: <file-path>
类型: <conflict type in Chinese>
说明: <clear Chinese description of what happened>

  源分支 (<source>): <what this branch did>
  目标分支 (<target>): <what this branch did>
  风险: <what would break if merged naively>
```

Then offer options via AskUserQuestion (options depend on the specific conflict type):

Typical options:
- **保留源分支版本** — Use the source branch's changes, discard target's conflicting changes
- **保留目标分支版本** — Keep the target branch's changes, discard source's conflicting changes
- **手动编辑** — Open the file for manual editing (mark the conflict and let the user resolve it)
- **合并两者** — Attempt to integrate both changes (only offer when semantically possible)

For ambiguous text conflicts, show the actual diff hunks so the user can make an informed choice.

Process all conflicts sequentially. Collect all decisions before proceeding to Phase 4.

### Phase 4: Execute Merge

Based on the analysis results and user decisions:

#### Step 1: Ensure clean working tree

```bash
git status --porcelain
```

If there are uncommitted changes, warn the user and suggest stashing:

```
当前工作区有未提交的变更。建议先暂存：
  git stash
合并完成后可以恢复：
  git stash pop
```

Wait for the user to confirm before proceeding.

#### Step 2: Perform the merge

```bash
git checkout <target>   # Switch to target branch if not already on it
git merge <source> --no-commit   # Merge without auto-commit to allow resolution
```

#### Step 3: Resolve conflicts

For TEXT_CONFLICT_SAFE conflicts and user-decided conflicts:
- Use the Edit tool to apply the chosen resolution to each conflicted file
- After editing, stage the resolved file: `git add <file>`

For "手动编辑" decisions:
- Leave the conflict markers in place
- Tell the user which files need manual editing
- Wait for the user to confirm they've finished editing
- Then stage: `git add <file>`

#### Step 4: Verify resolution

```bash
# Check no conflict markers remain
git diff --check

# Verify the merge result compiles (for Go projects)
go build ./...
```

If build fails, report the errors to the user and help fix them before committing.

#### Step 5: Commit

```bash
git commit -m "<merge commit message>"
```

The commit message should follow the format:
```
merge: 合并 <source> 到 <target>

<Chinese summary of what was merged and any conflicts resolved>
```

Report the result:

```
合并完成！

提交: <commit-hash>
合并: <source> → <target>
解决冲突: <N> 个文件
自动解决: <M> 个
手动处理: <K> 个

请检查合并结果，确认无误后可以推送到远程。
```

**Do NOT push to remote unless the user explicitly asks.**

## Safety Rules

1. **Never force-push or use destructive git operations.** If something goes wrong, abort the merge with `git merge --abort` and explain the situation.

2. **Always use `--no-commit` for the initial merge** so we have a chance to verify the result before committing.

3. **If the merge would result in data loss**, warn the user explicitly before proceeding.

4. **If the build fails after merge resolution**, do not commit. Help the user fix the build first.

5. **Back out cleanly on failure.** If anything goes wrong mid-merge, run `git merge --abort` and report what happened.

6. **Respect the user's decisions.** When they choose an option for a conflict, apply exactly that. Don't second-guess or override.

## Edge Cases

**Fast-forward merge**: If the target branch is a direct ancestor of the source, report it and ask if the user wants a fast-forward or a merge commit:
```
目标分支 <target> 可以快进合并到 <source>。
```

**Large merge (>50 files conflicting)**: Warn the user and suggest reviewing in smaller batches. Still proceed if they confirm.

**Binary file conflicts**: Cannot auto-resolve. Always present to the user for decision.

**Submodule conflicts**: Flag explicitly and ask the user which version to keep.

**Merge already in progress**: If `git status` shows a merge in progress, ask the user if they want to continue resolving or abort.

## Example Interaction

User: `/smart-merge main`

```
正在分析分支合并情况...

源分支: main (5 个提交)
目标分支: feat/user-auth (当前分支, 3 个提交)
分叉点: abc1234

源分支变更: 12 个文件
目标分支变更: 8 个文件
重叠文件: 3 个

正在检测逻辑冲突...

发现 1 个逻辑冲突和 2 个可自动解决的文本冲突：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

逻辑冲突 1/1: internal/biz/user/usecase.go
类型: 函数签名变更
说明: main 分支修改了 CreateUser 的参数（新增 orgID 参数），
     但当前分支新增了 3 处对旧签名的调用。

  main 分支: CreateUser(ctx, dto) → CreateUser(ctx, orgID, dto)
  当前分支: 新增调用 CreateUser(ctx, dto) 于第 45, 78, 112 行
  风险: 合并后编译失败，调用参数不匹配

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

可自动解决的文本冲突:
  1. go.mod — 依赖版本不同，取较新版本
  2. internal/server/http.go — 双方各自新增路由，无重叠

请选择如何处理逻辑冲突：
```

Then uses AskUserQuestion to present options for the logical conflict.
