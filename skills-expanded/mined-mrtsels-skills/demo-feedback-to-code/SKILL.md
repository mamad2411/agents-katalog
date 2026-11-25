---
name: demo-feedback-to-code
title: 演示反馈 → 代码修改
description: 从演示反馈文档提取修改意见，逐条确认后批量派发 Claude Code 修改
---

## 场景

甲方/用户通过微信发送 .docx 文件（视频修改建议、演示反馈等），需要提取文字、逐条确认、批量修改代码。

## 步骤

### 1. 提取文本
用 `read_file` 读取 .docx 文件（自动提取文字）。

### 2. 逐条确认
用 `clarify` 工具逐条向用户确认每条修改意见的含义：
- 每条给 2 个选项：「是，理解正确」「不是，我解释一下」
- 用户选「不是」时，再问「那你解释一下」
- 用户在选项中选择后，再继续下一条
- 不要一次性列所有条目——用户明确要求逐条问

### 3. 批量修改

#### 3.1 设置 Kanban
用 `todo` 工具创建任务列表，每个独立修改为一个 task。

#### 3.2 按改动分组
把修改按影响范围分组（政府端/企业端/协会端、文本替换/逻辑修改/功能删除等）。

#### 3.3 创建独立分支+worktree
```bash
git push origin main:refs/heads/feat/<name>
git worktree add /tmp/wt-<name> feat/<name>
```

#### 3.4 并行派发子代理
用 `delegate_task` 并行派发子代理（最多 3 个并行），每个子代理：
- cd worktree
- 用 claude 修改代码
- node --check 验证语法
- git add/commit/push

#### 3.5 合并
```bash
git merge --squash feat/<name>
git commit
```

### 4. 验证
- node --check 所有 script 块
- 确认改动前后端都可访问
- 清理 worktree + 远程分支

### 5. 成本
所有 Claude Code 调用使用 `--model sonnet`（指向 deepseek-v4-flash），不要用 pro 模型。

## 注意事项
- 每个独立改动用单独分支+worktree，避免 index.html 冲突
- 改完后必须 node --check（提取 <script> 块逐段检查）
- 文字替换（"查看详情"→"详情"等）可以不用子代理，直接 sed/patch
- 用户对 UI 文字偏好：短字优先（如「详情」而非「查看详情」）
