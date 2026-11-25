---
name: te-audience
version: 1.0.0
description: "TE 受众管理：用户标签、分群、受众属性"
metadata:
  requires:
    bins: ["te-cli"]
  cliHelp: "te-cli audience --help"
---

# te-audience

> **前置条件:** 阅读 [`../te-shared/SKILL.md`] 了解认证、项目选择和通用约定。

## 概述

`te-audience` 域负责 TE 平台的受众管理能力，包括：

- **用户标签** — 查询和管理用户标签体系
- **用户分群** — 查看分群列表、预估分群人数
- **受众事件** — 获取受众相关事件定义
- **受众属性** — 加载受众属性（用户属性、事件属性等）

所有命令通过 `te-cli audience +<command>` 调用。

## 核心场景

### 1. 查看用户标签体系
```bash
# 列出项目下所有用户标签
te-cli audience +list-tags -p <project-id>

# 获取某个标签的详细信息
te-cli audience +get-tag -p <project-id> --tag-id 42
```

### 2. 用户分群管理
```bash
# 列出所有用户分群
te-cli audience +list-clusters -p <project-id>

# 预估满足条件的实体数量
te-cli audience +predict-cluster-count -p <project-id> --conditions '{"property":"age","op":"gt","value":18}'
```

### 3. 受众事件与属性
```bash
# 列出受众事件
te-cli audience +list-audience-events -p <project-id>

# 加载受众属性（并行调用 3 个 API）
te-cli audience +load-audience-props -p <project-id>

# 可选传入 events 过滤
te-cli audience +load-audience-props -p <project-id> --events '[{"name":"login"}]'
```

## 参考文档

详见 `references/` 目录下各命令文档。
