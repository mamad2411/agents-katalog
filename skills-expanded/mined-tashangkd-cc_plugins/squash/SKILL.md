---
name: squash
description: Commit 历史整理与合并。将 TDD 循环产生的多个细碎 commit 合并为有意义的功能 commit，包含安全检查、交互式 rebase 指导。用户提到 squash、整理 commit 时使用。
user-invocable: true
---

# Commit 历史整理

> **TDD 产生的小 commit 应该在功能完成后整理**

将 TDD 循环产生的多个细碎 commit 合并为有意义的功能 commit。

---

## 快捷命令

```bash
/squash              # 交互式引导（自动安全检查）
/squash feature       # 合并单个功能的所有 commit
/squash abort         # 中止 rebase
```

**⚠️ 安全警告**：Squash 仅适用于**本地未推送的 commit**。

---

## 1. 安全检查

### 快速检查

| 检查 | 命令 | 安全 | 危险 |
|------|------|------|------|
| 保护分支 | `git branch --show-current` | feature/* | main/master |
| 未推送 | `git log @{u}..` | 有输出 | 无输出 |

**Golden Rule**：只整理**本地未推送**的 commit。

---

## 2. 交互式 Rebase

### 2.1 合并最近 N 个 commit

```bash
# 查看最近 commit
git log --oneline -10

# 合并最近 6 个 commit
git rebase -i HEAD~6
```

### 2.2 Rebase 命令

| 命令 | 说明 |
|------|------|
| `pick` | 保留此 commit |
| `squash` | 合并到前一个 commit |
| `fixup` | 合并到前一个，丢弃 message |
| `drop` | 删除此 commit |

### 2.3 合并示例

**Before**：
```
pick abc1234 test: 添加订单测试
pick def5678 feat: 实现订单功能
pick ghi9012 refactor: 提取验证函数
```

**After**：
```
pick abc1234 test: 添加订单测试
fixup def5678 feat: 实现订单功能
fixup ghi9012 refactor: 提取验证函数
```

---

## 3. 快速合并

```bash
# 方式 A：软重置后重新提交
git reset --soft HEAD~4
git commit -m "feat: 实现完整功能"

# 方式 B：自动 fixup
GIT_SEQUENCE_EDITOR="sed -i '2,$s/^pick/fixup/'" git rebase -i HEAD~4
```

---

## 4. 推送重写的历史

```bash
git push --force-with-lease origin feature-branch
```

| 命令 | 说明 |
|------|------|
| `--force-with-lease` | **推荐**：如果远程有新提交则失败 |
| `--force` / `-f` | 强制覆盖，可能丢失他人提交 |

---

## 5. 故障恢复

```bash
# 放弃 rebase
git rebase --abort

# 恢复到 rebase 前的状态
git reflog
git reset --hard HEAD@{N}
```

---

## 6. 清理空间

```bash
# 快速清理（推荐）
git gc --prune=now

# 激进清理（.git 过大时）
git gc --aggressive --prune=now
```

---

**小 commit 开发 → 整理后推送 → 干净的历史**
