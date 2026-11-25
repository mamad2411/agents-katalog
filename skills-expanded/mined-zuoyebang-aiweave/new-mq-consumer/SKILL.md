---
name: new-mq-consumer
description: 根据 scheduled_tasks_design.md §3 生成 MQ 消费者（攒批 + 落库 + Redis 联动 + 死信队列）。
disable-model-invocation: true
argument-hint: "[topic] 默认 {example-topic}"
---

生成 MQ 消费者。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 特定内容如下。

## 第 0 步：拒绝规则与依赖前置

- ⛔ 拒绝（§A.1）：topic 命中 `BUILD_STATUS.md` §0 中 🚫 模块时立即拒绝
- 状态检查（§A.2）：读 `BUILD_STATUS.md` §3 与 §6.2
- 依赖（§A.3）：Consumer Client 基础设施可能不存在，首次运行必须先：
  1. 检查 `helpers/kafka_consumer.go` 是否存在；不存在 → 先生成（按 `docs/architecture/helpers_api.md` §3.2）：
     ```go
     var {Topic}SubClient *kafka.SubClient
     func InitKafkaConsumer(engine *gin.Engine) {
         {Topic}SubClient = kafka.InitKafkaSub(engine, conf.RConf.KafkaSub["{topic}"])
         if {Topic}SubClient == nil { panic("init kafka consumer failed!") }
     }
     ```
  2. 检查 `conf/mount/resource.yaml` 有对应 kafkaSub 节
  3. 检查 cobra 子命令 `{topic}-consumer` 在 `router/command.go::Commands` 注册并调 `helpers.InitKafkaConsumer(engine)`

## 第 1 步：读取设计文档（公共必读见 §B）

- 主文档：`docs/service/scheduled_tasks_design.md` §3
- 额外必读：
  - `docs/schema/database_design.md`（落库表 / 按月分片）
  - `docs/architecture/pkg_api.md` §kafka.SubClient
  - `docs/cache/cache_design.md` §2.x（Redis 联动 Hash 字段映射）

## 第 2 步：生成消费者代码

文件：`controllers/mq/{topic}_consumer.go`

```go
package mq

import (
    "{project}/helpers"
    "{project}/models/db_xxx_call_log"
    "{project}/pkg/gin"
    "{project}/pkg/golib/v2/tlog"
)

type {Topic}Msg struct {
    // 字段定义（与 Producer 侧 struct 一致）
}

func Start{Topic}Consumer(engine *gin.Engine) {
    helpers.{Topic}SubClient.Subscribe(handle{Topic}Message)
    select {} // block
}

func handle{Topic}Message(ctx *gin.Context, msg interface{}) error {
    // 1. 反序列化
    // 2. 攒批（200 条 / 5s）
    // 3. 按时间月份分组 → 分表名
    // 4. 批量 INSERT
    // 5. HINCRBY 更新 Redis 日统计
    // 6. 提交 offset
    // 7. 失败 → 重试 3 次 → DLQ
}
```

## 第 3 步：注册消费者

`router/mq.go`：

```go
package router

import (
    mq_ctrl "{project}/controllers/mq"
    "{project}/pkg/gin"
)

func Mq(engine *gin.Engine) {
    go mq_ctrl.Start{Topic}Consumer(engine)
}
```

## 第 4 步：文档同步（公共项见 §C）

- 确认 `scheduled_tasks_design.md` §3 与实现一致
- 确认 `database_design.md` §4.5 MQ 链路一致
- 确认 `routing.md` §7 MQ 路由已登记
- 更新 BUILD_STATUS §6.2 状态

## 第 5 步：测试同步（4 类用例标准见 §D）

不启动真 Kafka，通过以下方式覆盖：

- **方式 A（推荐）**：Producer 侧用 `framework.Kafka` Fake 断言（`cases/internal/{producer}_test.go`）
- **方式 B**：Consumer 处理函数单测（`controllers/mq/{topic}_consumer_test.go`），不启 sarama，直接调 `processBatch`
- **方式 C**：e2e 真 Kafka（`test/e2e/scenario_{topic}_e2e_test.go`），默认 Skip

## 第 6 步：验证（公共格式见 §E）

```bash
go build ./controllers/mq/... ./router/...
go vet ./controllers/mq/...
```


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
