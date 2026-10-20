---
name: kitex-knowledge
description: 当在 Kitex 框架项目中开发、定义 Thrift/Protobuf IDL、生成 Client/Server 代码、配置服务发现/负载均衡/超时/重试、使用泛化调用（Generic Call）或 Streaming、排查 RPC 错误码（如 103 超时、1201 连接服务端超时、1601 ACL拒绝等）时使用。
user-invocable: false
---

# Kitex 知识库

Kitex 是字节跳动内部的 Golang 微服务 RPC 框架，基于高性能网络库 Netpoll，支持 Thrift、Protobuf、gRPC 等多种协议。

## 快速入门

Kitex 框架的基础概念和入门指南：

- **快速入门**：面向有经验开发者的快速上手指南
- **框架概览**：了解 Kitex 的核心特性和架构
- **核心概念**：RPC、IDL、服务发现等基础概念
- **安装配置**：环境准备和项目初始化
- **第一个服务**：创建和运行 RPC 服务

**使用场景**：
- 新建 Kitex 项目
- 了解 RPC 框架基础
- 微服务开发入门

[quick-start.md](./quick-start.md) - 快速入门（有经验开发者）
[what-is-kitex.md](./what-is-kitex.md) - Kitex 框架概览
[key-concepts.md](./key-concepts.md) - 核心概念
[install-and-setup.md](./install-and-setup.md) - 安装和配置
[create-first-service.md](./create-first-service.md) - 创建第一个服务

## IDL 与代码生成

使用 Thrift IDL 定义服务接口：

- **Thrift IDL 定义**：服务接口和数据结构定义
- **代码生成**：从 IDL 生成 Go 代码

**使用场景**：
- 定义服务接口
- 自动生成客户端/服务端代码
- API 契约管理

[define-thrift-idl.md](./define-thrift-idl.md) - 定义 Thrift IDL
[generate-code-from-idl.md](./generate-code-from-idl.md) - 从 IDL 生成代码

## 服务治理

Kitex 的服务治理能力：

- **启动配置**：Server 启动时的配置加载
- **服务配置**：客户端和服务端配置
- **负载均衡**：内置和自定义负载均衡策略
- **超时控制**：请求超时配置
- **重试机制**：失败重试策略

**使用场景**：
- 服务调用优化
- 高可用配置
- 流量治理

[startup-configuration.md](./startup-configuration.md) - 启动配置
[configure-service.md](./configure-service.md) - 服务配置
[configure-loadbalance.md](./configure-loadbalance.md) - 负载均衡配置
[configure-timeout.md](./configure-timeout.md) - 超时配置
[configure-retry.md](./configure-retry.md) - 重试配置

## 高级特性

Kitex 的高级功能：

- **中间件**：请求处理中间件
- **Call Options**：动态调用选项
- **连接池**：连接池调优
- **泛化调用**：无 IDL 调用
- **流式传输**：Streaming 支持

**使用场景**：
- 自定义请求处理
- 性能调优
- 特殊场景适配

[using-middleware.md](./using-middleware.md) - 使用中间件
[get-response-in-middleware.md](./get-response-in-middleware.md) - 在中间件中获取响应
[using-call-options.md](./using-call-options.md) - 使用 Call Options
[tune-connection-pool.md](./tune-connection-pool.md) - 连接池调优
[using-generic-call.md](./using-generic-call.md) - 泛化调用
[using-streaming.md](./using-streaming.md) - 流式传输

## 扩展开发

自定义扩展组件：

- **自定义负载均衡器**：实现自定义负载均衡策略
- **自定义服务发现**：实现自定义 Resolver

**使用场景**：
- 定制化需求
- 集成第三方组件

[implement-custom-loadbalancer.md](./implement-custom-loadbalancer.md) - 自定义负载均衡器
[implement-custom-resolver.md](./implement-custom-resolver.md) - 自定义 Resolver

## 错误处理

Kitex 的错误处理机制：

- **错误类型**：理解 Kitex 错误分类
- **错误处理**：正确处理 RPC 错误
- **错误处理指南**：最佳实践
- **错误码参考**：Kitex/Kite、Mesh Proxy、DES-RPC 等错误码详解

**使用场景**：
- 错误码设计
- 异常处理
- 问题排查
- 根据错误码定位问题

[handle-errors.md](./handle-errors.md) - 错误处理
[error-handling-guide.md](./error-handling-guide.md) - 错误处理指南
[error-codes.md](./error-codes.md) - 错误码参考（Kitex/Mesh/DES-RPC/MySQL）

## 最佳实践与 FAQ

Kitex 开发的最佳实践和常见问题：

- **最佳实践**：开发规范和性能优化
- **常见问题**：FAQ 和问题排查

**使用场景**：
- 代码审查
- 问题排查
- 性能优化

[best-practices.md](./best-practices.md) - 最佳实践
[common-issues-faq.md](./common-issues-faq.md) - 常见问题 FAQ
