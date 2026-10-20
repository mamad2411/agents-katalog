---
description: Go Uber 工程规范，基于 golang.mdc，新增 fx 依赖注入、12-Factor 结构设计、Makefile 构建管理及 CI/CD 友好约束
globs: ["**/*.go", "**/go.mod", "**/go.sum", "**/Makefile"]
alwaysApply: false
---

# Go Uber 工程规范

> 本规范在 [golang.mdc](golang.mdc) 基础上新增工程化约束，适用于生产级 Go 服务。

## 约束一：依赖注入使用 go.uber.org/fx

- 所有服务依赖通过 `go.uber.org/fx` 进行声明式依赖注入，禁止使用全局变量传递依赖
- 每个组件提供 `Module` 变量，聚合本包所有 `fx.Provide` / `fx.Invoke`
- 构造函数使用 `fx.Annotate` 或具名返回值解决同类型多实例冲突
- 使用 `fx.Lifecycle` 管理组件启动与关闭，确保资源有序释放
- 使用 `fx.In` / `fx.Out` 嵌入结构体处理多依赖场景，提升可读性

```go
// internal/user/module.go
package user

import "go.uber.org/fx"

var Module = fx.Module("user",
    fx.Provide(NewRepository),
    fx.Provide(NewService),
    fx.Provide(NewHandler),
)

// internal/user/service.go
type ServiceParams struct {
    fx.In

    Repo   Repository
    Cache  Cache
    Logger *zap.Logger
}

func NewService(p ServiceParams) *Service {
    return &Service{
        repo:   p.Repo,
        cache:  p.Cache,
        logger: p.Logger,
    }
}

// cmd/server/main.go
func main() {
    app := fx.New(
        fx.Provide(config.New),
        fx.Provide(logger.New),
        fx.Provide(database.New),
        user.Module,
        order.Module,
        fx.Invoke(registerRoutes),
    )
    app.Run()
}

// 使用 fx.Lifecycle 管理资源生命周期
func NewHTTPServer(lc fx.Lifecycle, cfg *Config, logger *zap.Logger) *http.Server {
    srv := &http.Server{Addr: cfg.Addr}
    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            go srv.ListenAndServe()
            logger.Info("http server started", zap.String("addr", cfg.Addr))
            return nil
        },
        OnStop: func(ctx context.Context) error {
            return srv.Shutdown(ctx)
        },
    })
    return srv
}
```

## 约束二：结构设计遵循 12-Factor 应用方法论

遵循 [12-Factor App](https://12factor.net/) 方法论设计服务结构：

### Factor I - 基准代码（Codebase）

- 一个代码库，多环境部署，通过配置区分环境，禁止为不同环境维护不同分支

### Factor II - 依赖（Dependencies）

- 通过 `go.mod` / `go.sum` 显式声明并隔离所有依赖，禁止依赖系统级工具

### Factor III - 配置（Config）

- 使用 `github.com/spf13/viper` 统一管理配置，支持配置文件、环境变量及命令行参数，优先级从高到低：环境变量 > 配置文件 > 默认值
- 配置文件优先从 `configs/` 目录加载，支持同时加载多个配置文件（如基础配置 + 环境特定配置），后加载的文件覆盖前者
- 配置文件格式推荐 YAML，文件名规范：`configs/config.yaml`（基础）+ `configs/config.<env>.yaml`（环境覆盖）
- 所有敏感配置（密码、密钥）必须通过环境变量注入，不得写入配置文件
- 配置结构体通过 fx 注入，所有组件从配置结构体读取参数，禁止直接调用 `viper.Get*`

```go
// configs/config.yaml（基础配置）
http:
  addr: ":8080"
  read_timeout: "30s"
  write_timeout: "30s"

log:
  level: "info"

database:
  max_open_conns: 25
  max_idle_conns: 5
  conn_max_lifetime: "5m"

// configs/config.local.yaml（本地开发覆盖，加入 .gitignore）
http:
  addr: ":3000"
log:
  level: "debug"
```

```go
// internal/config/config.go
package config

import (
    "fmt"
    "strings"

    "github.com/spf13/viper"
)

type Config struct {
    HTTP     HTTPConfig     `mapstructure:"http"`
    Log      LogConfig      `mapstructure:"log"`
    Database DatabaseConfig `mapstructure:"database"`
}

type HTTPConfig struct {
    Addr         string        `mapstructure:"addr"`
    ReadTimeout  time.Duration `mapstructure:"read_timeout"`
    WriteTimeout time.Duration `mapstructure:"write_timeout"`
}

type LogConfig struct {
    Level string `mapstructure:"level"`
}

type DatabaseConfig struct {
    DSN             string        `mapstructure:"dsn"`
    MaxOpenConns    int           `mapstructure:"max_open_conns"`
    MaxIdleConns    int           `mapstructure:"max_idle_conns"`
    ConnMaxLifetime time.Duration `mapstructure:"conn_max_lifetime"`
}

// New 加载配置：优先读取 configs/ 目录下的配置文件，支持多文件叠加
// 加载顺序：configs/config.yaml → configs/config.<APP_ENV>.yaml
// 环境变量自动覆盖同名配置（下划线分隔，自动大写）
func New() (*Config, error) {
    v := viper.New()

    // 基础默认值
    v.SetDefault("http.addr", ":8080")
    v.SetDefault("http.read_timeout", "30s")
    v.SetDefault("http.write_timeout", "30s")
    v.SetDefault("log.level", "info")

    // 优先从 configs/ 目录加载基础配置文件
    v.SetConfigName("config")
    v.SetConfigType("yaml")
    v.AddConfigPath("configs/")
    v.AddConfigPath(".")

    if err := v.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            return nil, fmt.Errorf("read config file: %w", err)
        }
    }

    // 加载环境特定配置文件（如 configs/config.production.yaml），合并覆盖
    env := strings.ToLower(v.GetString("APP_ENV"))
    if env == "" {
        env = strings.ToLower(getEnv("APP_ENV", "local"))
    }
    v.SetConfigName("config." + env)
    if err := v.MergeInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            return nil, fmt.Errorf("merge %s config: %w", env, err)
        }
    }

    // 环境变量自动绑定（ENV_VAR 映射 config key，如 HTTP_ADDR → http.addr）
    v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
    v.AutomaticEnv()

    cfg := &Config{}
    if err := v.Unmarshal(cfg); err != nil {
        return nil, fmt.Errorf("unmarshal config: %w", err)
    }
    return cfg, nil
}

func getEnv(key, defaultVal string) string {
    if val := os.Getenv(key); val != "" {
        return val
    }
    return defaultVal
}
```

### Factor IV - 后端服务（Backing Services）

- 数据库、缓存、消息队列等后端服务均视为外部资源，通过配置中的 URL/DSN 连接
- 不区分本地和第三方服务，均通过依赖注入传递连接

### Factor VI - 进程（Processes）

- 应用以无状态进程运行，不在进程内存中存储会话状态
- 需要持久化的数据必须写入外部存储（数据库、Redis 等）

### Factor VIII - 并发（Concurrency）

- 通过进程类型水平扩展（web 进程、worker 进程分离）
- 使用 `go.uber.org/fx` 的 `Lifecycle` 管理进程内的并发组件

### Factor IX - 易处理（Disposability）

- 快速启动（目标 < 5s），优雅关闭（处理完当前请求后退出）
- 捕获 `SIGINT` / `SIGTERM` 信号，通过 `fx` 的 `OnStop` 钩子释放资源

```go
// fx 自动处理 SIGINT/SIGTERM，触发所有 OnStop 钩子
app := fx.New(
    // ...
    fx.WithLogger(func(log *zap.Logger) fxevent.Logger {
        return &fxevent.ZapLogger{Logger: log}
    }),
)
app.Run() // 阻塞直到收到终止信号，然后有序关闭
```

### Factor XI - 日志（Logs）

- 日志作为事件流输出到 stdout，由平台（Docker/K8s）负责收集
- 使用 `go.uber.org/zap` 输出结构化 JSON 日志，禁止写入本地日志文件

```go
func NewLogger(cfg *Config) (*zap.Logger, error) {
    if cfg.Log.Level == "development" {
        return zap.NewDevelopment()
    }
    zapCfg := zap.NewProductionConfig()
    level, err := zap.ParseAtomicLevel(cfg.Log.Level)
    if err != nil {
        return nil, fmt.Errorf("parse log level: %w", err)
    }
    zapCfg.Level = level
    return zapCfg.Build()
}
```

## 约束三：统一的构建管理使用 Makefile

- 所有构建、测试、lint、代码生成操作均通过 `Makefile` 封装，提供统一入口
- Makefile 中声明 `.PHONY` 目标防止与同名文件冲突
- 所有变量使用 `?=` 支持外部覆盖，CI 可通过环境变量定制行为
- 目标命名使用小写中划线风格：`build`、`test`、`lint`、`docker-build`

```makefile
# Makefile

APP_NAME    ?= myapp
BUILD_DIR   ?= ./bin
GO          ?= go
GOFLAGS     ?= -trimpath
LDFLAGS     ?= -s -w
VERSION     ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
COMMIT      ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

.PHONY: all build test lint fmt vet clean docker-build docker-push generate tidy

all: lint test build

## 构建二进制
build:
	$(GO) build $(GOFLAGS) \
		-ldflags "$(LDFLAGS) -X main.version=$(VERSION) -X main.commit=$(COMMIT)" \
		-o $(BUILD_DIR)/$(APP_NAME) ./cmd/server

## 运行所有测试（含竞态检测）
test:
	$(GO) test -race -timeout 120s ./...

## 运行测试并生成覆盖率报告
test-coverage:
	$(GO) test -race -coverprofile=coverage.out -covermode=atomic ./...
	$(GO) tool cover -html=coverage.out -o coverage.html

## 代码格式化
fmt:
	gofmt -w -s .
	goimports -w .

## 静态检查
vet:
	$(GO) vet ./...

## lint（依赖 golangci-lint）
lint:
	golangci-lint run ./...

## 代码生成（wire / mockery / protoc 等）
generate:
	$(GO) generate ./...

## 整理依赖
tidy:
	$(GO) mod tidy

## 清理构建产物
clean:
	rm -rf $(BUILD_DIR) coverage.out coverage.html

## 构建 Docker 镜像
docker-build:
	docker build \
		--build-arg VERSION=$(VERSION) \
		--build-arg COMMIT=$(COMMIT) \
		-t $(APP_NAME):$(VERSION) .

## 推送 Docker 镜像
docker-push:
	docker push $(APP_NAME):$(VERSION)
```

## 约束四：CI/CD 友好

### 代码结构要求

- 所有配置均可通过环境变量覆盖，CI 无需修改代码即可运行不同环境
- 测试不依赖本地服务，使用 `testcontainers-go` 或 mock 替代外部依赖
- 构建结果为单一静态二进制，便于容器化部署

### Dockerfile 规范

- 使用多阶段构建，最终镜像基于 `gcr.io/distroless/static` 或 `alpine`
- 构建阶段通过 `go build -trimpath -ldflags "-s -w"` 减小二进制体积
- 不在镜像中保留源码、测试文件、开发工具

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -trimpath -ldflags "-s -w" \
    -o /bin/server ./cmd/server

# Final stage
FROM gcr.io/distroless/static:nonroot
COPY --from=builder /bin/server /server
ENTRYPOINT ["/server"]
```

### GitHub Actions 工作流规范

- 所有 CI 步骤通过 `make` 命令调用，与本地开发体验一致
- 使用缓存加速 Go 模块和构建产物下载
- 拆分为独立 job：lint、test、build，支持并行执行和按需重跑

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - uses: golangci/golangci-lint-action@v6
        with:
          version: latest

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - run: make test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 获取完整 tag 历史，用于 VERSION
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - run: make build
      - uses: actions/upload-artifact@v4
        with:
          name: server-binary
          path: bin/
```

### 健康检查与可观测性

- 提供 `/healthz`（存活）和 `/readyz`（就绪）HTTP 端点供 K8s 探针使用
- 通过 `go.uber.org/fx` 的 `Lifecycle` 在就绪检查中验证所有依赖（数据库连接等）可用
- 暴露 Prometheus `/metrics` 端点，输出 RED 指标（Rate、Errors、Duration）

```go
// internal/health/handler.go
type Handler struct {
    checks []HealthCheck
}

type HealthCheck interface {
    Name() string
    Check(ctx context.Context) error
}

func (h *Handler) Readyz(w http.ResponseWriter, r *http.Request) {
    for _, check := range h.checks {
        if err := check.Check(r.Context()); err != nil {
            http.Error(w, fmt.Sprintf("%s: %v", check.Name(), err), http.StatusServiceUnavailable)
            return
        }
    }
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("ok"))
}
```

## 约束五：默认技术栈选型

在未明确要求的情况下，统一使用以下默认技术栈：

- **HTTP 框架**：`github.com/gin-gonic/gin`
- **ORM**：`gorm.io/gorm` + `gorm.io/driver/mysql`
- **数据库**：MySQL
- **API 文档**：`github.com/swaggo/swag`（swaggo）

### HTTP 框架 - Gin

```go
// internal/server/server.go
func NewHTTPServer(lc fx.Lifecycle, cfg *Config, logger *zap.Logger, h *UserHandler) *gin.Engine {
    r := gin.New()
    r.Use(gin.Recovery())

    v1 := r.Group("/api/v1")
    {
        users := v1.Group("/users")
        users.POST("", h.Create)
        users.GET("/:id", h.Get)
    }

    srv := &http.Server{Addr: cfg.HTTP.Addr, Handler: r}
    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            go srv.ListenAndServe()
            logger.Info("http server started", zap.String("addr", cfg.HTTP.Addr))
            return nil
        },
        OnStop: func(ctx context.Context) error {
            return srv.Shutdown(ctx)
        },
    })
    return r
}
```

### ORM - GORM + MySQL

```go
// internal/database/database.go
func NewDB(cfg *Config, logger *zap.Logger) (*gorm.DB, error) {
    db, err := gorm.Open(mysql.Open(cfg.Database.DSN), &gorm.Config{
        Logger: gormzap.New(logger),
    })
    if err != nil {
        return nil, fmt.Errorf("open database: %w", err)
    }

    sqlDB, _ := db.DB()
    sqlDB.SetMaxOpenConns(cfg.Database.MaxOpenConns)
    sqlDB.SetMaxIdleConns(cfg.Database.MaxIdleConns)
    sqlDB.SetConnMaxLifetime(cfg.Database.ConnMaxLifetime)

    return db, nil
}
```

### API 文档 - Swagger

- 需要生成 API 文档时，所有 HTTP API 处理函数**必须**添加 Swagger 注释
- 在 `cmd/<app>/main.go` 中引入 `_ "your-module/docs"` 并注册 `/swagger/*any` 路由
- 注释字段：`@Summary`、`@Description`、`@Tags`、`@Accept`、`@Produce`、`@Param`、`@Success`、`@Failure`、`@Router`

```go
// CreateOrder godoc
// @Summary 创建订单
// @Description 创建一个新的商城订单
// @Tags mall-orders
// @Accept json
// @Produce json
// @Param order body dto.CreateOrderReq true "订单信息"
// @Success 200 {object} response.Result{data=string} "订单ID"
// @Failure 400 {object} response.Result
// @Router /api/v1/mall/orders [post]
func (h *OrderHandler) CreateOrder(c *gin.Context) {
    var req dto.CreateOrderReq
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, response.Fail(err.Error()))
        return
    }
    id, err := h.svc.CreateOrder(c.Request.Context(), &req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, response.Fail(err.Error()))
        return
    }
    c.JSON(http.StatusOK, response.OK(id))
}
```

## 推荐工具

| 工具 | 用途 |
|------|------|
| `go.uber.org/fx` | 依赖注入框架 |
| `go.uber.org/zap` | 结构化日志 |
| `github.com/spf13/viper` | 配置管理 |
| `github.com/gin-gonic/gin` | HTTP 框架 |
| `gorm.io/gorm` | ORM |
| `gorm.io/driver/mysql` | MySQL 驱动 |
| `github.com/swaggo/swag` | Swagger 文档生成 |
| `golangci-lint` | 静态分析 |
| `testcontainers-go` | 集成测试容器化依赖 |
| `gomock` / `mockery` | Mock 生成 |
| `goreleaser` | 跨平台构建与发布 |
