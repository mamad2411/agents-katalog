---
name: finishing-a-development-branch
description: "完成开发分支——功能开发完成后的收尾流程：测试验证、代码审查、合并、清理与部署归档。适配 Gitee 和 GitHub 双平台。"
version: "4.3.8"
updated: "2026-05-14"
---

# 完成开发分支

## 概述

"代码写完了"≠"分支完成了"。通过结构化选项引导开发工作的收尾：验证→选择→执行→清理。

**核心原则：** 完成的分支 = 测试通过 + 审查通过 + 已合并 + 分支已删除 + 文档已更新。

**开始时宣布：** "正在使用 finishing-a-development-branch 技能完成分支收尾。"

## 步骤 1：验证测试

**在展示选项之前，必须先验证测试通过：**

```bash
npm test  # 或 cargo test / pytest / go test ./...
```

**测试失败 → 停止，不继续。** 显示失败信息，要求先修复。
**测试通过 → 继续步骤 2。**

**🔴 CI 状态检查（项目有 CI 时）**：
若项目配置了 CI（`.github/workflows/` 等），先确认当前分支 CI 通过：
```bash
gh run list --branch $(git branch --show-current) --limit=1 --json status,conclusion
```
CI 失败 → 停止流程，先修复 CI。测试通过 ≠ CI 通过。

## 步骤 2：确定基础分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或确认："这个分支是从 main 分出来的——对吗？"

## 步骤 3：展示收尾选项

```
功能已完成。你想怎么做？

1. 本地合并回 <base-branch>
2. 推送并创建 Pull Request
3. 保持分支现状（我稍后处理）
4. 丢弃这项工作

选哪个？
```

## 步骤 4：执行选择

### 选项 1：本地合并

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
# 重新运行测试
<test command>
# 测试通过 → 删除分支
git branch -d <feature-branch>
```

### 选项 2：推送并创建 PR

> 🔴 推送前确认：CI 已通过（若项目有 CI 配置）。CI 失败时绝不要推送。

**Gitee：**
```bash
git push -u origin <feature-branch>
# 在 Gitee 页面创建 PR，使用下方模板
```

**GitHub：**
```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## 变更概述
## 关联需求/任务
## 测试情况
## 部署注意事项
EOF
)"
```

### 选项 3：保持现状

报告："保留分支 <name>。工作树保留。"

**不清理工作树。**

### 选项 4：丢弃

**先确认：** "这将永久删除分支 <name> 和所有提交。输入 'discard' 确认。"

确认后：
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

## 步骤 5：清理

选项 1、2、4 需要清理：

```bash
# 如使用 worktree
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>

# 删除远程分支（选项 2）
git push origin --delete <feature-branch>
```

## 快速参考

| 选项 | 合并 | 推送 | 清理分支 | 保留工作树 |
|------|------|------|---------|-----------|
| 1. 本地合并 | ✓ | — | ✓ | — |
| 2. 创建 PR | — | ✓ | —（审查后） | ✓ |
| 3. 保持现状 | — | — | — | ✓ |
| 4. 丢弃 | — | — | ✓（强制） | — |

## PR 描述模板

```
## 变更概述
<一句话描述>

## 关联需求/任务
- REQ-XXX
- TASK-XXX

## 变更文件
- <文件路径>（新增/修改）

## 验证证据
- 单元测试：N 通过 / 0 失败
- Gate C1 质量检查：全部通过
- Gate C2 测试：全部通过

## 部署注意事项
- [ ] 需数据库迁移 [ ] 需更新配置 [ ] 无特殊
```

## 验证清单

- [ ] 测试全部通过（步骤 1）
- [ ] CI 通过（若项目已配置 CI）
- [ ] 代码审查已完成且意见已处理
- [ ] Gate C1 + Gate C2 全部通过
- [ ] 已合并到目标分支
- [ ] 功能分支已删除（本地 + 远程）
- [ ] 实现文档已输出到 `.jarvis/YYYY-MM-DD/implementation/`
- [ ] 相关文档已更新（API 文档 / CHANGELOG）

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 测试失败仍继续合并 | 测试必须全部通过，失败即停止 |
| "接下来做什么？"开放式提问 | 展示 4 个结构化选项 |
| 自动删除可能还需要的 worktree | 只在选项 1/4 时清理 |
| 丢弃时不确认 | 要求输入 'discard' 确认 |

## 红线

- 测试失败时绝不继续
- CI 失败时绝不推送（测试通过不等于 CI 会通过）
- 合并不验证测试结果
- 不确认就删除工作成果
- 未经明确请求就强制推送
