---
name: discord-governance
description: Discord 服务器分区和管理流程。用于创建/管理分类、频道、子区，维护置顶摘要，执行归档操作。触发词：Discord 整理、频道管理、子区管理、归档频道。
---

# Discord 治理 Skill

我们 Discord 服务器的分区和管理规范。

## 核心理念

| 层级 | 用途 | 生命周期 |
|------|------|----------|
| **分类** | 大方向分组 | 长期稳定 |
| **频道** | 项目/领域入口，放规范和链接 | 长期稳定 |
| **子区** | 具体任务/讨论 | 完成后归档 |

**原则**：频道保持干净做管理，子区承载真正的对话。

## 快速参考

### 新建子区
```
1. 在对应频道创建子区
2. 发送置顶摘要（见 templates/pinned-summary.md）
3. 置顶该消息
```

### 归档子区
```
1. 更新置顶摘要，标记为 ✅ 已完成
2. 让子区自动归档（或手动归档）
```

### 更新摘要
```
讨论有重要结论时，更新置顶消息的「关键结论」部分
```

## 参考文档

| 文档 | 内容 |
|------|------|
| [philosophy.md](references/philosophy.md) | 设计理念详解 |
| [structure.md](references/structure.md) | 当前服务器结构 |
| [naming.md](references/naming.md) | 命名规范 |
| [templates/](references/templates/) | 置顶摘要、频道简介模板 |
| [workflows/](references/workflows/) | 具体操作流程 |

## 服务器信息

- **服务器 ID**：（填入你的服务器 ID）
- **服务器名称**：（填入你的服务器名称）
