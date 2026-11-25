---
name: hertz-knowledge
description: 当在 Hertz 框架项目中开发、用 hertztool 从 IDL 生成代码、处理 app.RequestContext、配置路由/中间件、参数绑定验证（Binding/Validator）、或配置 Netpoll/TLS/HTTP2 时使用。
user-invocable: false
---

# Hertz 知识库

Hertz 是字节跳动内部自研的高性能 Golang HTTP 框架，基于高性能网络库 Netpoll，提供卓越的吞吐量和低延迟。

## 快速入门

Hertz 框架的基础概念和入门指南：

- **框架概览**：了解 Hertz 的核心特性和架构
- **安装配置**：环境准备和项目初始化
- **第一个服务**：创建和运行 HTTP 服务

**使用场景**：
- 新建 Hertz 项目
- 了解 Hertz 框架特性
- HTTP 服务开发入门

[what-is-hertz.md](./what-is-hertz.md) - Hertz 框架概览
[install-and-setup.md](./install-and-setup.md) - 安装和配置
[create-first-service.md](./create-first-service.md) - 创建第一个服务

## 代码生成

使用 Hertztool 从 IDL 自动生成代码：

- **IDL 注解定义**：Thrift/Protobuf IDL 注解规范
- **代码生成工具**：使用 Hertztool 生成代码
- **生成代码示例**：理解生成的代码结构

**使用场景**：
- IDL 驱动开发
- 自动生成 Handler 代码
- API 接口定义

[define-idl-annotations.md](./define-idl-annotations.md) - 定义 IDL 注解
[advanced-idl-annotations.md](./advanced-idl-annotations.md) - 高级 IDL 注解
[generate-code-with-hertztool.md](./generate-code-with-hertztool.md) - 使用 Hertztool 生成代码
[generate-code-example.md](./generate-code-example.md) - 代码生成示例

## 路由与处理器

路由管理和请求处理：

- **路由管理**：静态路由、参数路由、路由组
- **Handler 实现**：请求处理函数编写
- **请求上下文**：理解 RequestContext 的使用

**使用场景**：
- API 路由设计
- 请求处理逻辑
- 上下文数据传递

[manage-routes.md](./manage-routes.md) - 路由管理
[implement-handlers.md](./implement-handlers.md) - 实现 Handler
[understanding-request-context.md](./understanding-request-context.md) - 理解请求上下文
[request-context.md](./request-context.md) - 请求上下文概述
[request-api.md](./request-api.md) - Request API 详解
[response-api.md](./response-api.md) - Response API 详解

## 参数绑定与验证

请求参数的自动绑定和验证：

- **参数绑定**：Query、Body、Header 等参数绑定
- **参数验证**：使用 validator 进行参数校验
- **自定义绑定**：自定义绑定器和验证器

**使用场景**：
- API 参数处理
- 输入验证
- 错误处理

[bind-and-validate-request.md](./bind-and-validate-request.md) - 参数绑定和验证

## 中间件

Hertz 中间件机制和常用中间件：

- **中间件机制**：理解中间件的工作原理
- **内置中间件**：日志、恢复、跨域等
- **自定义中间件**：编写自定义中间件

**使用场景**：
- 请求日志记录
- 认证授权
- 跨域处理
- 错误恢复

[using-middleware.md](./using-middleware.md) - 使用中间件

## 服务配置

Hertz Server 和协议配置：

- **服务器配置**：端口、超时、连接池等配置
- **协议配置**：HTTP/1.1、HTTP/2、HTTPS 配置

**使用场景**：
- 服务性能调优
- HTTPS 配置
- 协议升级

[configure-server.md](./configure-server.md) - 服务器配置
[configure-protocols.md](./configure-protocols.md) - 协议配置

## HTTP 客户端

Hertz 提供的高性能 HTTP 客户端：

- **客户端使用**：发起 HTTP 请求
- **连接复用**：连接池管理
- **超时控制**：请求超时配置

**使用场景**：
- 调用外部 HTTP API
- 微服务间 HTTP 通信
- 第三方服务集成

[using-http-client.md](./using-http-client.md) - 使用 HTTP 客户端

## 最佳实践

Hertz 开发的最佳实践和规范：

- **代码组织**：项目结构和代码规范
- **性能优化**：性能调优建议
- **错误处理**：错误处理模式

**使用场景**：
- 代码审查
- 性能优化
- 问题排查

[best-practices.md](./best-practices.md) - 最佳实践
