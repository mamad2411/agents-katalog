---
name: tcc-knowledge
description: 当在 Golang 服务中接入 TCC 动态配置中心、使用 code.byted.org/gopkg/tccclient SDK、调用 GetConfig、或实现功能开关/灰度配置时使用。
user-invocable: false
---

# TCC 动态配置中心

TCC（动态配置中心）是字节跳动内部的配置管理服务，提供配置的动态下发和实时更新能力。

## SDK 接入

TCC 提供两个主要的 Golang SDK：

- **TCC V2 SDK**：支持访问 TCC V2/V3 配置，推荐版本 >= v1.6.2
- **TCC V3 SDK**：专用于访问 TCC V3 配置，推荐版本 >= v3.0.0

**使用场景**：
- 动态配置管理
- 功能开关控制
- 灰度发布配置
- 运行时参数调整

[tcc-usage.md](./tcc-usage.md) - TCC SDK 使用指南
