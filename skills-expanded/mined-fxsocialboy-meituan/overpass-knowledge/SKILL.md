---
name: overpass-knowledge
description: 当使用 Overpass 进行 RPC 调用、自动生成 kitex_gen 代码、配置 Overpass Go 客户端、或查阅 Overpass 使用指南时使用。
user-invocable: false
---

# Overpass 知识库

Overpass 是 ByteDance 内部的一站式 RPC 调用解决方案，可以全自动生成 RPC 调用代码，简化微服务间的调用流程。

## 平台简介

Overpass 的核心价值和解决的问题：

- **自动生成 kitex_gen 代码**：无需手动运行 kitex tool
- **自动创建和管理 Client**：统一的 Client 封装
- **IDL 变更自动更新**：与 DevFlow 平台集成

**使用场景**：
- 了解 Overpass 平台
- 评估是否使用 Overpass
- 与传统方式对比

[overpass-introduction.md](./overpass-introduction.md) - Overpass 平台简介

## 快速入门

快速开始使用 Overpass：

- **核心概念**：理解 Overpass 的工作原理
- **快速入门**：5 分钟上手 Overpass

**使用场景**：
- 首次使用 Overpass
- 快速集成 RPC 调用

[overpass-concepts.md](./overpass-concepts.md) - 核心概念
[overpass-quickstart.md](./overpass-quickstart.md) - 快速入门

## Go 语言使用

在 Go 项目中使用 Overpass：

- **Go 使用指南**：完整的 Go 语言使用示例
- **常用结构体**：Overpass 提供的通用结构体

**使用场景**：
- Go 项目集成 Overpass
- RPC 调用代码编写

[overpass-go-usage.md](./overpass-go-usage.md) - Go 语言使用指南
[overpass-common-structs.md](./overpass-common-structs.md) - 常用结构体

## 客户端配置

Overpass 客户端的配置选项：

- **客户端配置**：超时、重试、熔断等配置
- **高级配置**：自定义配置选项

**使用场景**：
- 调整 RPC 调用参数
- 性能优化
- 可靠性配置

[overpass-client-configuration.md](./overpass-client-configuration.md) - 客户端配置

## 平台操作

Overpass 平台的操作指南：

- **平台操作**：在 Overpass 平台上的操作流程
- **IDL 管理**：与 DevFlow 集成

**使用场景**：
- 在平台上添加新的 RPC 依赖
- 管理 IDL 版本

[overpass-platform-operations.md](./overpass-platform-operations.md) - 平台操作指南

## 问题排查

Overpass 使用中的问题排查：

- **常见问题**：FAQ 和解决方案
- **错误排查**：错误信息解读

**使用场景**：
- 遇到问题时排查
- 理解错误信息

[overpass-troubleshooting.md](./overpass-troubleshooting.md) - 问题排查
