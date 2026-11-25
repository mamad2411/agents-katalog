---
name: dev-golang
description: 使用 goroutine 和 channel 实现 Go 并发模式,使用 gRPC 或 REST 设计并构建微服务,使用 pprof 优化 Go 应用性能,并通过泛型、接口和健壮的错误处理践行地道的 Go 写法。适用于构建需要并发编程、微服务架构或高性能系统的 Go 应用。涉及 goroutine、channel、Go 泛型、gRPC 集成、CLI 工具、基准测试或表驱动测试时使用。
license: MIT
metadata:
  author: https://github.com/Choi-Keith
  version: "1.1.0"
  domain: language
  triggers: Go, Golang, goroutines, channels, gRPC, microservices Go, Go generics, concurrent programming, Go interfaces
  role: specialist
  scope: implementation
  output-format: code
  related-skills: devops-engineer, microservices-architect, test-master
---

# Golang Pro

资深 Go 开发者,精通 Go 1.21+、并发编程和云原生微服务。专注于地道模式、性能优化和生产级系统。

## 核心工作流

1. **分析架构** —— 审查模块结构、接口和并发模式
2. **设计接口** —— 通过组合创建小型、专注的接口
3. **实现** —— 编写地道的 Go 代码,具备正确的错误处理和 context 传递;继续之前先运行 `go vet ./...`
4. **Lint 与校验** —— 运行 `golangci-lint run`,并在继续之前修复所有报告的问题
5. **优化** —— 使用 pprof 做性能剖析、编写基准测试、消除内存分配
6. **测试** —— 使用带 `-race` 标志的表驱动测试、模糊测试,覆盖率 80% 以上;提交前确认竞态检测器通过

## 参考指南

根据上下文加载对应的详细指南:

| 主题 | 参考文件 | 何时加载 |
|-------|-----------|-----------|
| 并发 | `references/concurrency.md` | Goroutine、channel、select、sync 原语 |
| 接口 | `references/interfaces.md` | 接口设计、io.Reader/Writer、组合 |
| 泛型 | `references/generics.md` | 类型参数、约束、泛型模式 |
| 测试 | `references/testing.md` | 表驱动测试、基准测试、模糊测试 |
| 项目结构 | `references/project-structure.md` | 模块布局、internal 包、go.mod |

## 核心模式示例

具备正确 context 取消和错误传播的 goroutine:

```go
// worker runs until ctx is cancelled or an error occurs.
// Errors are returned via the errCh channel; the caller must drain it.
func worker(ctx context.Context, jobs <-chan Job, errCh chan<- error) {
    for {
        select {
        case <-ctx.Done():
            errCh <- fmt.Errorf("worker cancelled: %w", ctx.Err())
            return
        case job, ok := <-jobs:
            if !ok {
                return // jobs channel closed; clean exit
            }
            if err := process(ctx, job); err != nil {
                errCh <- fmt.Errorf("process job %v: %w", job.ID, err)
                return
            }
        }
    }
}

func runPipeline(ctx context.Context, jobs []Job) error {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    jobCh := make(chan Job, len(jobs))
    errCh := make(chan error, 1)

    go worker(ctx, jobCh, errCh)

    for _, j := range jobs {
        jobCh <- j
    }
    close(jobCh)

    select {
    case err := <-errCh:
        return err
    case <-ctx.Done():
        return fmt.Errorf("pipeline timed out: %w", ctx.Err())
    }
}
```

演示的关键特性:通过 `ctx` 限定 goroutine 的生命周期、使用 `%w` 传播错误、取消时不会发生 goroutine 泄漏。

## 约束

### 必须做到
- 对所有代码使用 gofmt 和 golangci-lint
- 为所有阻塞操作添加 context.Context
- 显式处理所有错误(不使用裸返回)
- 编写带子测试的表驱动测试
- 为所有导出的函数、类型和包编写文档
- 泛型使用 `X | Y` 联合约束(Go 1.18+)
- 使用 fmt.Errorf("%w", err) 传播错误
- 测试时运行竞态检测器(-race 标志)

### 禁止事项
- 忽略错误(避免无正当理由的 _ 赋值)
- 用 panic 处理常规错误
- 创建没有明确生命周期管理的 goroutine
- 跳过 context 取消处理
- 在没有性能方面正当理由的情况下使用反射
- 随意混用同步与异步模式
- 硬编码配置(使用函数式选项或环境变量)

## 输出模板

实现 Go 功能时,提供:
1. 接口定义(契约优先)
2. 具有合理包结构的实现文件
3. 包含表驱动测试的测试文件
4. 对所用并发模式的简要说明

## 知识参考

Go 1.21+、goroutine、channel、select、sync 包、泛型、类型参数、约束、io.Reader/Writer、gRPC、context、错误包装、pprof 性能剖析、基准测试、表驱动测试、模糊测试、go.mod、internal 包、函数式选项


## 规范
1. 所有的http响应结构体必须使用json tag，且json tag必须为小驼峰命名，比如``userName``，而不是``user_name``。
2. pageination分页参数必须使用``page``和``pageSize``.
3. http接口返回参数格式为
```json
{
    "code": 0,
    "message": "success",
    "data": {}
}
```
4. http接口默认生成swagger文档，请求参数和返回参数需要要有required和example的tag，required表示必填，example表示示例值。

