---
name: dev-backend
description: 使用现代技术（Node.js、Python、Go、Rust）、框架（NestJS、FastAPI、Django）、数据库（PostgreSQL、MongoDB、Redis）、API（REST、GraphQL、gRPC）、认证（OAuth 2.1、JWT）、测试策略、安全最佳实践（OWASP Top 10）、性能优化、可扩展性模式（微服务、缓存、分片）、DevOps 实践（Docker、Kubernetes、CI/CD）与监控来构建健壮的后端系统。适用于设计 API、实现认证、优化数据库查询、搭建 CI/CD 流水线、处理安全漏洞、构建微服务或开发生产级后端系统。
license: MIT
version: 1.0.0
---

# 后端开发技能

使用现代技术、最佳实践与经过验证的模式进行生产级后端开发。

## 适用场景

- 设计 RESTful、GraphQL 或 gRPC API
- 构建认证/授权系统
- 优化数据库查询与 schema
- 实现缓存与性能优化
- OWASP Top 10 安全防护
- 设计可扩展的微服务
- 测试策略（单元、集成、E2E）
- CI/CD 流水线与部署
- 生产系统的监控与调试

## 技术选型指南

**语言:** Node.js/TypeScript（全栈）、Python（数据/ML）、Go（并发）、Rust（性能）
**框架:** NestJS、FastAPI、Django、Express、Gin
**数据库:** PostgreSQL（ACID）、MongoDB（灵活 schema）、Redis（缓存）
**API:** REST（简单）、GraphQL（灵活）、gRPC（性能）

详见：`references/backend-technologies.md` 中的详细对比

## 参考导航

**核心技术:**
- `backend-technologies.md` - 语言、框架、数据库、消息队列、ORM
- `backend-api-design.md` - REST、GraphQL、gRPC 模式与最佳实践

**安全与认证:**
- `backend-security.md` - OWASP Top 10 2025、安全最佳实践、输入校验
- `backend-authentication.md` - OAuth 2.1、JWT、RBAC、MFA、会话管理

**性能与架构:**
- `backend-performance.md` - 缓存、查询优化、负载均衡、扩展
- `backend-architecture.md` - 微服务、事件驱动、CQRS、saga 模式

**质量与运维:**
- `backend-testing.md` - 测试策略、框架、工具、CI/CD 测试
- `backend-code-quality.md` - SOLID 原则、设计模式、整洁代码
- `backend-devops.md` - Docker、Kubernetes、部署策略、监控
- `backend-debugging.md` - 调试策略、性能分析、日志、生产环境调试
- `backend-mindset.md` - 问题求解、架构思维、协作

## 关键最佳实践（2025）

**安全:** Argon2id 密码、参数化查询（SQL 注入减少 98%）、OAuth 2.1 + PKCE、限流、安全响应头

**性能:** Redis 缓存（数据库负载降低 90%）、数据库索引（I/O 减少 30%）、CDN（延迟降低 50%+）、连接池

**测试:** 70-20-10 金字塔（单元-集成-E2E）、Vitest 比 Jest 快 50%、微服务契约测试、83% 的迁移在没有测试时失败

**DevOps:** 蓝绿/金丝雀部署、特性开关（故障减少 90%）、Kubernetes 采用率 84%、Prometheus/Grafana 监控、OpenTelemetry 链路追踪

## 快速决策矩阵

| 需求 | 选择 |
|------|--------|
| 快速开发 | Node.js + NestJS |
| 数据/ML 集成 | Python + FastAPI |
| 高并发 | Go + Gin |
| 极致性能 | Rust + Axum |
| ACID 事务 | PostgreSQL |
| 灵活 schema | MongoDB |
| 缓存 | Redis |
| 内部服务 | gRPC |
| 公开 API | GraphQL/REST |
| 实时事件 | Kafka |

## 实施清单

**API:** 选择风格 → 设计 schema → 校验输入 → 添加认证 → 限流 → 文档 → 错误处理

**数据库:** 选择数据库 → 设计 schema → 创建索引 → 连接池 → 迁移策略 → 备份/恢复 → 测试性能

**安全:** OWASP Top 10 → 参数化查询 → OAuth 2.1 + JWT → 安全响应头 → 限流 → 输入校验 → Argon2id 密码

**测试:** 单元 70% → 集成 20% → E2E 10% → 负载测试 → 迁移测试 → 契约测试（微服务）

**部署:** Docker → CI/CD → 蓝绿/金丝雀 → 特性开关 → 监控 → 日志 → 健康检查

## 资源

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/
