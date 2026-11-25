---
name: finishing-a-development-branch
description: 所有任务完成、所有测试通过后使用。验证测试 → 提供合并/PR/保留/丢弃四个选项 → 执行选择。触发词：完成了、做完了、合并、提交PR、收尾、finish、merge。
agent_created: true
---

# 完成开发分支

## 步骤 1：验证测试

运行项目测试套件。测试失败 → 停止，不能继续。

```bash
# Python
pytest -q

# Node/TS
pnpm test
```

如果失败，必须先用 `systematic-debugging` 修复。

## 步骤 2：确定基准分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
git branch --show-current
```

## 步骤 3：呈现四个选项

```
实现完成。你想怎么做？

1. 合并回 <基准分支>（本地）
2. 推送并创建 Pull Request
3. 保留分支现状（我稍后处理）
4. 丢弃这些工作

选哪个？
```

## 步骤 4：执行选择

### 选项 1：本地合并

```bash
git checkout <基准分支>
git pull
git merge <特性分支>
# 运行测试
git branch -d <特性分支>
```

### 选项 2：推送 + PR

```bash
git push -u origin <特性分支>
gh pr create --title "<标题>" --body "## 概要
- <要点1>
- <要点2>

## 测试计划
- [ ] <验证步骤>"
```

### 选项 3：保留现状

报告："保留分支 `<名称>`。稍后可以继续。"

### 选项 4：丢弃

**先确认：**
```
这将永久删除:
- 分支 <名称>
- 自 <基准分支> 以来的所有提交

输入"discard"确认。
```

等待精确输入 "discard" 后再执行：
```bash
git checkout <基准分支>
git branch -D <特性分支>
```

## 常见错误

- 提供选项前不验证测试 → 总是先验证
- 合并不拉取最新基准 → 总是先 `git pull`
- PR 未合并就删分支 → 等待合并确认
