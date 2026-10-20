---
description: |
  当用户要求"发消息/写 MQ/消息队列/事件"时触发。
  覆盖消息幂等、死信队列、延迟消息、事务消息。

triggers:
  - 发消息
  - 写 MQ
  - 消息队列
  - 事件
  - MQ
  - messaging
  - RocketMQ
  - Kafka

priority: medium
alwaysApply: false
globs: "**/*Event*.java, **/*Listener*.java, **/*Handler*.java, **/application*.yaml"

category: messaging
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/messaging.md

related-skills:
  - coding
  - debug-issue

when-to-use: |
  发布 / 消费消息、设计事件驱动
when-not-to-use: |
  仅阅读消息代码
version: "0.3.0"
since: "2026-08-13"
---

# 消息队列规范

> 完整规范详见 `wiki/_common/messaging.md`

## 硬约束（MUST）

- ✅ **MUST** 消费端幂等（用 Redis SETNX 去重）
- ✅ **MUST** 配置死信队列（DLQ）+ 告警
- ✅ **MUST** 跨服务消息经生态消息桥（具体类名见栈级规则，如 structure-boot 用 `DataScopeStreamBridge`）
- ✅ **MUST** 用生态事件管理器发布事件（具体类名见栈级规则）
- ✅ **MUST** 事件实现生态事件接口（具体接口见栈级规则）

## 禁止（MUST NOT）

- ❌ 在 Consumer 里写业务逻辑（应 dispatch 给 handler）
- ❌ 跳过幂等设计
- ❌ 不配 DLQ

## 关联

- Wiki：`wiki/_common/messaging.md`
- 技能：`coding` / `debug-issue`
