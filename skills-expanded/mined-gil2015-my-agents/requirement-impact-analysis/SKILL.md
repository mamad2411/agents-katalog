---
name: requirement-impact-analysis
description: Use when frontend requirements need scope control, interaction coverage, or downstream implementation and testing impact mapping
---

# Requirement Impact Analysis

## 产物

- `req.md`
- `issues.md`
- `scope.md`
- `impact-map.md`

## `scope.md`

记录本轮做什么、不做什么、任务类型和停止点。

## `impact-map.md`

每条需求映射到：

- 页面区域
- 交互动作
- 数据字段
- 接口依赖
- 状态变化
- 权限/异常/空态/加载态
- 验收标准
- 测试范围

## 规则

没有显式影响面，就不能交给下游猜。
