---
name: git-worktree-helper
description: 检查、创建和管理 Git worktree，用于并行分支开发。适用于需要按本地分支模式批量创建 worktree、把 worktree 放到仓库同级目录、避免为已在其他目录检出的分支重复创建 worktree、核对分支与 worktree 路径映射，或在多个分支上修改前先准备隔离工作区的场景。
---

# Git Worktree Helper

用这个 skill 以安全、可重复的方式管理本地 Git worktree。

## 工作流

前置约束：

- 创建 worktree 时，必须由用户明确提供目标分支名或分支匹配模式
- 如果用户没有提供分支名或模式，只能执行现状检查，不能默认对所有本地分支创建 worktree。
- 禁止把“未指定范围”解释为“为所有分支批量创建 worktree”，避免目录数量失控和工作区膨胀。

### 1. 先检查当前状态

- 运行 `git branch --list '<pattern>'` 查看候选本地分支。
- 运行 `git branch -r --list 'origin/<pattern>'` 查看候选远程分支。
- 先用自然语言汇总候选分支，明确区分哪些是本地分支，哪些是远程分支，等待用户确认目标范围。
- 如果用户选择的是远程分支，先在本地创建对应分支，再继续创建 worktree；不要直接基于远程引用跳过本地分支这一步。
- 运行 `git worktree list --porcelain` 建立已有分支到路径的映射。
- 把当前工作区所在分支视为已有 worktree，不要为它重复创建 worktree。
- 如果用户只要求查看映射关系、核对现状或确认哪些分支已检出，到这里即可，不进入创建步骤。

### 2. 选择目标目录布局

- 默认批量布局：在仓库根目录同级创建一个名为 `<repo-name>-worktrees` 的目录。
- 每个 worktree 目录名由分支名推导而来，把 `/` 替换成 `~`。
- 如果用户指定了基础目录，优先使用用户指定值而不是默认值。
- 如果用户已经明确给出目标路径，直接使用该路径，不必再推导默认布局。

目录结构示例：

```bash
/path/to/
├── repo/ # 当前项目路径
└── repo-worktrees/
    ├── skill~git-worktree/ # 对应[技能]开发分支 skill/git-worktree
    └── feature~login/      # 对应[功能]开发分支 feature/login
```

> 默认使用 `~` 替代 `/`，以降低与原分支名中连字符 `-` 混用时的路径碰撞风险。

路径映射示例：

- `skill/git-worktree` -> `repo-worktrees/skill~git-worktree`
- `feature/login` -> `repo-worktrees/feature~login`

创建前检查：

- 批量处理时，先构造完整的 `branch -> target_path` 计划表。
- 在执行前检查目标路径唯一性；如果两个分支映射到同一路径，立刻停止，并明确报出冲突分支对。
- 如果目标路径已经存在，但没有注册为 worktree，立刻停止并把它作为人工冲突暴露出来。

### 3. 创建 worktree

- 批量创建时，先列出命中的本地分支，再逐个推导目标路径，形成明确的创建计划。
- 当范围超过一个分支时，先用自然语言汇总计划，至少说明命中的分支、对应路径、哪些分支会被跳过。
- 确认计划后，再逐个运行 `git worktree add <path> <branch>` 正式执行。
- 如果只缺一个分支，直接使用 `git worktree add <path> <branch>` 即可。

示例：

```bash
git branch --list 'skill/*'
git branch -r --list 'origin/skill/*'
git worktree list --porcelain
git worktree add /path/to/repo-worktrees/skill~git-worktree skill/git-worktree
git worktree add /path/to/repo-worktrees/feature~login feature/login
```

### 4. 验证结果

- 创建完成后运行 `git worktree list --porcelain`，确认新路径已注册。
- 对每个新建的 worktree 运行 `git -C <worktree-path> branch --show-current`，确认检出的分支正确。
- 核对计划与结果是否一致，尤其是 `created`、`skipped`、`failed/conflicted` 三类数量和明细。
- 明确汇报哪些分支因为已有 worktree 被跳过，哪些路径被新建，哪些分支因为冲突未处理。

## 安全规则

- 不要为已经有 worktree 的分支再创建第二个 worktree。
- 除非用户明确要求，否则不要删除、`prune` 或移动 worktree。
- 不要为了管理本地 worktree 而推送远端变更。
- 如果检测到路径映射冲突，或者目标路径已经存在但没有注册为 worktree，立刻停止并把它作为人工冲突暴露出来。

## 执行要求

- 优先使用标准 Git 命令，不依赖额外脚本。
- 批量处理时，先汇总计划，再执行创建，避免一次性盲目落地。
- 无匹配分支：属于正常无操作结果，应明确说明“没有匹配到候选分支，因此未创建 worktree”。
- 已有 worktree：属于正常跳过，应在汇报中列出分支和现有路径。
- 路径映射冲突或目标路径冲突：属于失败，停止执行，等待人工处理。
- 非 Git 仓库、分支不存在、命令执行失败：属于失败，直接停止并暴露错误。
- 汇报结果时明确区分：已存在的 worktree、这次新建的 worktree、因冲突而未处理的分支。
