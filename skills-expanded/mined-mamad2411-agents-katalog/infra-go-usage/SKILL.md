---
name: infra-go-usage
description: '使用 infra-go Go 基础设施库在业务项目中搭建服务。覆盖 conf（配置加载）、logger（结构化日志）、orm（MySQL/PostgreSQL/SQLite）、redisx（Redis 与分布式锁）、cache（统一缓存：内存/Redis）、httpx（HTTP 服务、参数绑定、统一 Response[T] 响应、中间件：熔断/超时/限流/加密/降载）、jwt（认证中间件）、ratelimit（内存/Redis 限流）、breaker（熔断器）、retry（重试）、taskq（异步任务队列）、storage（OSS/COS/KODO 对象存储）、websocket（实时通信）、trace（链路追踪）、hash（密码/摘要/加密/HMAC 签名）、cast（类型转换）、stringx（字符串）、syncx（并发原语）、service（ServiceGroup 服务编排）。Use when: 用 Go 写业务服务需要选型/初始化/组装 infra-go 模块，需要把 conf+logger+orm+redisx+httpx+jwt 组合起来，或需要统一响应、中间件、优雅关闭等基础设施。'
---

# infra-go 使用指南

指导如何在业务项目中正确使用 `github.com/chihqiang/infra-go` 的各模块，包括模块选型、初始化顺序、组装方式与验收标准。适用于：新建一个 Go 业务服务，或给现有服务接入某个基础设施能力。

## When to Use

- 新建 Go 业务服务，需要搭建配置、日志、数据库、Redis、HTTP 等基础设施
- 需要决定某个需求该用哪个 infra-go 模块（见决策表）
- 需要把多个模块（如 conf + orm + httpx + jwt）正确组装在一起
- 需要按项目约定处理错误、上下文与统一响应

## Module Decision Table（选型决策）

| 需求 | 模块 | 关键入口 |
|------|------|----------|
| 加载 JSON/YAML 配置、默认值、环境变量 | `conf` | `conf.MustLoad` |
| 结构化 / 轮转日志 | `logger` | 包级 `logger.Info` 或 `logger.New` |
| 数据库 CRUD（MySQL/Postgres/SQLite） | `orm` | `orm.MustNew` |
| Redis 缓存 / 分布式锁 | `redisx` | `redisx.MustNew` |
| 进程内内存缓存（热点数据） | `cache` | `cache.NewMemCache` |
| 分布式缓存（跨实例共享） | `cache` | `cache.NewRedisCache` |
| HTTP 服务 / 参数绑定 / 统一响应 | `httpx` | `httpx.NewServer` |
| 接口鉴权 | `jwt` | `jwt.MustNew` + `AuthMiddleware` |
| 接口限流 | `ratelimit` | `ratelimit.NewTokenBucket` |
| 下游保护（熔断快速失败） | `breaker` | `breaker.NewBreaker` 或 `breaker.Do`；按路由隔离用 `httpx.WithRouteBreaker` |
| 失败重试 | `retry` | `retry.Do` |
| 异步任务队列 | `taskq` | `taskq.NewProducer` / `NewConsumer` |
| 对象存储（本地文件 / OSS/COS/KODO） | `storage` | `storage.New` |
| WebSocket 实时通信 | `websocket` | `websocket.MustNew` |
| 链路追踪 | `trace` | `trace.StartAgent` |
| 密码 / 摘要哈希 | `hash` | `hash.BcryptHashDefault` |
| 敏感数据加密 / 请求签名 | `hash` | `hash.AESGCMEncrypt` / `hash.HMACSign` |
| 类型安全转换 | `cast` | `cast.To[T]` |
| 字符串工具 | `stringx` | `stringx.RandId` |
| 路径模式匹配（跳过日志 / 忽略追踪等） | `match` | `match.NewPathMatcher` |
| 响应状态码 / 字节数记录（包装 ResponseWriter） | `respw` | `respw.NewRecorderWriter` |
| 响应超时丢弃 / 加密缓冲（包装 ResponseWriter） | `respw` | `respw.NewTimeoutWriter` · `respw.NewCryptionWriter` |
| 并发原语 | `syncx` | `syncx.NewSingleFlight` |
| 并发启停多个服务 | `service` | `service.NewServiceGroup` |

**分支逻辑（决策点）**：

- 单机部署限流 → 内存限流器（`NewTokenBucket`）；多实例共享限流 → Redis 限流器（`NewRedisTokenBucket`）
- 短期临时数据（缓存/会话/计数器）→ `redisx`；需要可靠持久化与事务 → `orm`
- 接口需实时返回 → `httpx`（必要时 + `websocket`）；允许异步消费 → `taskq`
- 需要互斥保护临界区 → `redisx.Locker`（跨实例）或 `syncx`（单进程）
- 一次请求内需要防缓存击穿/重复执行 → `syncx.NewSingleFlight`
- 文件上传/下载统一接口 → `storage`（Driver 决定 local/OSS/COS/KODO）

## Workflow（完整工作流）

### Step 1 — 需求分析：确定所需模块

1. 列出服务的全部基础设施需求（配置、日志、存储、HTTP、鉴权、限流、重试、队列、实时通信…）
2. 用上面的决策表为每项需求选择一个模块
3. 记录模块间的先后依赖（如 jwt 中间件依赖 conf 提供的 Secret；ServiceGroup 依赖各服务的启动/停止）
4. 按推荐的业务目录结构搭建骨架（config / svc / route / handler / logic / model / middleware），见 [project-structure](./references/project-structure.md)

### Step 2 — 引入依赖

```bash
go get github.com/chihqiang/infra-go/conf
go get github.com/chihqiang/infra-go/logger
go get github.com/chihqiang/infra-go/orm
# ...按需引入，只引入实际用到的模块
```

模块间零强制依赖，按需 import。

### Step 3 — 用 conf 定义并加载配置

1. 定义 Config 结构体，用 `json` 标签声明字段名、默认值与校验指令：

```go
type Config struct {
    Host    string `json:",default=0.0.0.0"`
    Port    int    `json:",default=8080,range=[1:65535]"`
    LogMode string `json:",options=[file,console]"`
    Verbose bool   `json:",optional"`
}
```

2. 启动阶段加载（出错即 panic）：

```go
var cfg Config
conf.MustLoad("config.yaml", &cfg, conf.UseEnv())
```

3. 标签指令速查：`default=...` 默认值；`range=[a:b]` 数值范围；`options=[a,b]` 枚举；`optional` 可选字段；`env=VAR` 优先环境变量；配置内可用 `${VAR}` 引用环境变量（配合 `conf.UseEnv()`）。

### Step 4 — 按依赖顺序初始化组件

遵循每个模块 `New` 返回 error、`MustNew` 出错 panic 的约定：

```go
// 1. 日志（全局可用，最先初始化）
logger.New(logger.Config{Level: logger.InfoLevel, AppName: "my-service"})
defer logger.Sync()

// 2. 数据库
db := orm.MustNew(orm.Config{Driver: orm.DriverMySQL, Host: cfg.Host, ...})
defer orm.Close(db)

// 3. Redis
client := redisx.MustNew(redisx.Config{Addr: cfg.RedisAddr, KeyPrefix: "myapp"})
defer client.Close()

// 4. JWT（供中间件使用）
j := jwt.MustNew(jwt.Config{Secret: cfg.JWTSecret, ...})
```

约定：

- 全局单例 / 服务级组件用 `MustXxx`（启动期失败即 panic，快速失败）
- 可恢复的局部对象用 `Xxx` 并显式处理 error
- 所有持有连接或后台 goroutine 的组件都要 `defer Close / Stop / Sync`

### Step 5 — 用 httpx 组装 HTTP 服务与中间件

1. 定义请求结构体，用 `binding` 标签做校验：

```go
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}
```

2. 注册路由，用 `MustBind*` 一步完成绑定 + 校验 + 自动错误响应：

```go
server.AddRoute(httpx.Route{
    Method: "POST",
    Path:   "/users",
    Handler: func(w http.ResponseWriter, r *http.Request) {
        var req CreateUserRequest
        if err := httpx.MustBindJSON(w, r, &req); err != nil {
            return // 已自动写 400
        }
        user := createUser(req)
        httpx.OkJSON(w, user) // 自动包成 Response[T]，code=0, msg=ok
    },
})
```

3. 挂中间件（鉴权、请求 ID、恢复、CORS、限流等）：

```go
server.Use(httpx.WithRecovery())
server.Use(httpx.WithRequestID())
server.Use(httpx.WithCors("*"))
server.Use(j.AuthMiddleware(func(r *http.Request) string {
    return r.Header.Get("Authorization")
}))
```

4. 启动（阻塞，支持 SIGINT/SIGTERM/SIGHUP 优雅关闭）：

```go
server.Start()
```

### Step 6 — 用 service 编排多个服务的生命周期

把 HTTP 服务、队列消费、后台任务等包装成 `service.Service`，交给 `service.NewServiceGroup` 统一并发启停：

```go
sg := service.NewServiceGroup()
sg.Add(service.WithStart(func() { _ = server.Start() }))
sg.Add(service.WithStart(func() { _ = consumer.Run() }))
sg.Start() // 阻塞，全部退出后返回；Stop 保证只执行一次
```

### Step 7 — 按约定处理错误、上下文与统一响应

- 错误信息用英文，注释用中文（项目统一风格）
- HTTP 层统一 `httpx.OkJSON(w, data)` / `httpx.OkJSONCtx(ctx, w, data)` / `httpx.WriteHTTPError(w, status, msg)` / `httpx.WriteHTTPErrorWithCode(w, status, code, msg)`
- 需要关联 traceID / requestID 时用 `Ctx` 系列响应与 `logger.XxxCtx(ctx, ...)`
- 跨模块统一用 `context.Context` 传递（orm / redisx / retry / taskq 均支持 ctx 超时与取消）
- 语义化错误用 `errors.Is` 判断：`redisx.ErrNil`、`jwt.ErrExpiredToken`、`retry.ErrMaxRetries` 等

## Acceptance Criteria（验收清单）

- [ ] 只引入了实际使用的模块
- [ ] 配置通过 `conf` 加载，含默认值与环境变量支持；敏感信息走环境变量
- [ ] 所有组件按依赖顺序初始化；连接类组件有 `Close / Stop / Sync`
- [ ] HTTP 路由用 `MustBind*` 处理参数；响应统一走 `httpx.Ok*` / `WriteHTTPError`
- [ ] 鉴权 / 限流 / 请求 ID / 恢复以中间件形式挂在 httpx 上
- [ ] 多服务用 `service.NewServiceGroup` 统一启停，支持优雅关闭
- [ ] 错误信息为英文、注释为中文，符合项目风格
- [ ] 涉及网络 / 临时性失败处使用了 `retry`；多实例场景用了 Redis 限流 / 锁
- [ ] `go build ./...` 与 `go vet ./...` 通过

## References

各模块 API 文档统一维护在 `references/` 目录（按模块划分文件），覆盖安装、配置、初始化、关键方法与错误约定，按功能分组：

| 类别 | 模块文档 |
|------|------|
| 配置与日志 | [conf](./references/conf.md) · [logger](./references/logger.md) |
| 数据层 | [orm](./references/orm.md) · [redisx](./references/redisx.md) · [cache](./references/cache.md) |
| HTTP 与接口 | [httpx](./references/httpx.md) · [jwt](./references/jwt.md) · [ratelimit](./references/ratelimit.md) · [breaker](./references/breaker.md) · [retry](./references/retry.md) · [websocket](./references/websocket.md) |
| 异步与存储 | [taskq](./references/taskq.md) · [storage](./references/storage.md) |
| 观测与安全 | [trace](./references/trace.md) · [hash](./references/hash.md) |
| 通用工具 | [cast](./references/cast.md) · [stringx](./references/stringx.md) · [syncx](./references/syncx.md) · [match](./references/match.md) · [respw](./references/respw.md) |
| 服务编排 | [service](./references/service.md) · [mapping](./references/mapping.md) |
| 工程结构 | [project-structure](./references/project-structure.md) |

所有模块遵循统一约定：`New` 返回 error、`MustNew` 出错 panic；连接类组件有 `Close / Stop / Sync`；注释中文、错误英文。
