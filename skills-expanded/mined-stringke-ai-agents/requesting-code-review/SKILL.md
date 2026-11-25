---
name: requesting-code-review
description: 派遣 code-reviewer 子代理对当前改动进行全面代码审查。触发短语："代码审查"、"review"、"审查代码"。
allowed-tools: Read, Glob, Grep, Bash, Agent
---

# /requesting-code-review — 请求代码审查

派遣一个 code-reviewer 子代理对当前的代码变更进行全面审查。

## 流程

### 第一步：收集变更信息

```bash
# 查看当前分支的所有变更
git diff main...HEAD --stat
git diff main...HEAD
git log main..HEAD --oneline
```

如果没有远程分支对比，使用暂存区和工作区的 diff：

```bash
git diff --stat
git diff
git diff --cached --stat
git diff --cached
```

### 第二步：收集上下文

如果存在 plan.md 或 spec.md，读取它们作为审查上下文。

### 第三步：派遣审查子代理

使用 Agent 工具派遣子代理，prompt 结构：

1. 引用 `references/code-reviewer-prompt.md` 的完整内容
2. 附加变更的 diff 信息
3. 附加 plan.md/spec.md 内容（如有）
4. 指定审查范围

### 第四步：呈现结果

将审查结果完整呈现给用户，按严重度排序：
1. 关键问题（CRITICAL）
2. 重要问题（IMPORTANT）
3. 建议（SUGGESTION）

## 何时使用

- 完成一轮实现后，合并前
- 完成 plan.md 中一个阶段的任务后
- 用户想要第二意见时
