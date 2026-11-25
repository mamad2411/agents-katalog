---
name: byteconf-knowledge
description: 当在 Golang 服务中接入 ByteConf 配置管理平台、使用 code.byted.org/ttarch/byteconf_sdk 库、实现配置动态下发和实时更新时使用。
user-invocable: false
---

# ByteConf 配置管理平台

ByteConf 是字节跳动内部的配置管理平台，提供配置的动态下发、实时更新和条件规则管理能力。平台支持配置的树状管理、多租户隔离、灰度发布和容灾备份，为服务端应用提供稳定可靠的配置管理服务。

## SDK 接入

ByteConf SDK 提供配置的实时监听和动态获取能力，支持单配置监听、目录监听、条件规则配置等多种使用场景。SDK 基于 CDS 做配置分发，采用 gRPC 长链接 push 机制，实现秒级生效的配置更新。

**核心使用场景**：
- **单配置监听**：监听单个配置的变更，适用于功能开关、参数调整等场景
- **目录监听**：监听指定路径下的所有配置，支持前缀匹配，适用于批量配置管理
- **条件规则配置**：基于决策树的条件规则管理，支持丰富的规则函数和灵活组合
- **动态配置获取**：根据输入条件变量获取匹配的动态配置

[byteconf-sdk-usage.md](./byteconf-sdk-usage.md) - ByteConf SDK 使用指南

