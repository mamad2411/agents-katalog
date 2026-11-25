---
name: dolphin-knowledge
description: 当在Golang或Rust服务中接入Dolphin动态决策平台、使用code.byted.org/dolphin/go-dolphin/v2或rust-dolphin SDK、调用规则决策、或实现业务逻辑动态配置时使用。
user-invocable: false
---

# Dolphin动态决策平台

Dolphin是基于规则引擎的动态决策平台，支持通过配置规则替代业务中频繁变更的业务逻辑，提升用户业务的工作和运营效率。平台将业务逻辑抽象为事件、规则组和规则，让开发者能够在不修改代码的情况下动态调整业务决策逻辑。

## SDK接入

Dolphin提供多种接入方式，其中**SDK接入是推荐方案**，支持Go和Rust语言。SDK基于高性能规则执行引擎实现，通过RPC异步获取规则和配置，规则在本地执行，提供低延迟的决策能力。

**核心特性**：
- **本地执行**：规则在业务服务本地执行，避免网络延迟
- **异步更新**：规则配置异步拉取，不影响服务性能
- **多语言支持**：支持Go和Rust语言SDK
- **容灾机制**：支持从本地文件加载规则，保障服务可用性

**使用场景**：
- 业务规则频繁变更的动态配置
- 需要高性能决策的业务逻辑
- 多环境（泳道）规则管理
- 功能开关和灰度发布控制

[dolphin-sdk-usage.md](./dolphin-sdk-usage.md) - Dolphin SDK使用指南
[dolphin-sdk-disaster-recovery.md](./dolphin-sdk-disaster-recovery.md) - Dolphin SDK容灾方案
[dolphin-sdk-lane.md](./dolphin-sdk-lane.md) - Dolphin SDK泳道配置指南

