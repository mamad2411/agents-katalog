---
name: metrics-knowledge
description: 当在 Golang 服务中接入字节跳动 Metrics 监控系统、使用 code.byted.org/gopkg/metrics 库（含 v2、v3、v4 版本）进行监控打点、或使用 code.byted.org/inf/metrics-query SDK 查询数据时使用。
user-invocable: false
---

# Metrics 监控平台

Metrics 是字节跳动内部的监控打点系统，提供指标数据的采集、存储、查询和可视化能力。作为公司内业务接入 Metrics 系统的标准方式，Metrics SDK 是整个写入链路的第一环，支持多种编程语言，其中 Go SDK 是公司内部使用最多的基础库之一，接入了超过 50000 个 PSM。

## 前置条件

Metrics 在每台物理机/云主机都有部署名为 `metricserver2` 的 agent，SDK 依赖该 agent 向后传递数据。接入前需确保：
- **物理机**：检查 metricserver2 进程是否运行
- **容器环境**：检查 `/opt/tmp/sock` 目录下的 socket 文件是否存在

## 工程接入

仓库：https://code.byted.org/gopkg/metrics

```bash
# 接入 V4（推荐）
go get code.byted.org/gopkg/metrics/v4

# 接入 V3
go get code.byted.org/gopkg/metrics/v3

# 接入 V2
go get code.byted.org/gopkg/metrics
```

## SDK 版本选择

Metrics Go SDK 目前线上主要使用 V2、V3 和 V4 三个版本，可以一起使用而不会互相影响：

- **V4（推荐）**：最新一代 SDK，核心编码模块升级到 codec-2.0，原生支持 Metrics-2.0，性能提升 10%-100%
- **V3**：当前主要使用版本，解决了 V2 丢点问题，性能提升 50% 以上
- **V2**：早期版本，不推荐新项目使用

**使用场景**：
- 服务监控指标打点
- 业务性能数据采集
- 系统健康状态监控
- 自定义业务指标上报

## 文档索引

[metrics-sdk-overview.md](./metrics-sdk-overview.md) - Metrics Golang SDK 接入指南（含 V4/V3/V2 完整示例）

[metrics-query-guide.md](./metrics-query-guide.md) - 使用 Golang SDK 查询数据指南

[metrics-v4-guide.md](./metrics-v4-guide.md) - Metrics 2.0 Go SDK 用户使用指南（多租户、多值指标等高级功能）

