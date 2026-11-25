---
name: ag-skills
description: This skill should be used when the user asks to create an ag-core microservice, define a protobuf API, generate code with aggo, implement service logic, add Kitex/Hertz adapter, generate DAO/Model with gen-go-db, design database tables, build a gRPC/HTTP service with ag-core, use aggo new/proto commands, gen-go-db db commands, or work with ag-core .proto files, internal/service/, idl/api/ directories.
version: 1.0.0
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# ag-core Skills for AI Agents

This skill provides comprehensive ag-core microservices framework knowledge, optimized for AI agents helping developers build production-ready services with protobuf IDL, Kitex (gRPC), and Hertz (HTTP).

> **⚠️ 项目本地规则优先**: 在执行任何开发任务前，先检查项目 `.claude/ai-context/00-instructions.md` 中的规则。项目级别的规则（如目录约定、禁止项）**覆盖**本 skill 中的通用指导。

## When to Use This Skill

Invoke when working with ag-core:
- **Initializing projects**: `aggo new` + AI context injection (see [create-project](workflows/create-project.md))
- **Syncing AI context**: update `.claude/` when skill ai-context is updated (see [update-ai-context](workflows/update-ai-context.md))
- **Defining APIs**: protobuf IDL with gRPC + HTTP annotations
- **Generating code**: `aggo proto` with all plugin/mode combinations
- **Implementing business logic**: `internal/service/` layer
- **Calling other services**: generating and using client code
- **Designing database tables**: defining YAML definitions, running gen-go-db, using generated DAO
- **Building TCP services**: agonet EventLoop network framework, Pipeline handler chain, LengthField codec, TLS/TLCP

## Knowledge Structure

Load specific guides as needed:

### Workflow Guides

#### Create Project
**File**: [workflows/create-project.md](workflows/create-project.md)
**When**: User asks to create/init/scaffold a new ag-core project

#### Sync AI Context
**File**: [workflows/update-ai-context.md](workflows/update-ai-context.md)
**When**: User asks to update/sync AI context to an existing project, or after ai-context has been updated

### Pattern Guides

#### 1. Proto IDL Patterns
**File**: [references/proto-idl-patterns.md](references/proto-idl-patterns.md)
**When**: Writing .proto files, defining gRPC services, adding HTTP annotations
**Contains**: Proto syntax, service patterns, HTTP method annotations, path params, stream RPC

#### 2. Code Generation
**File**: [references/code-generation.md](references/code-generation.md)
**When**: Running `aggo proto`, understanding generation targets, post-generation steps
**Contains**: Full command reference, plugin/mode matrix, output file mapping

#### 3. Project Structure
**File**: [references/project-structure.md](references/project-structure.md)
**When**: Understanding project layout, knowing where to write code vs generated files
**Contains**: Directory tree, file responsibilities, modification rules

#### 4. Kitex Patterns
**File**: [references/kitex-patterns.md](references/kitex-patterns.md)
**When**: Using Kitex for gRPC communication, adding interceptors, configuring gRPC server/client
**Contains**: gRPC server/client architecture, middleware priority system, metadata propagation, fx injection, 流式传输（服务端/客户端实现 + 限制）

#### 5. Hertz Patterns
**File**: [references/hertz-patterns.md](references/hertz-patterns.md)
**When**: Using Hertz for HTTP services, adding middleware, routing, request validation
**Contains**: HTTP routing, ServerConfigurator assembly, middleware injection, request binding, client calls

#### 6. Nacos Patterns
**File**: [references/nacos-patterns.md](references/nacos-patterns.md)
**When**: Service registration, service discovery, Nacos configuration center, SD mode switching, remote config, agnacos module setup
**Contains**: FX module registration (FxNacosNamingMode/FxNacosConfigMode), app.yml config, service registration/discovery, remote config center, local dev bypass

#### 7. AgLog Patterns
**File**: [references/aglog-patterns.md](references/aglog-patterns.md)
**When**: Logging configuration, log levels, structured logging, file rotation, module-specific logging
**Contains**: FX init, GetSlog/GetSlogByName, InfoContext patterns, zap configuration, file rotation, dev/prod switching, best practices

#### 8. Redis Patterns
**File**: [references/redis-patterns.md](references/redis-patterns.md)
**When**: Redis cache, Redis configuration, cache operations, agredis setup
**Contains**: FX init, AgRedisClient injection, 4 config modes (single/cluster/Sentinel/RW), basic operations (String/Hash/List/Set/ZSet), best practices

#### 9. Kafka Patterns
**File**: [references/kafka-patterns.md](references/kafka-patterns.md)
**When**: Kafka messaging, producer, agsarama configuration
**Contains**: FX module (FxAgsaramaModule), sarama.Client injection, config (28 fields + SASL), Sync/Async producer (fx管理生命周期), best practices

#### 10. Kafka Consumer Patterns
**File**: [references/kafka-consumer-patterns.md](references/kafka-consumer-patterns.md)
**When**: Kafka consumer, consumer group, Consumer Server, Multi-Handler
**Contains**: Consumer lifecycle (ag_server.Server + self-managed ctx), Multi-Handler routing (CompositeHandler + fx.In auto-register + routes mapping), handler patterns (kafkahandler包 + biz注入), fx registration (AsKafkaHandler + FxHandlerModule), validation firewall

#### 11. Table YAML Definition
**File**: [references/db-yaml-format.md](references/db-yaml-format.md)
**When**: Defining table structures, designing YAML table definitions, adding indexes/constraints, writing custom queries
**Contains**: YAML format, column definition, type mapping, indexes, self_query_rules, dynamic SQL templates

#### 12. gen-go-db CLI
**File**: [references/gen-go-db-cli.md](references/gen-go-db-cli.md)
**When**: Running `gen-go-db db` to generate Model/DAO from YAML definitions
**Contains**: Command syntax, parameters, output files, usage examples

#### 13. Service Clients
**File**: [references/service-clients.md](references/service-clients.md)
**When**: Calling other microservices, creating client factories, configuring downstream connections, SD/direct switching
**Contains**: ClientsConfig three-part pattern, Kitex/HTTP factory functions, SD/direct switching, app.yml config

#### 14. DAO Usage Guide
**File**: [references/dao-usage.md](references/dao-usage.md)
**When**: Using generated DAO for CRUD, calling named SQL, dynamic query conditions, pagination, transactions
**Contains**: InsertOne/Update/FindByPrimaryKey/FindByStruct/FindByCustomerRule/FindByCondition, fx injection, transactions

#### 15. Verification
**File**: [references/verification.md](references/verification.md)
**When**: Project initialization, adding database tables, adding config modules, adding cross-service calls, adding gRPC/HTTP services, gen-go-db generation
**Contains**: Centralized fx injection checks, build verification, assembly order, runtime declarations — organized by operation scenario

### Supporting Resources

#### Best Practices
**File**: [best-practices/overview.md](best-practices/overview.md)
**When**: Production deployment, code quality, security hardening

#### 16. Configuration Patterns
**File**: [references/ag-conf-patterns.md](references/ag-conf-patterns.md)
**When**: Adding or reading configuration, creating config structs, using app.yml, hot-reload, binding config
**Contains**: Three-part config pattern (struct+default+constructor), value-tag styles, binding vs GetProperty, config priorities

#### 17. Gateway Pattern
**File**: [references/gateway-patterns.md](references/gateway-patterns.md)
**When**: Calling other microservices, organizing biz/gateway/clients layers, integrating Redis/Kafka, defining Gateway interfaces
**Contains**: Three-layer pattern (biz interface → gateway impl → clients factory), ClientsConfig, copier conversion, SD/direct switching

#### 18. Agonet Patterns
**File**: [references/agonet-patterns.md](references/agonet-patterns.md)
**When**: TCP 长连接服务、短连接客户端、自定义通信协议、TLS/TLCP 安全传输、EventLoop 网络框架、Pipeline 管道、LengthField 编解码
**Contains**: FX module (Server/Client/ShortClient), config (TCP/TLS/TLCP/KeepAlive), Simple 三层架构, Pipeline 事件传播, Handler 类型体系, 长连接/短连接客户端, LengthField 编解码器, 常见陷阱

#### Troubleshooting
**File**: [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
**When**: aggo proto errors, compile failures, runtime issues, debugging

## Core Workflows

### Initializing a New Project (with AI Context)

1. Follow [workflows/create-project.md](workflows/create-project.md)
2. This includes: `aggo new` → inject `.claude/` AI context → verify build

### Syncing AI Context to Existing Project

1. Follow [workflows/update-ai-context.md](workflows/update-ai-context.md)
2. This copies the latest ai-context files from skill to project's `.claude/ai-context/`

### Creating a New Service (in Existing Project)

1. Define proto in `idl/api/<service>/`
2. Generate code with `aggo proto` (one command, see code-generation.md)
3. Implement business logic in `internal/biz/<service>_biz.go`
4. Wire thin layer in `internal/service/agservice_*.go` (delegate to biz)
5. `go mod tidy && go build ./...`

### Adding a New API Service

1. Create `idl/api/<service>/<service>.proto`
2. Define gRPC service + HTTP annotations
3. Run full `aggo proto` pipeline
4. Implement biz + service layers as above

### Calling Other Microservices

1. Copy callee's `.proto` to `idl/api/<service>/`
2. `aggo proto -p kitex,hertz -m client ...`
3. Follow Gateway Pattern: clients/ factory → gateway/ impl → biz/ orchestration
   (see [[gateway-patterns]])

## Key Principles

### Always Follow
- Proto-First: define `.proto` before any code
- service/ is thin layer: delegate to biz/ for business logic
- Never edit generated code (adpgen/ svcgen/)
- Post-generation: `go mod tidy && go build ./...`

### Never Do
- Put business logic in `internal/service/` (use biz/)
- Manually edit `adpgen/` or `svcgen/` files
- Skip `go mod tidy` after generation
- Forget HTTP annotations when generating Hertz code
