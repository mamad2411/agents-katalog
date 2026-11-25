---
name: mearl-profile-creator
description: "Create, update, or review a Mearl App Profile for H5 or WebView emulation. 适用于新建、修改或审查 Mearl App Profile，包括客户端 UA、JSBridge、WebView 行为及 Profile 分发。使用现有端模拟时走通用 Mearl 流程。"
version: "3.1.0"
---

# Mearl Profile Creator

将 App WebView 的页面可见行为做成可安装、可验证的 Mearl App Profile。先读[端模拟开发参考](references/app-profile.md)，再按目标项目实际依赖的 `@mearl/browser-core`、`@mearl/app-profiles` 和 `@mearl/preset` 公开契约确认可用字段与宿主能力。

1. 从用户指定的客户端、现有配置或可靠的文档和样本确认平台、UA、版本、桥对象、调用和回调约定，以及页面需要复现的容器行为。区分已确认的行为和测试替身，在 `usage.limitations` 说明覆盖范围。
2. 沿用已有包和 Profile ID。新建时根据目标工作区选择包目录，用 `<bundle-id>/<profile-id>` 命名定义。优先用声明式配置描述 UA 和方法数据。实现 JSBridge 或容器行为时，确认宿主是否已有匹配实现，按需为 Profile 绑定页面运行时。
3. 用真实资源字节生成 `bundle.json`。独立安装时交付 Profile 及清单所引用的资源。任务需要通过 Preset 选择实现时，在对应 Preset 声明浏览器包及 App ID 映射。
4. 先校验定义、包清单与资源，再在隔离的目标浏览器检查能力目录。用新标签页在导航前启用 Profile，验证首屏请求和页面可见行为，再验证清除或切换。已有 Profile 更新时覆盖受影响的平台和原有调用方式。

交付时给出包路径、能力目录中的 ID、安装与使用示例、模拟范围和实际完成的验证。若缺少安装来源或目标宿主，记录可复现的验收步骤。
