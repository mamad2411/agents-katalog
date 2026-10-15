---
name: te-operation
version: 1.0.0
description: "TE 运营管理：任务、流程画布、推送通道、空间导航"
metadata:
  requires:
    bins: ["te-cli"]
  cliHelp: "te-cli operation --help"
---

# te-operation

> **前置条件:** 阅读 [`../te-shared/SKILL.md`] 了解认证、项目选择和通用约定。

## 概述

`te-operation` 域负责 TE 平台的运营管理能力，包括：

- **任务管理** — 创建运营任务、查看任务列表与统计
- **流程画布** — 保存和管理自动化流程（Flow）
- **推送通道** — 查看推送通道配置
- **空间导航** — 获取空间树、时区、标记时间等基础信息

所有命令通过 `te-cli operation +<command>` 调用。

## 核心场景

### 1. 任务管理
```bash
# 创建运营任务
te-cli operation +create-task -p <project-id> --task-config '{"name":"双十一活动","type":"push"}'

# 分页查看任务列表
te-cli operation +list-tasks -p <project-id> --page 1 --page-size 20

# 查看任务统计数据
te-cli operation +get-task-stats -p <project-id> --task-id 100
```

### 2. 流程画布
```bash
# 保存流程配置
te-cli operation +save-flow -p <project-id> --flow-config '{"name":"新用户引导","nodes":[...]}'

# 列出所有流程
te-cli operation +list-flows -p <project-id>

# 获取流程详情
te-cli operation +get-flow -p <project-id> --flow-uuid "abc-123-def"
```

### 3. 推送通道
```bash
# 列出推送通道
te-cli operation +list-channels -p <project-id>

# 获取通道详情
te-cli operation +get-channel -p <project-id> --channel-id 5
```

### 4. 空间导航与基础信息
```bash
# 获取空间树
te-cli operation +get-space-tree -p <project-id>

# 获取时区信息
te-cli operation +get-timezone -p <project-id>

# 列出标记时间
te-cli operation +list-mark-times -p <project-id>
```

## 参考文档

详见 `references/` 目录下各命令文档。
