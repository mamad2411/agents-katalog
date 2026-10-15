---
name: check-opencode-updates
description: 检查 opencode 和 oh-my-openagent (omo) 的版本更新情况，有更新时自动获取并展示 release 说明。当用户提及版本检查、更新、版本对比、更新日志、release notes，或询问 opencode/omo 是否需要更新、有没有新版本时，立即使用此技能。即使用户只是随意提到"检查更新"或"版本"，也应触发此技能进行版本检查。
---

# check-opencode-updates

检查 opencode 和 oh-my-openagent (omo) 的版本更新情况，有更新时自动获取并展示 release 说明。

## 快速开始

```bash
python3 skills/check-opencode-updates/scripts/check_updates.py
```

## 输出格式

**无更新时：**
```
opencode: 1.2.27 (up to date)
oh-my-openagent: 3.12.3 (up to date)
```

**有更新时：**
```
opencode: 1.2.27 (up to date)
oh-my-openagent: 3.12.2 (update available)

==================================================

## oh-my-openagent 更新日志

### v3.12.3
- revert(todo-continuation): remove debug logging

[查看完整发布说明](https://github.com/code-yeongyu/oh-my-openagent/releases/tag/v3.12.3)
```

## 状态说明

| 状态 | 含义 |
|------|------|
| `up to date` | 本地版本与远程版本一致 |
| `update available` | 远程有新版本可用，并展示更新日志 |
| `not installed` | 本地未安装 |
| `error` | 获取版本失败 |

## 功能说明

1. 通过 GitHub API 获取最新版本，对比本地版本
2. 有更新时，自动获取本地版本到最新版本之间的所有 release 说明
3. 过长的 release 说明会自动截取前 500 字符

## 注意

- 不自动执行更新操作
- 只检查 opencode 和 oh-my-openagent 两个工具
