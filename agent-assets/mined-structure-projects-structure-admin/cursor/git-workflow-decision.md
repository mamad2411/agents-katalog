---
description: |
triggers:
  - 开始新任务
  - 创建分支
  - 新建功能
  - 拉分支
  - 切分支
  - 新需求
  - 开始开发
  - new branch
  - create branch
role: devops
priority: high
category: git
stack: _common
alwaysApply: false
---


# Git 工作流决策

> 按团队规模 + 任务时长选择正确的 Git 流程。**禁止默认推送 feat 分支到远程**。

## 前置条件

- 用户要开始一个新任务

## 执行步骤

### 第 1 步：询问用户场景（MUST）

```
请确认任务场景：

Q1: 这个任务是多人协作还是单人独立？
    a) 单人独立
    b) 多人协作

Q2: 预期完成时间？
    a) 短线（< 3 天，无需远程备份）
    b) 长线（≥ 3 天，或需要远程备份）

请回答 Q1 和 Q2，例如"a + a"表示单人短线。
```

### 第 2 步：按回答选择流程

| Q1 + Q2 | 流程 | 分支策略 |
|---|---|---|
| **单人 + 短线** | 单人短线流程 | 本地 `feat-*`，不推远程，完成后合并到 develop 推送 |
| **单人 + 长线** | 单人长线流程 | 本地 `feat-*`，**推远程**（备份），完成后 PR 合并 |
| **多人 + 任意** | 多人协作流程 | 远程 `feat-*`，**必须 PR 评审**，合并后删远程 |

### 第 3 步：执行对应流程

#### 单人短线

```bash
git checkout develop && git pull
git checkout -b feat-<name>
# 编码 + 提交（本地）
# 完成后：
git checkout develop
git merge --no-ff feat-<name>
git push origin develop
git branch -d feat-<name>
```

**关键约束**：
- ❌ MUST NOT 推送 feat 到远程
- ✅ MUST 合并到 develop 后推送 develop

#### 单人长线

```bash
git checkout develop && git pull
git checkout -b feat-<name>
git push -u origin feat-<name>  # 备份
# 编码 + 提交 + 定期推送
# 完成后：
gh pr create --base develop --title "..."
# CI 通过后：
gh pr merge --squash
git push origin --delete feat-<name>
```

#### 多人协作

```bash
git checkout develop && git pull
git checkout -b feat-<name>
git push -u origin feat-<name>
# 每日推送 + 与 develop 同步
# 完成后：
gh pr create --base develop --title "..." --body "..."
gh pr request-review @<reviewer>  # MUST 评审
# 评审通过后：
gh pr merge --squash
git push origin --delete feat-<name>
```

**关键约束**：
- ✅ MUST 推送远程
- ✅ MUST PR 评审
- ❌ MUST NOT 直接推 develop / master

### 第 4 步：输出明确指引

告诉用户：
- 创建了哪个分支
- 是否推送了远程
- 完成后应该怎么合并
- 需要评审吗

## 产出物

- 正确的分支策略
- 已创建的分支
- 明确的后续指引

## 完成标准

- 分支策略与场景匹配
- 用户明确后续步骤
- 分支已创建并（按需）推送

## 关联

- Wiki：`wiki/_common/git-workflow.md`
- 后续：`coding` / `gh-pr-workflow`
- 规则：`common-git`
