---
name: et-unitybridge
description: UnityBridge workflow for AI operations in Unity Editor. Use when checking UnityBridge connectivity, Unity compile or PlayMode state, running deferred UnityBridge commands, operating assets/scenes/GameObjects/Inspector/Prefabs/GameView/screenshots, running Editor tests, or troubleshooting UnityBridge responses.
---

# et-unitybridge - UnityBridge / AI 操作 Unity 入口

## 何时使用

- 查询 UnityBridge 宿主是否在线、Unity 是否正在编译、PlayMode 状态、CodeMode、Unity 版本。
- 让 AI 操作 Unity Editor：资源、场景、选择集、GameObject、Transform、Inspector、Prefab、菜单、截图、GameView、Editor 测试。
- 执行 `Compile` / `Refresh` / `RegenProject` / `EnterPlay` / `ExitPlay` / `Reload` 等会跨 Unity 状态变化的命令。
- 排查 UnityBridge 返回的 `Error` / `Message`。

## 不要加载

- 只是普通 C# 编译（用 `et-build`）
- 只是读写 Excel 或导出 Luban
- 只是纯代码结构分析，不需要 Unity 编辑器参与
- 只是要解释命令协议，不实际操作 Unity 时，优先只读 proto 或 handler，不启动 UnityBridge。

## 默认动作

1. CLI 入口为 `dotnet ./Bin/ET.UnityBridge.dll`。
2. 操作前先发 `Ping`；只有需要命令列表或详细状态时再查 `HostState`。
3. `Compile`、`Refresh`、`RegenProject`、`EnterPlay`、`ExitPlay`、`AssetImportRequest`、`AssetRefreshRequest` 等 deferred 命令必须等待最终响应。
4. `Reload` 要求 Unity 已进入 PlayMode；`EnterPlay` 前确认 Unity 未编译且未切换 PlayMode。
5. 如果 `Bin/ET.UnityBridge.dll` 尚不存在，先用 `et-build` 编译确认工具是否生成。
6. 如果桥接宿主不可用，先检查 Unity 是否已打开项目、心跳文件是否存在、桥接根目录是否一致。

## 省 Token 规则

- 不要完整读取所有 UnityBridge proto、handler 或 `AvailableCommands`。
- 先用 `HostState` 或 `rg` 发现命令名，再只打开相关 proto 小片段和对应 handler。
- 先执行最小读命令确认目标，再做写操作；批量操作前先验证 1 个样本。
- 不要把完整 JSON 响应贴给用户；只总结 `Error`、`Message` 和关键字段。
- 优先 UnityBridge 命令，不要用 GUI 点击 Unity Editor，除非命令缺失或用户明确要求。

## 最小流程

```powershell
dotnet ./Bin/ET.UnityBridge.dll '{"_t":"Ping"}'
```

如果需要命令列表或状态：

```powershell
dotnet ./Bin/ET.UnityBridge.dll '{"_t":"HostState"}'
```

按任务选择一个最小命令执行；失败时先看 `Error` / `Message`，再读相关 handler。

## 按需补读

- `references/et-unitybridge-ai-ops.md`：AI 操作 Unity 的任务路由、命令发现、省 token 操作模式。
- `references/et-unitybridge-cli.md`：CLI 参数、等待、返回值解读、常见错误。
