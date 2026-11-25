---
name: customize-reasonix
description: 配置 Reasonix 自身 — 查看/修改 config.json、管理全局记忆、查看技能目录结构
---
# Customize Reasonix

帮助你查看和配置 Reasonix 自身的设置。

## 能做什么

| 操作 | 方法 |
|------|------|
| 查看当前配置 | `read_file("~/.reasonix/config.json")` |
| 查看全局记忆清单 | `list_directory("~/.reasonix/memory/global/")` |
| 查看技能清单 | `list_directory("~/.reasonix/skills/")` |
| 安装新技能 | `install_skill(...)` 或写入 `~/.reasonix/skills/<name>/SKILL.md` |
| 查看用量统计 | `read_file("~/.reasonix/usage.jsonl")` |
| 查看会话日志 | `list_directory("~/.reasonix/sessions/")` |
| 查看版本 | `read_file("~/.reasonix/version-cache.json")` |

## 配置位置

```
~/.reasonix/
├── config.json          Reasonix 平台配置
├── memory/global/       全局记忆（持久化行为规则）
├── memory/project/      项目记忆
├── skills/              技能目录
│   ├── <name>/SKILL.md  目录技能
│   └── <name>.md        单文件技能
├── sessions/            会话日志
└── usage.jsonl          用量追踪
```
