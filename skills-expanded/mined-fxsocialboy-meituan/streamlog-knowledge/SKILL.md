---
name: streamlog-knowledge
description: 当在 Golang 服务中接入 StreamLog 流式日志平台、使用 code.byted.org/gopkg/logs SDK 或 logs/v2 SDK、实现微服务日志采集和上报时使用。
user-invocable: false
---

# StreamLog 流式日志平台

StreamLog（流式日志平台）是字节跳动内部的日志管理服务，提供日志的实时采集、存储、查询和分析能力，支持微服务架构下的日志统一管理和监控告警。

## SDK 接入

StreamLog SDK 主要用于微服务日志接入场景，适用于部署在 TCE、FaaS、Cronjob、Goofy、Bernard 等平台的服务，这些服务有明确的 PSM 作为服务标识。

**主要使用场景**：
- **微服务日志采集**：为部署在云原生平台的服务提供标准化的日志采集方案
- **日志实时上报**：通过 Unix Domain Socket (UDS) 将日志实时发送到 StreamLog 代理
- **日志查询与分析**：支持基于关键字、SQL 查询、Trace 日志等多种查询方式
- **监控告警集成**：与监控系统集成，实现日志转指标和告警关联

**SDK 版本选择**：
- **StreamLog 1.0 SDK**：适用于旧版本平台，API 形式为 `{Level}sf(format string, v ...string)` 的无反射 Format API
- **StreamLog 2.0 SDK**：新版本平台，提供更灵活的日志拼接 API，如 `Str()` 和 `Obj()` 方法

**初始化示例**：
```go
func init() {
   options := []logs.Option{
      logs.SetWriter(
         logs.InfoLevel,
         writer.NewConsoleWriter(),
         writer.NewAgentWriter(),
         writer.NewAsyncWriter(
            writer.NewFileWriter("test/test.log", writer.Hourly, writer.SetKeepFiles(12)),
            true,
         ),
      ),
   }
   log.SetDefaultLogger(options...)
}
```

[streamlog-sdk-usage.md](./streamlog-sdk-usage.md) - StreamLog SDK 使用指南

