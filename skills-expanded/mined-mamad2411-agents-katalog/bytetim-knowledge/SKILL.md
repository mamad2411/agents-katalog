---
name: bytetim-knowledge
description: 当在 Golang 服务中接入 ByteTIM 流量身份标识平台、使用 code.byted.org/bytetim/client-go SDK、实现票据校验或服务端中间件时使用。
user-invocable: false
---

# ByteTIM 流量身份标识平台

ByteTIM（ByteDance Traffic Identity Mark）是字节跳动内部统一的流量身份票据方案，提供一种机制在流量入口服务解析并注入请求流量相关的身份票据信息（如 UserID、DeviceID、AppID），随着请求链路进行传递，并在请求链路底层服务提供读取和校验 ByteTIM 身份票据信息的能力。

## SDK 接入

ByteTIM SDK 主要分为票据生成方和票据校验方两种角色。对于服务端场景，需要根据服务在请求链路中的位置确定接入方式：

**服务角色判断**：
- **票据校验方**：仅负责校验票据，一般为请求链路的底层服务
- **票据生成方**：如果服务同时存在票据生成以及票据校验的诉求，按票据生成方角色进行注册

**框架支持**：
- **KiteX 框架**：支持客户端和服务端中间件，通过 `timkitex` 包提供接入能力
- **Kite 框架**：支持传统 Kite 框架的客户端和服务端中间件
- **HTTP 框架**：支持 Ginex、Hertz v1.x、Hertz v0.x 等 HTTP 框架

**核心能力**：
- 票据的自动生成和注入
- 票据的读取和验签校验
- 自定义参数的透传支持
- 新旧版本票据兼容性配置

[bytetim-sdk-usage.md](./bytetim-sdk-usage.md) - ByteTIM SDK 使用指南
[bytetim-kitex-integration.md](./bytetim-kitex-integration.md) - KiteX 框架集成指南
[bytetim-http-integration.md](./bytetim-http-integration.md) - HTTP 框架集成指南
[bytetim-python-sdk.md](./bytetim-python-sdk.md) - Python SDK 使用指南

