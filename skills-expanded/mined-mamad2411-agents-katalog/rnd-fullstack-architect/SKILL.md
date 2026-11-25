---
name: rnd-fullstack-architect
description: "全栈架构设计专家 - 精通前后端架构设计、微服务架构、云原生架构、移动端架构。适用场景：(1) SaaS 产品架构设计，(2) 微服务拆分与治理，(3) 前端工程架构，(4) 移动端架构（iOS/Android/跨平台），(5) API 设计与网关架构，(6) 数据库选型与设计，(7) DevOps 与部署架构，(8) 高可用与容灾设计，(9) 性能优化与扩展策略"
---

# 全栈架构设计师

## 系统架构全景

```
┌──────────────────────────────────────────────────────────┐
│                      客户端层                             │
│  ┌────────┐  ┌──────────┐  ┌────────┐  ┌────────┐       │
│  │  Web   │  │  Mobile  │  │Desktop │  │  IoT   │       │
│  │(React) │  │(RN/Flutter)│(Electron)│(Embedded)│       │
│  └────────┘  └──────────┘  └────────┘  └────────┘       │
├──────────────────────────────────────────────────────────┤
│                      接入层                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │     CDN     │  │   API网关   │  │     WAF     │      │
│  │(CloudFlare) │  │(Kong/Apisix)│  │  (防火墙)   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
├──────────────────────────────────────────────────────────┤
│                      服务层                               │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│  │用户服务│ │订单服务│ │支付服务│ │消息服务│ │搜索服务││
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│
├──────────────────────────────────────────────────────────┤
│                      数据层                               │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│  │ MySQL  │ │ Redis  │ │   ES   │ │ Kafka  │ │  OSS   ││
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│
└──────────────────────────────────────────────────────────┘
```

## 前端架构模式

### 分层架构 (Feature-Sliced Design)

```
src/
├── app/                    # 应用层：路由、布局、全局配置
│   ├── (routes)/
│   ├── layout.tsx
│   └── providers.tsx
├── features/               # 特性层：按业务模块组织
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── types.ts
│   ├── dashboard/
│   └── settings/
├── shared/                 # 共享层
│   ├── components/         # 通用UI组件
│   ├── hooks/              # 通用Hooks
│   ├── utils/              # 工具函数
│   └── types/              # 类型定义
└── infrastructure/         # 基础设施层
    ├── api/                # API客户端 (axios/fetch)
    ├── store/              # 状态管理
    └── i18n/               # 国际化
```

### 状态管理选型

| 场景 | 推荐方案 | 特点 |
|------|----------|------|
| 服务端状态 | TanStack Query / SWR | 缓存、后台刷新、乐观更新 |
| 客户端全局状态 | Zustand / Jotai | 轻量、原子化 |
| 表单状态 | React Hook Form | 性能优化、校验集成 |
| URL状态 | nuqs / searchParams | 可分享、SEO友好 |

### 性能优化策略

```
1. 代码分割: React.lazy + Suspense
2. 虚拟列表: @tanstack/react-virtual
3. 图片优化: next/image, lazy loading
4. 缓存策略: Service Worker, HTTP Cache
5. 预加载: prefetch, preload, preconnect
```

## 后端架构模式

### 微服务拆分原则

```
1. 单一职责: 每个服务只做一件事
2. 业务边界: 按领域边界划分 (DDD)
3. 数据自治: 每个服务独立数据库
4. 独立部署: 服务可独立发布
5. 容错设计: 服务降级、熔断、限流
```

### 服务通信模式

| 模式 | 场景 | 技术选型 |
|------|------|----------|
| 同步调用 | 实时查询 | gRPC (内部) / REST (对外) |
| 异步消息 | 事件驱动 | Kafka / RabbitMQ |
| 服务发现 | 动态寻址 | Consul / Nacos / K8s Service |
| 配置中心 | 统一配置 | Apollo / Nacos / Consul |

### 典型服务结构 (Clean Architecture)

```
service/
├── cmd/                    # 入口点
│   └── main.go
├── internal/
│   ├── domain/             # 领域层
│   │   ├── entity/         # 实体
│   │   ├── valueobject/    # 值对象
│   │   └── service/        # 领域服务
│   ├── application/        # 应用层
│   │   ├── usecase/        # 用例
│   │   └── dto/            # 数据传输对象
│   ├── infrastructure/     # 基础设施层
│   │   ├── repository/     # 仓储实现
│   │   └── external/       # 外部服务
│   └── interfaces/         # 接口层
│       ├── http/           # HTTP Handler
│       └── grpc/           # gRPC Handler
├── pkg/                    # 可导出包
└── api/                    # API定义
    ├── proto/              # gRPC定义
    └── openapi/            # OpenAPI定义
```

## 数据库架构

### 选型指南

| 类型 | 场景 | 推荐 | 特点 |
|------|------|------|------|
| 关系型 | 事务、复杂查询 | PostgreSQL | ACID、扩展性强 |
| 文档型 | 灵活Schema | MongoDB | 水平扩展、聚合查询 |
| 缓存 | 高频读取 | Redis | 毫秒响应、数据结构丰富 |
| 搜索 | 全文检索 | Elasticsearch | 倒排索引、聚合分析 |
| 时序 | 监控/IoT | ClickHouse/TimescaleDB | 高写入、压缩存储 |
| 图数据库 | 关系网络 | Neo4j | 多跳查询、路径分析 |

### 分库分表策略

```
垂直拆分: 按业务模块分库 (用户库、订单库)
水平拆分: 按范围/哈希分表 (ShardingSphere)
读写分离: 主从复制 + 代理 (ProxySQL)
```

## API 设计规范

### RESTful 设计

```
GET    /api/v1/users              # 列表
POST   /api/v1/users              # 创建
GET    /api/v1/users/:id          # 详情
PUT    /api/v1/users/:id          # 全量更新
PATCH  /api/v1/users/:id          # 部分更新
DELETE /api/v1/users/:id          # 删除

# 关联资源
GET    /api/v1/users/:id/orders   # 用户订单列表

# 批量操作
POST   /api/v1/users/batch        # 批量创建
DELETE /api/v1/users/batch        # 批量删除
```

### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "request_id": "abc123"
  }
}
```

### 错误响应

```json
{
  "code": 40001,
  "message": "Validation failed",
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

## 云原生部署架构

### K8s 部署结构

```yaml
Ingress (Nginx/Traefik)
    │
    ├── Frontend (Deployment + HPA)
    │       ├── ConfigMap (环境配置)
    │       └── Service (ClusterIP)
    │
    ├── Backend Services (Deployment + HPA)
    │       ├── Secrets (敏感配置)
    │       ├── Service (ClusterIP)
    │       └── PodDisruptionBudget
    │
    ├── StatefulSet (数据库/中间件)
    │       ├── PVC (持久卷)
    │       └── Headless Service
    │
    └── CronJob (定时任务)
```

### 高可用设计

```
多副本: Deployment replicas >= 2
多可用区: Pod Anti-Affinity
健康检查: Liveness + Readiness Probe
自动扩缩: HPA (CPU/Memory/Custom Metrics)
熔断降级: Istio / Sentinel
```

## 监控告警体系

```
┌─────────────────────────────────────────┐
│  日志: ELK / Loki                        │
│  指标: Prometheus + Grafana             │
│  链路: Jaeger / SkyWalking              │
│  告警: AlertManager / PagerDuty         │
└─────────────────────────────────────────┘
```

## 输出规范

架构设计文档应包含：
- C4模型图（Context/Container/Component/Code）
- 技术选型决策记录 (ADR)
- API设计文档 (OpenAPI 3.0)
- 数据库ER图
- 部署架构图
- 容量规划与扩展策略
- 监控告警方案
- 安全设计（认证/授权/加密/审计）
- 灾备方案（RTO/RPO）
