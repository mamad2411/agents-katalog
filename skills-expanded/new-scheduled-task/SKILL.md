---
name: new-scheduled-task
description: 根据 scheduled_tasks_design.md 生成定时任务实现（cobra 命令 / cycle / crontab + controller 入口 + service 方法）。
disable-model-invocation: true
argument-hint: <任务名> 例如 flush-daily-stats 或 cleanup-stale
---

根据 `$ARGUMENTS` 生成定时任务实现。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：任务名命中 `BUILD_STATUS.md` §0 中 🚫 任务（如 `{disabled-task}`）时立即拒绝
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §6 定时任务明细
- 依赖（§A.3）：对应 service 方法未实现 → 先调 `/new-service` 生成

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/service/scheduled_tasks_design.md` 中对应任务章节
- 确认任务类型（cobra / cycle / crontab）、并行策略（SPOP / 分布式锁 / 单进程）、涉及的 DB 和 Redis 操作

## 第 2 步：识别 router/command.go 整体结构

`router/command.go` 应有固定 4 函数（参见 docs-spec/10 §10）：

```go
func Commands(rootCmd *cobra.Command, engine *gin.Engine) { ... }
func run(...) error { ... }
func Tasks(engine *gin.Engine) { startCycle(engine); startCrontab(engine) }
func startCycle(engine *gin.Engine) { ... }
func startCrontab(engine *gin.Engine) { ... }
```

新增任务**只在对应函数体内追加注册行**，不改变签名或拆文件。

## 第 3 步：生成代码

### cobra 任务

a. 在 `Commands(...)` 追加：

```go
rootCmd.AddCommand(&cobra.Command{
    Use: "{task-name}",
    Run: func(cmd *cobra.Command, args []string) {
        run(engine, command_ctrl.{TaskFunc}, args...)
    },
})
```

b. 创建 controller 入口（`controllers/command/{task_name}.go`）：

```go
package command

import (
    "{project}/service/{module}"
    "{project}/pkg/gin"
)

func {TaskFunc}(ctx *gin.Context, args ...string) error {
    return {module}.{Method}(ctx)
}
```

### cycle 任务

在 `startCycle` 函数体内追加：

```go
c.AddFunc(<interval>, func(ctx *gin.Context) error {
    return {module}.{Method}(ctx)
})
```

⚠️ `c.AddFunc` 必须在 `c := command.InitCycle(engine)` 之后、`c.Start()` 之前。`c.Start()` 只调用一次。

### crontab 任务

```go
c.AddFunc("0 0 2 * * *", func(ctx *gin.Context) error {  // 6 位 cron
    return {module}.{Method}(ctx)
})
// InitCrontab 内部已 Start，不要再 Start
```

## 第 4 步：并行安全实现

```go
// SPOP 模式
for {
    member, err := conn.Do("SPOP", "{name}:dirty")
    if member == nil { break }
    ...
}

// 分布式锁模式
locked, _ := conn.Do("SET", "lock:{task_name}", "1", "NX", "EX", lockTTL)
if locked == nil { return nil }
defer conn.Do("DEL", "lock:{task_name}")
```

## 第 5 步：文档同步（公共项见 §C）

- 确认 `scheduled_tasks_design.md` 任务设计与实现一致
- 确认 `routing.md` §8 命令表已含此任务
- 更新 BUILD_STATUS §6 状态

## 第 6 步：测试同步（4 类用例标准见 §D）

定时任务**不**通过 HTTP 测，而是：

- **方式 A（推荐）**：service 方法单元测试（`service/{module}/{action}_test.go`）
- **方式 B**：e2e 端到端（`test/e2e/scenario_{task}_test.go`）

至少覆盖：正常 flush / 空 Set 不报错 / 部分失败 entry 仍在 dirty。

## 第 7 步：验证（公共格式见 §E）

```bash
go build ./controllers/command/... ./service/{module}/... ./router/...
go vet ./...
cd test && go test -v ./e2e/... -run Scenario{Task}
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
