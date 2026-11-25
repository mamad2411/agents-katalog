---
name: golang-dev
description: Go 开发规范与最佳实践，涵盖项目结构、错误处理、并发模式、接口设计、Web 框架、单元测试
version: "1.0"
---

# Go 开发规范

## 概述

本 Skill 指导 Go 项目的开发规范与最佳实践，包括项目结构、错误处理、并发模式、接口设计、Web 框架使用和测试。

适用场景：
- 新建 Go 微服务项目
- 设计并发安全的业务逻辑
- gin/echo Web 框架最佳实践
- 编写 table-driven 单元测试
- 错误处理与 wrap 策略

---

## 项目结构

### 标准布局（适合中大型服务）

```
my-service/
├── cmd/                      # 入口程序
│   └── server/
│       └── main.go           # main 函数，只做组装和启动
├── internal/                 # 私有代码（外部不可导入）
│   ├── config/               # 配置加载
│   │   └── config.go
│   ├── domain/               # 领域层（核心业务逻辑）
│   │   ├── model/            # 领域模型
│   │   │   └── user.go
│   │   ├── repository/       # 仓储接口
│   │   │   └── user.go
│   │   └── service/          # 领域服务
│   │       └── user.go
│   ├── handler/              # HTTP 处理器（接口层）
│   │   └── user.go
│   ├── middleware/            # 中间件
│   │   ├── auth.go
│   │   └── logger.go
│   └── infra/                # 基础设施（数据库、缓存等实现）
│       ├── mysql/
│       │   └── user_repo.go
│       └── redis/
│           └── cache.go
├── pkg/                      # 可导出的公共库
│   ├── errcode/              # 错误码定义
│   │   └── errcode.go
│   └── response/             # 统一响应
│       └── response.go
├── api/                      # API 定义（OpenAPI、protobuf）
│   └── openapi.yaml
├── scripts/                  # 构建、部署脚本
├── go.mod
├── go.sum
└── Makefile
```

### 关键原则

```go
// cmd/server/main.go — 只做组装，不写业务逻辑
package main

import (
    "context"
    "log"
    "my-service/internal/config"
    "my-service/internal/handler"
    "my-service/internal/infra/mysql"
    "my-service/internal/domain/service"
)

func main() {
    // 1. 加载配置
    cfg := config.MustLoad()

    // 2. 初始化基础设施
    db := mysql.MustConnect(cfg.Database)
    defer db.Close()

    // 3. 组装依赖（手动注入，无需 DI 框架）
    userRepo := mysql.NewUserRepository(db)
    userSvc := service.NewUserService(userRepo)
    userHandler := handler.NewUserHandler(userSvc)

    // 4. 启动服务
    router := setupRouter(userHandler)
    if err := router.Run(cfg.Server.Addr); err != nil {
        log.Fatalf("服务启动失败: %v", err)
    }
}
```

---

## 错误处理

### 基本原则

```go
// 1. 永远检查错误，永远不要用 _ 忽略错误
result, err := doSomething()
if err != nil {
    return fmt.Errorf("执行操作失败: %w", err)  // 用 %w 包装错误
}

// 2. 错误只处理一次 — 要么返回，要么记日志，不要两者都做
// 错误示范:
if err != nil {
    log.Error("失败", err)  // 记了日志
    return err               // 又返回了 — 上层可能再记一次
}

// 正确做法: 底层返回，顶层记日志
```

### sentinel errors 与自定义错误

```go
// pkg/errcode/errcode.go
package errcode

import "errors"

// 哨兵错误 — 用于 errors.Is 判断
var (
    ErrNotFound     = errors.New("资源不存在")
    ErrUnauthorized = errors.New("未授权")
    ErrForbidden    = errors.New("无权限")
    ErrDuplicate    = errors.New("资源已存在")
)

// 业务错误 — 携带错误码和消息
type BizError struct {
    Code    string // 业务错误码，如 "USER_NOT_FOUND"
    Message string // 面向用户的错误消息
    Err     error  // 原始错误（可选）
}

func (e *BizError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("[%s] %s: %v", e.Code, e.Message, e.Err)
    }
    return fmt.Sprintf("[%s] %s", e.Code, e.Message)
}

func (e *BizError) Unwrap() error {
    return e.Err
}

// 构造函数
func NewBizError(code, message string) *BizError {
    return &BizError{Code: code, Message: message}
}

func WrapBizError(code, message string, err error) *BizError {
    return &BizError{Code: code, Message: message, Err: err}
}
```

### errors.Is 与 errors.As

```go
// errors.Is — 判断错误链中是否包含特定错误
if errors.Is(err, errcode.ErrNotFound) {
    // 返回 404
    c.JSON(http.StatusNotFound, response.Fail("资源不存在"))
    return
}

// errors.As — 提取错误链中的特定类型
var bizErr *errcode.BizError
if errors.As(err, &bizErr) {
    // 提取业务错误码，返回给前端
    c.JSON(http.StatusBadRequest, response.FailWithCode(bizErr.Code, bizErr.Message))
    return
}

// 兜底 — 未知错误
log.Errorf("未处理错误: %+v", err)
c.JSON(http.StatusInternalServerError, response.Fail("服务器内部错误"))
```

---

## 并发模式

### goroutine + WaitGroup（并行执行，等待全部完成）

```go
func fetchAllUserData(ctx context.Context, userID int64) (*UserFullData, error) {
    var (
        profile  *Profile
        orders   []*Order
        balance  *Balance
        mu       sync.Mutex   // 保护共享变量
        wg       sync.WaitGroup
        firstErr error
    )

    // 并发请求三个服务
    wg.Add(3)

    go func() {
        defer wg.Done()
        p, err := fetchProfile(ctx, userID)
        mu.Lock()
        defer mu.Unlock()
        if err != nil && firstErr == nil {
            firstErr = fmt.Errorf("获取用户资料失败: %w", err)
            return
        }
        profile = p
    }()

    go func() {
        defer wg.Done()
        o, err := fetchOrders(ctx, userID)
        mu.Lock()
        defer mu.Unlock()
        if err != nil && firstErr == nil {
            firstErr = fmt.Errorf("获取订单列表失败: %w", err)
            return
        }
        orders = o
    }()

    go func() {
        defer wg.Done()
        b, err := fetchBalance(ctx, userID)
        mu.Lock()
        defer mu.Unlock()
        if err != nil && firstErr == nil {
            firstErr = fmt.Errorf("获取余额失败: %w", err)
            return
        }
        balance = b
    }()

    wg.Wait()

    if firstErr != nil {
        return nil, firstErr
    }
    return &UserFullData{Profile: profile, Orders: orders, Balance: balance}, nil
}
```

### errgroup（推荐，更优雅的并发错误处理）

```go
import "golang.org/x/sync/errgroup"

func fetchAllUserData(ctx context.Context, userID int64) (*UserFullData, error) {
    var (
        profile *Profile
        orders  []*Order
        balance *Balance
    )

    g, ctx := errgroup.WithContext(ctx)

    g.Go(func() error {
        var err error
        profile, err = fetchProfile(ctx, userID)
        return err
    })

    g.Go(func() error {
        var err error
        orders, err = fetchOrders(ctx, userID)
        return err
    })

    g.Go(func() error {
        var err error
        balance, err = fetchBalance(ctx, userID)
        return err
    })

    // 任一 goroutine 返回错误，ctx 会被取消，其他 goroutine 应感知并退出
    if err := g.Wait(); err != nil {
        return nil, fmt.Errorf("获取用户完整数据失败: %w", err)
    }

    return &UserFullData{Profile: profile, Orders: orders, Balance: balance}, nil
}
```

### channel 模式（生产者-消费者）

```go
// 扇出-扇入模式：多个 worker 并行处理任务
func processOrders(ctx context.Context, orderIDs []int64) error {
    const workerCount = 5
    jobs := make(chan int64, len(orderIDs))  // 任务队列
    errs := make(chan error, workerCount)     // 错误收集

    // 启动 worker
    var wg sync.WaitGroup
    for i := 0; i < workerCount; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for orderID := range jobs {
                if err := processOneOrder(ctx, orderID); err != nil {
                    errs <- fmt.Errorf("处理订单 %d 失败: %w", orderID, err)
                    return
                }
            }
        }()
    }

    // 发送任务
    for _, id := range orderIDs {
        jobs <- id
    }
    close(jobs)

    // 等待所有 worker 完成，然后关闭错误 channel
    go func() {
        wg.Wait()
        close(errs)
    }()

    // 收集错误
    for err := range errs {
        return err  // 返回第一个错误
    }
    return nil
}
```

### context 超时与取消

```go
func callExternalService(ctx context.Context, req *Request) (*Response, error) {
    // 设置单次调用超时（不影响父 context）
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    // 使用 select 监听 context 取消信号
    resultCh := make(chan *Response, 1)
    errCh := make(chan error, 1)

    go func() {
        resp, err := doHTTPCall(ctx, req)
        if err != nil {
            errCh <- err
            return
        }
        resultCh <- resp
    }()

    select {
    case <-ctx.Done():
        return nil, fmt.Errorf("调用外部服务超时: %w", ctx.Err())
    case err := <-errCh:
        return nil, err
    case resp := <-resultCh:
        return resp, nil
    }
}
```

---

## 接口设计

### 小接口原则

```go
// 接口应该小而精 — Go 推崇一两个方法的接口
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// 通过组合构建更大的接口
type ReadWriter interface {
    Reader
    Writer
}

// 仓储接口 — 按需定义，不要一个大接口包含所有方法
type UserReader interface {
    FindByID(ctx context.Context, id int64) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
}

type UserWriter interface {
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
}

// 需要读写时组合
type UserRepository interface {
    UserReader
    UserWriter
}
```

### 面向接口编程 — 接口在消费方定义

```go
// 在使用方定义接口（而非实现方），这是 Go 的惯用做法
// internal/domain/service/user.go

// UserRepo — 领域服务只依赖抽象接口
type UserRepo interface {
    FindByID(ctx context.Context, id int64) (*model.User, error)
    Save(ctx context.Context, user *model.User) error
}

type UserService struct {
    repo UserRepo  // 依赖接口，不依赖具体实现
}

func NewUserService(repo UserRepo) *UserService {
    return &UserService{repo: repo}
}

func (s *UserService) GetUser(ctx context.Context, id int64) (*model.User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("获取用户失败: %w", err)
    }
    if user == nil {
        return nil, errcode.ErrNotFound
    }
    return user, nil
}
```

---

## gin Web 框架最佳实践

### 路由与 Handler

```go
// internal/handler/user.go
type UserHandler struct {
    userSvc *service.UserService
}

func NewUserHandler(svc *service.UserService) *UserHandler {
    return &UserHandler{userSvc: svc}
}

// RegisterRoutes 注册路由 — 路由定义集中管理
func (h *UserHandler) RegisterRoutes(r *gin.RouterGroup) {
    users := r.Group("/users")
    {
        users.POST("", h.Create)
        users.GET("/:id", h.GetByID)
        users.PUT("/:id", h.Update)
        users.DELETE("/:id", h.Delete)
    }
}

// Create 创建用户
func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        response.BadRequest(c, "参数格式错误")
        return
    }

    // 参数校验
    if err := req.Validate(); err != nil {
        response.BadRequest(c, err.Error())
        return
    }

    user, err := h.userSvc.CreateUser(c.Request.Context(), &req)
    if err != nil {
        handleError(c, err)  // 统一错误处理
        return
    }

    response.Created(c, toUserVO(user))
}
```

### 统一响应格式

```go
// pkg/response/response.go
package response

import "github.com/gin-gonic/gin"

type Result struct {
    Code    int         `json:"code"`    // 业务状态码，0 表示成功
    Message string      `json:"message"` // 提示信息
    Data    interface{} `json:"data"`    // 响应数据
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, Result{Code: 0, Message: "success", Data: data})
}

func Created(c *gin.Context, data interface{}) {
    c.JSON(http.StatusCreated, Result{Code: 0, Message: "success", Data: data})
}

func BadRequest(c *gin.Context, msg string) {
    c.JSON(http.StatusBadRequest, Result{Code: 400, Message: msg})
}

func Fail(msg string) Result {
    return Result{Code: -1, Message: msg}
}

func FailWithCode(code string, msg string) Result {
    return Result{Code: -1, Message: msg, Data: map[string]string{"error_code": code}}
}
```

### 中间件

```go
// internal/middleware/logger.go — 请求日志中间件
func RequestLogger(logger *slog.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path

        c.Next()  // 执行后续 handler

        logger.Info("请求处理完成",
            slog.String("method", c.Request.Method),
            slog.String("path", path),
            slog.Int("status", c.Writer.Status()),
            slog.Duration("latency", time.Since(start)),
            slog.String("client_ip", c.ClientIP()),
        )
    }
}

// internal/middleware/auth.go — JWT 认证中间件
func JWTAuth(secret string) gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            response.Unauthorized(c, "缺少认证令牌")
            c.Abort()
            return
        }

        claims, err := parseJWT(token, secret)
        if err != nil {
            response.Unauthorized(c, "认证令牌无效")
            c.Abort()
            return
        }

        // 将用户信息存入 context
        c.Set("user_id", claims.UserID)
        c.Next()
    }
}
```

---

## 单元测试（table-driven tests）

### 基本模式

```go
// internal/domain/service/user_test.go
func TestUserService_GetUser(t *testing.T) {
    tests := []struct {
        name      string        // 测试用例名称
        userID    int64         // 输入参数
        mockSetup func(*MockUserRepo)  // Mock 配置
        want      *model.User   // 期望返回值
        wantErr   error         // 期望错误
    }{
        {
            name:   "正常获取用户",
            userID: 1,
            mockSetup: func(m *MockUserRepo) {
                m.On("FindByID", mock.Anything, int64(1)).
                    Return(&model.User{ID: 1, Name: "张三"}, nil)
            },
            want:    &model.User{ID: 1, Name: "张三"},
            wantErr: nil,
        },
        {
            name:   "用户不存在",
            userID: 999,
            mockSetup: func(m *MockUserRepo) {
                m.On("FindByID", mock.Anything, int64(999)).
                    Return(nil, nil)
            },
            want:    nil,
            wantErr: errcode.ErrNotFound,
        },
        {
            name:   "数据库错误",
            userID: 1,
            mockSetup: func(m *MockUserRepo) {
                m.On("FindByID", mock.Anything, int64(1)).
                    Return(nil, errors.New("连接超时"))
            },
            want:    nil,
            wantErr: errors.New("获取用户失败"),  // 包装后的错误
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // 准备 Mock
            mockRepo := new(MockUserRepo)
            tt.mockSetup(mockRepo)

            // 创建被测服务
            svc := service.NewUserService(mockRepo)

            // 执行
            got, err := svc.GetUser(context.Background(), tt.userID)

            // 断言
            if tt.wantErr != nil {
                assert.Error(t, err)
                assert.ErrorContains(t, err, tt.wantErr.Error())
                assert.Nil(t, got)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.want, got)
            }

            mockRepo.AssertExpectations(t)
        })
    }
}
```

### HTTP Handler 测试

```go
func TestUserHandler_Create(t *testing.T) {
    tests := []struct {
        name       string
        body       string                   // 请求体 JSON
        mockSetup  func(*MockUserService)
        wantStatus int                      // 期望 HTTP 状态码
        wantCode   int                      // 期望业务码
    }{
        {
            name: "创建成功",
            body: `{"username":"zhangsan","email":"zhang@example.com"}`,
            mockSetup: func(m *MockUserService) {
                m.On("CreateUser", mock.Anything, mock.Anything).
                    Return(&model.User{ID: 1, Name: "zhangsan"}, nil)
            },
            wantStatus: http.StatusCreated,
            wantCode:   0,
        },
        {
            name:       "参数格式错误",
            body:       `invalid json`,
            mockSetup:  func(m *MockUserService) {},
            wantStatus: http.StatusBadRequest,
            wantCode:   400,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // 准备
            mockSvc := new(MockUserService)
            tt.mockSetup(mockSvc)
            h := handler.NewUserHandler(mockSvc)

            // 构建请求
            w := httptest.NewRecorder()
            c, _ := gin.CreateTestContext(w)
            c.Request = httptest.NewRequest("POST", "/users",
                strings.NewReader(tt.body))
            c.Request.Header.Set("Content-Type", "application/json")

            // 执行
            h.Create(c)

            // 断言
            assert.Equal(t, tt.wantStatus, w.Code)

            var resp response.Result
            err := json.Unmarshal(w.Body.Bytes(), &resp)
            assert.NoError(t, err)
            assert.Equal(t, tt.wantCode, resp.Code)
        })
    }
}
```

### 测试辅助工具

```go
// 使用 testify 断言
import "github.com/stretchr/testify/assert"
import "github.com/stretchr/testify/require"  // 失败立即终止

// 使用 testcontainers 做集成测试
import "github.com/testcontainers/testcontainers-go"

func setupMySQL(t *testing.T) *sql.DB {
    t.Helper()
    ctx := context.Background()
    container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "mysql:8.0",
            ExposedPorts: []string{"3306/tcp"},
            Env: map[string]string{
                "MYSQL_ROOT_PASSWORD": "test",
                "MYSQL_DATABASE":      "testdb",
            },
        },
        Started: true,
    })
    require.NoError(t, err)
    t.Cleanup(func() { container.Terminate(ctx) })

    // 获取连接地址并返回 *sql.DB
    ...
}
```

---

## 编码规范速查

| 规则 | 说明 |
|------|------|
| 命名 | 包名小写单词、变量 camelCase、导出类型 PascalCase、接口不加 I 前缀 |
| 错误处理 | 永远检查 error，用 `%w` 包装，不要 `_` 忽略 |
| context | 第一个参数始终是 `ctx context.Context`，不要存储到 struct |
| goroutine | 必须可控退出（通过 context 或 done channel），防止泄漏 |
| 接口 | 在消费方定义，保持小接口（1-3 个方法） |
| 零值可用 | 设计 struct 使零值有合理的默认行为 |
| defer | 资源释放用 defer，确保 Close/Unlock 不遗漏 |
| 日志 | 使用 slog（Go 1.21+），结构化日志替代 fmt.Printf |
| lint | 使用 golangci-lint，配置 .golangci.yml |
