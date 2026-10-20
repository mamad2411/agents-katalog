---
name: frontier-knowledge
description: 当在 Golang 服务中接入 Frontier 长连接网关、使用 code.byted.org/frontier/server-sdk-go SDK、实现上行消息接收和下行消息推送功能时使用。
user-invocable: false
---

# Frontier 长连接网关

Frontier 是字节跳动集团的消息网关产品服务，为业务侧提供安全、双工、低延迟的消息传递服务，满足全球海量消息推送需求。它作为长连接网关，在客户端与后端服务之间建立稳定的通信通道，支持双向消息传递。

## SDK 接入

Frontier 服务端 SDK 主要用于在业务后端服务中集成 Frontier 的长连接能力，实现上行消息的接收和下行消息的推送功能。当前仅支持 Go 语言版本，代码仓库地址为 `code.byted.org/frontier/server-sdk-go`。

**主要使用场景**：
- **上行消息接收**：接收客户端通过 Frontier 发送的消息
- **下行消息推送**：向客户端推送消息，支持单设备、多设备、跨应用等不同推送模式
- **条件推送**：根据设备平台、客户端版本、用户标签等条件进行精准推送
- **组播管理**：实现业务组的创建、销毁和组成员管理
- **连接管理**：查询在线连接信息，管理连接生命周期

**核心接口概览**：
- **上行接口**：`SendMessage`、`Auth`、`SendEvent`、`ACKMessage`
- **下行接口**：`Push`/`PushAsync`、`PushV2`/`PushV2Async`、`BatchPush`/`BatchPushAsync`、`GroupPush`/`GroupPushAsync`、`BroadcastPush`/`BroadcastPushAsync`、`QueryOnline`/`QueryOnlineAsync`

**技术前提**：
- Go 版本要求 ≥ 1.17
- 需要实现 `FrontierCallback` 接口来处理上行消息

[frontier-sdk-usage.md](./frontier-sdk-usage.md) - Frontier SDK 详细使用指南

