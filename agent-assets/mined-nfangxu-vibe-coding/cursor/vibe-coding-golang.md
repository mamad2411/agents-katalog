---
description: Go 语言开发规范，适用于所有 Go 项目，遵循 Uber Go 语言编码规范
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
alwaysApply: false
---

# Go 语言开发规范

## 代码风格

- 所有代码必须通过 `gofmt` 格式化，提交前运行 `goimports` 整理导入
- 使用 `golangci-lint` 进行静态检查，遵循 lint 报告中的所有警告
- 行长度建议不超过 120 个字符
- 使用 Tab 缩进，不使用空格

## 命名规范

- 包名使用小写单词，不使用下划线或驼峰：`package userservice`
- 导出的标识符使用 PascalCase：`type UserService struct`
- 未导出的标识符使用 camelCase：`func parseToken()`
- 接口名以行为命名，单方法接口通常以 `-er` 结尾：`type Reader interface`
- 常量使用 PascalCase（导出）或 camelCase（未导出）
- 避免在名称中重复包名：使用 `user.Service` 而非 `user.UserService`
- 错误变量命名以 `Err` 开头：`var ErrNotFound = errors.New("not found")`
- 函数名使用驼峰命名，遵循 Go 惯例（非 `get_user`，而是 `GetUser`）

## 项目结构

```
project/
├── cmd/              # 可执行程序入口
│   └── server/
│       └── main.go
├── internal/         # 私有应用代码（不对外暴露）
│   ├── handler/      # HTTP 处理器
│   ├── service/      # 业务逻辑层
│   ├── repository/   # 数据访问层
│   └── model/        # 数据模型
├── pkg/              # 可被外部使用的公共库
├── api/              # API 定义（protobuf / OpenAPI）
├── configs/          # 配置文件
├── scripts/          # 构建/部署脚本
├── go.mod
└── go.sum
```

## import 分组

按以下顺序分三组组织 import，组间用空行分隔：

1. 标准库
2. 第三方库
3. 项目内部包

```go
import (
    "fmt"
    "os"

    "github.com/gin-gonic/gin"
    "go.uber.org/zap"

    "github.com/yourorg/yourproject/internal/model"
)
```

## 错误处理

- 始终检查并处理错误，不要使用 `_` 忽略关键错误
- 每个错误只处理一次：记录或返回，不要既记录又返回
- 不要使用 `panic`，除非是程序初始化阶段无法恢复的情况
- 错误类型选择：
  - 静态字符串且无需匹配：`errors.New("msg")`
  - 动态字符串且无需匹配：`fmt.Errorf("msg: %v", val)`
  - 需要调用方用 `errors.Is` 匹配：导出顶层 `var ErrXxx = errors.New("...")`
  - 需要调用方用 `errors.As` 匹配：自定义 `error` 类型
- 使用 `fmt.Errorf("context: %w", err)` 包装错误以保留原始错误
- 在顶层统一处理错误并记录日志，底层只负责向上传递
- 使用 `errors.Is` / `errors.As` 进行错误类型判断

```go
// 推荐：包装错误并向上传递
if err := doSomething(); err != nil {
    return fmt.Errorf("doSomething failed: %w", err)
}

// 推荐：静态错误导出，支持 errors.Is 匹配
var ErrNotFound = errors.New("not found")

// 推荐：自定义错误类型，支持 errors.As 匹配
type NotFoundError struct {
    ID string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("resource %s not found", e.ID)
}
```

## 接口设计

- 在使用方定义接口，而非实现方
- 保持接口小而专一（Interface Segregation Principle）
- 优先使用组合而非继承
- 不要使用指向接口的指针，接口本身已是引用类型
- 在编译时验证接口合理性：`var _ http.Handler = (*Handler)(nil)`

```go
// 推荐：小接口，在使用方定义
type UserReader interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

type UserWriter interface {
    CreateUser(ctx context.Context, user *User) error
    UpdateUser(ctx context.Context, user *User) error
}

// 推荐：编译时接口合理性验证
var _ UserReader = (*userService)(nil)
```

## 并发编程

- 使用 `context.Context` 控制 goroutine 生命周期，作为函数第一个参数
- 使用 `sync.WaitGroup` 或 `errgroup` 等待 goroutine 完成
- 使用 channel 进行 goroutine 间通信，使用 mutex 保护共享状态
- 避免 goroutine 泄漏，确保每个 goroutine 都有退出路径
- 不要一劳永逸地启动 goroutine，必须提供停止或等待机制
- 零值 `sync.Mutex` 是有效的，不要使用指向 mutex 的指针；mutex 作为结构体字段时不嵌入，使用具名字段
- Channel 的 size 要么是 1，要么是无缓冲的；不要使用任意大小的 buffered channel
- 在边界处拷贝 Slices 和 Maps，避免外部修改内部状态
- 使用 `defer` 释放锁和资源，确保即使有多个返回路径也能正确释放

```go
// 推荐：mutex 作为具名字段，不嵌入
type SMap struct {
    mu   sync.Mutex
    data map[string]string
}

func (m *SMap) Get(k string) string {
    m.mu.Lock()
    defer m.mu.Unlock()
    return m.data[k]
}

// 推荐：使用 errgroup 管理并发任务
func fetchAll(ctx context.Context, ids []string) ([]*User, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]*User, len(ids))

    for i, id := range ids {
        i, id := i, id // 捕获循环变量（Go 1.22 以前需要）
        g.Go(func() error {
            user, err := fetchUser(ctx, id)
            if err != nil {
                return err
            }
            results[i] = user
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return results, nil
}
```

## 代码规范

- **减少嵌套**：优先处理错误/特殊情况并提前返回，减少正常逻辑的嵌套层级
- **避免不必要的 else**：`if` 块以 `return` 结束时，不需要 `else`
- **枚举从 1 开始**：使用 `iota + 1`，除非零值有明确语义
- **避免 `init()`**：`init()` 难以测试和控制执行顺序，优先使用显式初始化函数
- **避免可变全局变量**：通过构造函数注入依赖，减少全局状态
- **使用字段名初始化结构体**：始终在初始化结构体时指定字段名
- **序列化结构体中使用字段标记**：JSON/YAML 等序列化字段必须使用 struct tag

```go
// 推荐：提前返回，减少嵌套
func process(data []byte) error {
    if len(data) == 0 {
        return errors.New("empty data")
    }
    // 正常处理逻辑
    return nil
}

// 推荐：使用字段名初始化结构体
user := &User{
    ID:   "user-123",
    Name: "Alice",
}

// 推荐：枚举从 1 开始
type Direction int

const (
    North Direction = iota + 1
    South
    East
    West
)

// 推荐：序列化 struct 使用 tag
type Config struct {
    Host string `json:"host" yaml:"host"`
    Port int    `json:"port" yaml:"port"`
}
```

## 时间处理

- 使用 `time.Time` 表达时间点，使用 `time.Duration` 表达时间段
- 不要使用裸 `int` 或 `int64` 传递时间和时长，避免单位混淆
- 与外部系统交互时无法使用 `time.Duration`，在字段名中注明单位（如 `IntervalMillis`）

```go
// 推荐：使用 time.Duration 作为参数类型
func poll(delay time.Duration) {
    time.Sleep(delay)
}
poll(10 * time.Second)

// 推荐：使用 time.Time 进行比较
func isActive(now, start, stop time.Time) bool {
    return (start.Before(now) || start.Equal(now)) && now.Before(stop)
}
```

## 测试规范

- 测试文件以 `_test.go` 结尾，与被测文件放在同一包
- 单元测试函数命名：`TestFunctionName_Scenario_ExpectedResult`
- 使用 `testify` 库进行断言：`assert.Equal(t, expected, actual)`
- 使用表格驱动测试（Table-Driven Tests）
- 使用 `t.Parallel()` 并行运行独立测试
- Mock 使用 `testify/mock` 或 `gomock`

```go
func TestGetUser_ValidID_ReturnsUser(t *testing.T) {
    t.Parallel()

    tests := []struct {
        name    string
        id      string
        want    *User
        wantErr bool
    }{
        {
            name: "valid user id",
            id:   "user-123",
            want: &User{ID: "user-123", Name: "Alice"},
        },
        {
            name:    "empty id returns error",
            id:      "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        tt := tt
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got, err := GetUser(tt.id)
            if tt.wantErr {
                assert.Error(t, err)
                return
            }
            assert.NoError(t, err)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

## 依赖注入

- 通过构造函数注入依赖，避免全局变量
- 使用 `wire` 或手动依赖注入
- 使用功能选项（Functional Options）模式处理可选参数

```go
type UserService struct {
    repo   UserRepository
    cache  Cache
    logger *zap.Logger
}

func NewUserService(repo UserRepository, cache Cache, logger *zap.Logger) *UserService {
    return &UserService{
        repo:   repo,
        cache:  cache,
        logger: logger,
    }
}

// 推荐：Functional Options 模式用于可选配置
type ServerOption func(*Server)

func WithTimeout(d time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(addr string, opts ...ServerOption) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

## 日志规范

- 使用 `go.uber.org/zap` 进行结构化日志记录，通过依赖注入传递 `*zap.Logger`
- 日志级别：Debug < Info < Warn < Error
- 在函数入口记录关键参数，在错误处记录完整上下文
- 不在底层库中记录日志，只向上返回错误
- 生产环境使用 `zap.NewProduction()`，开发环境使用 `zap.NewDevelopment()`
- 使用 `logger.With(...)` 为 logger 附加固定字段，避免重复传参

```go
// 初始化
logger, _ := zap.NewProduction()
defer logger.Sync()

// 结构化日志
logger.Info("user created",
    zap.String("user_id", user.ID),
    zap.String("email", user.Email),
)

// 错误日志
logger.Error("failed to fetch user",
    zap.String("user_id", id),
    zap.Error(err),
)

// 附加固定字段（如 request_id）
reqLogger := logger.With(zap.String("request_id", requestID))
```

## HTTP 服务

- 始终为 `http.Server` 设置超时：`ReadTimeout`、`WriteTimeout`、`IdleTimeout`
- 使用 `context` 进行请求取消和超时控制
- 统一的错误响应格式
- 使用中间件处理跨切面关注点（鉴权、日志、限流）

## 性能

- 优先使用 `strconv` 而非 `fmt` 进行数字与字符串转换（性能更好）
- 优先使用 `strings.Builder` 进行字符串拼接
- 预分配切片容量：`make([]T, 0, capacity)`
- 初始化 map 时指定容量提示：`make(map[K]V, hint)`
- 避免反复将 `string` 转为 `[]byte`，若需多次使用先转换一次并保存
- 使用 `sync.Pool` 复用临时对象
- 避免在热路径中进行内存分配
- 使用 `pprof` 进行性能分析

```go
// 推荐：strconv 比 fmt 性能更好
s := strconv.Itoa(42)        // 推荐
s := fmt.Sprintf("%d", 42)   // 避免（性能较低）

// 推荐：预分配容量
results := make([]string, 0, len(input))
index := make(map[string]int, len(keys))
```
