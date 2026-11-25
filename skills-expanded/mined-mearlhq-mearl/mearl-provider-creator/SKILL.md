---
name: mearl-provider-creator
description: Use when/适用于：用户希望将云浏览器、真机、外部浏览器平台或已有控制 SDK 接入 Mearl Browser Provider，或要求审计、升级已有 Provider。不用于普通页面操作、设备模拟，或只是安装和使用现成 Provider。
version: "3.1.0"
metadata:
  argument-hint: '<浏览器平台、SDK 或已有 Provider，以及期望接入的能力>'
---

# Mearl Provider Creator

把外部浏览器平台或控制 SDK 转化为可安装、可观测、可验证的 Mearl Browser Provider。用户只需给出目标平台或代码、希望支持的使用场景与必要凭据的提供方式；Agent 负责完成契约设计、实现和验证。

新建或实质修改 Provider 前，读取 [Provider 契约](./references/provider-contract.md)。随后从目标项目实际安装的 `@mearl/provider` 包、其导出类型与随包文档确认当前契约；若用户提供的是包含 Mearl Provider 源码的工作区，可通过包清单或模块解析定位对应 package，不假定它位于某个固定目录。实际依赖的公开契约与 reference 不同时，以实际依赖版本为准，并避免使用只存在于未发布源码中的内部接口。

## 输入与产物

从 SDK、API 文档、现有包或 Provider 目录推导 Provider ID、包名、目标目录、生命周期语义、控制方式、支持的 action 与输入 schema。已有 Provider 在其真实目录增量修改。新建时优先遵从用户指定位置；否则依据当前工作区已经存在的 workspace 配置和包布局选择不冲突的目录，不能从中确定唯一位置时再只询问输出目录。不要假定项目是 monorepo，也不要预设 `packages/`、`providers/` 或其他父目录。

默认产出独立 npm 包，包含 `package.json#mearl.provider`、Provider runtime、必要的 SDK adapter 和测试。只创建实际运行所需的文件，不添加占位实现或与 Provider 分发无关的文档。

## 工作流

1. 检查目标 SDK 或已有 Provider 的包结构、版本、生命周期 API、身份与凭据来源。不能从代码或官方文档确认的能力不得声明。
2. 先确定浏览器实例的状态、控制方式、归属、持久化策略和允许操作，再实现 manifest 与 runtime。不用单一 `connected` 布尔值隐藏配对、停止或失联状态。
3. 让 `browserType.inputSchema` 和真实创建参数一致；Provider 自有配置使用 `browserType.configuration.inputSchema`。需要用户理解的配对、计费、登录态和收尾规则写入 `browserType.help`。
4. 使用 `BrowserProviderDefinition` 实现 `listBrowsers`、`launch`、`close` 与真实需要的可选生命周期方法。只有 `control.kind: "provider"` 才实现 `handleAction`，并只声明已端到端验证的 capability。
5. 将 Provider 实例列表作为单一事实源，并在 server 启动后及每次可观察状态变化后通过 `server.updateBrowsers()` 发布完整快照。`definition.listBrowsers` 只供 Provider runtime 查询与校验，不会自动更新 Mearl 宿主的 `browser_list`；轮询或 SDK 事件都必须落到同一份快照再发布。
6. 优先从 `package.json#mearl.provider` 读取 runtime descriptor，避免手写两份 ID、协议、版本和 schema。验证构建产物能独立解析全部运行时依赖、manifest 的 `entry` 确实被打包，再运行包级测试、typecheck 和 build。不用关闭校验或宽化类型来掩盖契约错误。
7. 先直接运行 Provider runtime，验证 schema、实例创建与列表、一个真实 action 和关闭流程。在包已经发布到当前用户可访问的注册源时，再通过 Mearl 安装并验证 Provider 帮助、`browser_manage` 与 `browser_list`；不要为了补齐安装验证而擅自发布包。若验证必须创建计费资源、扫码配对、删除数据或提供凭据，停在该动作前请用户介入。

## 实现约束

- `providerId` 使用稳定的 kebab-case 标识，不与内置 `local` 冲突；实例 `browserId` 在该 Provider 内稳定即可。
- `operations` 只声明当前实例真实允许且 Provider 已实现的操作，并按 Runtime 映射到相应方法：`start`、`detach`、`syncCookies` 分别对应同名方法，`access` 对应 `getAccess`，`close` 与 `deleteData` 都由 `close` 处理。已停止的持久化实例可声明 `start`；临时实例不应伪装成可恢复资源。
- `details` 和 `references` 只返回可展示的非敏感 JSON。凭据不进入 Provider 列表；临时访问地址只通过 `getAccess` 返回，并标记 `sensitive: true`。
- 关闭、释放、删除数据和同步 Cookie 是不同语义。根据用户请求和平台契约选择实现，不在普通关闭中顺带删除持久化数据。
- 外部 CLI、系统服务或非 npm 运行环境由配套安装入口显式准备；Provider 的加载和帮助阶段不得静默安装。缺失时返回包含可执行修复命令的错误，配套 Skill 或 plugin 可提供幂等的 `setup` 与只读 `doctor`。
- Provider 进程退出时关闭本地 server、连接与计时器；除非平台契约明确把进程退出定义为资源关闭，否则不要把信号处理偷偷等同于 `close`、释放租约或删除远端资源。
- 已有 Provider 升级时保留用户可见的 Provider ID、输入字段和实例语义；只有真实平台契约或用户目标要求时才做不兼容变更。

## 验证与交付

单元测试至少覆盖 schema 校验、创建与列表一致性、状态与 control 组合、`server.updateBrowsers()` 的发布时机、operation 对应实现、未声明 action 拒绝和敏感元数据边界。使用 Provider 包及其所在工作区已经声明的包管理器、test、typecheck 和 build 命令；没有现成脚本时，根据实际工具链执行等价校验，不假定 pnpm、固定包名或仓库级测试项目存在。

交付时说明 Provider 路径、控制方式、实现的生命周期与 action、安装和调用示例、验证结果，以及因凭据、配对、计费或外部环境尚未完成的端到端步骤。不将“编译通过”表述成“平台接入已验证”。
