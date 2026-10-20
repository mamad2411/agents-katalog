---
description: |
triggers:
  - 提 PR
  - 创建 PR
  - 请求评审
  - 合并 PR
  - 关闭 PR
  - 发起合并
  - gh pr
  - pull request
  - new pr
  - create pr
role: devops
priority: high
category: ci
stack: _common
alwaysApply: false
---


# GitHub PR 工作流

> 用 `gh` CLI 完成 PR 全流程。**MUST 命令行操作（留痕），禁止 Web 界面**。

## 前置条件（MUST 全部满足）

1. **本地 CI 通过**：编译 + 测试 + lint
2. **评审通过**：`review.md` 存在，无未解决 MUST fix
3. **分支正确**：当前分支为 `feat-*` / `fix-*` / `hotfix-*`
4. **已推远程**：`git push -u origin feat-<name>`

## 执行步骤

### 第 1 步：与 develop 同步

```bash
git fetch origin
git rebase origin/develop  # 或 git merge origin/develop
# 解决冲突（如有）
git push origin feat-<name>
```

### 第 2 步：创建 PR

```bash
gh pr create \
  --base develop \
  --title "feat(user): 新增用户登录接口" \
  --body "$(cat <<'EOF'
## 变更说明
<一句话说明>

## 变更类型
- [x] feat 新功能

## 关联
- Proposal: changes/proposals/<id>/
- Issue: #<number>

## 测试
- [x] 单元测试通过
- [x] 集成测试通过

## Checklist
- [x] 代码符合规范
- [x] 测试覆盖率 ≥ 80%
- [x] 文档已更新
- [x] CHANGELOG 已更新
EOF
)"
```

**MUST 用户确认标题和描述后再执行**。

### 第 3 步：请求评审

```bash
# 请求特定人评审
gh pr request-review <number> @reviewer

# 查看评审状态
gh pr view <number> --json reviews
```

### 第 4 步：处理评审意见

如果有 MUST fix 意见：
1. 调用 `review-fix-loop` 技能
2. 修复后推送
3. 请求复评

```bash
# 修复后推送
git add .
git commit -m "fix: 处理评审意见 - xxx"
git push

# 请求复评
gh pr request-review <number> @reviewer
```

### 第 5 步：检查 CI 状态

```bash
gh pr checks <number>

# 预期：全部通过
# 失败：修复后重试
```

### 第 6 步：合并 PR

**前置条件**（MUST 全部满足）：
- ✅ CI 全部通过
- ✅ 至少 1 人评审通过
- ✅ 无未解决 MUST fix

**合并方式选择**：

| 方式 | 命令 | 适用 |
|---|---|---|
| **Squash** ⭐ | `gh pr merge --squash` | 默认推荐，多 commit 压缩为 1 个 |
| **Merge** | `gh pr merge --merge` | 需保留完整历史 |
| **Rebase** | `gh pr merge --rebase` | 保持线性历史 |

```bash
# MUST 用户确认合并方式后执行
gh pr merge <number> --squash

# 合并后删除远程分支
git push origin --delete feat-<name>

# 切回 develop 并拉最新
git checkout develop
git pull
```

## 产出物

- 创建的 PR
- 评审通过
- 合并后的 develop / master
- 清理的远程分支

## 完成标准

- PR 创建成功（含完整描述）
- 评审通过
- CI 通过
- 合并成功
- 远程分支已删除

## 关联

- 前置：`ci-gate` + `expert-review`
- 中途：`review-fix-loop`（如有 MUST fix）
- 后续：`archive-change`（归档变更）
- Wiki：`wiki/_common/github-workflow.md`
