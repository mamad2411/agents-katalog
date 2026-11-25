---
name: gdp-knowledge
description: 当在 GDP 框架项目中开发时必读。触发场景：GDP 开发流程、GDP 开发规范、GDP组件使用、插件与中间件开发、执行 gdp init/update/lint 命令、实现 Handler/Action/Domain/DAL/DAO 分层代码、使用 code.byted.org/gdp 包（af/raf/compkg/log/metrics/config/mocks）。
user-invocable: false
---

# GDP 知识库

GDP (Go Development Platform) 是字节跳动内部的 Golang 服务开发框架，采用 IDL 驱动开发模式，提供标准化的代码分层架构。

## 开发指南

GDP 项目开发的核心流程和规范：

- **IDL 驱动开发**：先定义接口（IDL），再生成代码骨架，最后实现业务逻辑
- **代码分层架构**：按 Handler → Action → Domain → DAL → DAO 调用链组织代码
- **工作流规范**：使用 `gdp update` 同步代码，禁止手动创建生成目录下的文件

**使用场景**：
- 新建 GDP 项目
- 了解 GDP 开发流程
- 代码结构规范

[guide/guide.md](./guide/guide.md) - GDP 项目开发规范总览
[guide/workflow-guide.md](./guide/workflow-guide.md) - 开发工作流指南
[guide/code-layers-guide.md](./guide/code-layers-guide.md) - 代码分层架构指南

## 代码分层示例

各层代码的编写规范和示例：

- **Action 层**：接入层，参数绑定和校验
- **Domain 层**：业务逻辑层，核心业务实现
- **DAL 层**：数据服务层，聚合 DAO、调用 RPC
- **DAO 层**：数据模型层，数据库 CRUD 操作

**使用场景**：
- 编写各层业务代码
- 理解代码职责划分
- 代码审查参考

[code-layers/action-examples.md](./code-layers/action-examples.md) - Action 层示例
[code-layers/domain-examples.md](./code-layers/domain-examples.md) - Domain 层示例
[code-layers/dal-examples.md](./code-layers/dal-examples.md) - DAL 层示例
[code-layers/dao-examples.md](./code-layers/dao-examples.md) - DAO 层示例

## GDP 组件

GDP 官方提供的组件使用指南：

- **配置管理**：使用 GDP 配置组件管理应用配置
- **日志**：标准化日志记录
- **监控指标**：Metrics 埋点和监控
- **测试**：单元测试和集成测试

**使用场景**：
- 配置管理和热更新
- 日志记录最佳实践
- 服务监控和告警

[components/config.md](./components/config.md) - 配置管理
[components/log.md](./components/log.md) - 日志组件
[components/metrics.md](./components/metrics.md) - 监控指标
[components/testing.md](./components/testing.md) - 测试组件
[components/compkg.md](./components/compkg.md) - 通用组件包

## GDP 命令

GDP CLI 工具命令参考：

- **gdp init**：初始化 GDP 项目
- **gdp update**：同步 IDL 并生成代码
- **gdp lint**：代码规范检查

**使用场景**：
- 项目初始化
- 代码生成和更新
- 代码质量检查

[commands/init-command.md](./commands/init-command.md) - init 命令
[commands/update-command.md](./commands/update-command.md) - update 命令
[commands/lint-command.md](./commands/lint-command.md) - lint 命令

## 插件与中间件

GDP 框架提供的插件（af 专属）和中间件（af/raf 通用）机制，用于注入通用逻辑：

- **插件**：基于 AOP，分阶段执行（OnStartup/OnShutdown/OnSuccess/OnError），优先于中间件执行
- **中间件**：基于责任链，开发简单，支持 Next/Abort 流程控制
- **自定义参数传递**：基于 URI 的静态参数注册，可向插件/中间件传递接口级别参数

**使用场景**：
- 开发通用逻辑（鉴权、日志、限流等）
- 选择插件还是中间件
- 实现基于接口的静态传参

[components/plugin-middleware.md](./components/plugin-middleware.md) - 插件与中间件开发指南

## RAL 资源访问层

资源访问层的使用指南，包括数据库、缓存、RPC 调用等：

- **数据库访问**：MySQL/PostgreSQL 访问
- **缓存访问**：Abase/Redis 使用
- **RPC 调用**：调用其他服务
- **消息队列**：EventBus 使用

**使用场景**：
- 数据库 CRUD 操作
- 缓存读写
- 服务间 RPC 调用
- 异步消息处理

[ral/overview.md](./ral/overview.md) - RAL 概述
[ral/database.md](./ral/database.md) - 数据库访问
[ral/abase_redis.md](./ral/abase_redis.md) - Abase/Redis 缓存
[ral/rpc.md](./ral/rpc.md) - RPC 调用
[ral/eventbus.md](./ral/eventbus.md) - EventBus 消息队列
[ral/testing.md](./ral/testing.md) - RAL 测试
