---
name: libra-knowledge
description: 当在 Golang 服务中接入 Libra A/B 实验平台、使用 code.byted.org/iesarch/abtest SDK、调用分流服务获取实验参数、或实现服务端 A/B 实验功能时使用。
user-invocable: false
---

# Libra A/B 实验平台

Libra 是字节跳动内部的 A/B 实验平台，提供从实验设计、流量分配、参数下发到效果分析的全链路实验能力。平台通过**分流服务**实现用户随机抽样和流量分层管理，支持大规模并行实验，确保实验结果的科学性和可靠性。

## SDK 接入

对于 Golang 服务，推荐使用由 IES 架构团队开发的 **Abtest SDK**。该 SDK 封装了 RPC 调用、AB 参数解析等底层逻辑，为开发者提供直接读取实验参数的简洁接口。

**核心使用场景**：
- **服务端 A/B 实验**：在服务端逻辑中根据用户身份动态返回不同的实验参数
- **配置动态下发**：通过配置中心管理实验参数，实现运行时动态调整
- **流量分层管理**：利用 Libra 的分流服务实现同层互斥、层间正交的流量复用
- **实验数据上报**：确保实验曝光时能正确上报实验组标记（vid）用于效果分析

**接入前准备**：
1. 确保产品已完成 Libra 平台的基础接入，拥有有效的应用（App）标识（app_id）和功能模块（Token）。
2. 对于服务端实验，需要创建或关联对应的**配置空间**（Namespace），这是配置下发的最小管理单位。

**SDK 初始化示例**：
```go
import "code.byted.org/iesarch/abtest/ab"

// 推荐方式：创建独立的 Client 实例
options := []ab.Option{
    ab.DesignationMode(ab.LibraNamespaceOpti), // 必须！使用 Libra 推荐的 namespace 优化
    ab.EnableNsReveal(), // 开启本地兜底，保障线上业务安全
}
AbClient := ab.MustNewClient(options...)
```

**重要注意事项**：
- SDK 配置应在**进程级别**生效，避免在公共库（common lib）中配置
- 确保实验参数（abparam）的 key 中不包含 "." 字符，或使用自定义分隔符
- 接入完成后需进行**接入校验**，验证实验配置能正确返回且 ABLog 能正常写入

[abtest-sdk-usage.md](./abtest-sdk-usage.md) - Abtest SDK 详细使用指南与最佳实践
[libra-config-space.md](./libra-config-space.md) - Libra 配置空间管理与配置发布流程

