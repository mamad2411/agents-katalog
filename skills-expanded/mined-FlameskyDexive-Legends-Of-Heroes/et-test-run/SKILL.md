---
name: et-test-run
description: ET test execution and failure debugging workflow for WOW. Use when building before tests, cleaning Logs, running server or Hotfix tests through ET.App Test commands, running Unity Editor tests through UnityBridge UnityTestRunRequest, reading Logs/All.log, judging results, and diagnosing failed or unmatched tests.
---

# et-test-run - 测试执行入口

## 何时使用

- 执行测试（全部 / 指定用例）。
- 查看测试日志、分析失败原因。
- 验证修改后的代码是否通过目标测试或回归测试。

## 不要加载

- 只是编写测试用例：用 `et-test-write`。
- 只是编译项目：用 `et-build`。

## 默认动作

1. 先用 `dotnet build ET.sln` 编译，除非用户明确只要看日志或已经完成编译。
2. 运行测试前清理 `Logs/`，避免旧日志干扰。
3. 服务端 / Hotfix 测试使用 WOW 现有测试入口：管道输入 `Test` 命令到 `dotnet ./Bin/ET.App.dll --SceneName=Test`。
4. Unity Editor 测试使用 UnityBridge 的 `UnityTestRunRequest`，按 `Name` 正则匹配测试类名执行。
5. Editor 测试不走 Unity Test Framework 的 `Filter`、`ExecutionSettings` 或 Test Runner。
6. 失败时先看控制台首个失败点；服务端测试再看 `Logs/All.log`，Editor 测试看 response 里的 `Message` 与 `Results[].Message`。
7. 服务端测试成功后也检查 `Logs/All.log`，确认没有隐藏异常或错误日志。
8. 调试失败遵循先定位原因、再改代码；不要为了跑通测试随意修改正常业务逻辑。

## 常用命令

```powershell
dotnet build ET.sln
```

```powershell
Remove-Item ./Logs -Recurse -Force -ErrorAction SilentlyContinue
```

```powershell
"Test" | dotnet ./Bin/ET.App.dll --SceneName=Test
```

```powershell
"Test --Name=CreateRobot" | dotnet ./Bin/ET.App.dll --SceneName=Test
```

```powershell
dotnet ./Bin/ET.UnityBridge.dll '{"_t":"Ping"}'
```

```powershell
dotnet ./Bin/ET.UnityBridge.dll '{"_t":"UnityTestRunRequest","Name":".*"}'
```

```powershell
Get-Content ./Logs/All.log -Tail 200
```

## 常见失败原因

| 现象 | 优先检查 |
|---|---|
| Entity 已失效 | `await` 后是否通过 `EntityRef` 重新获取 |
| 数据不一致 | 测试准备与配置链路 |
| 消息超时 | 网络消息发送、事件是否真的发布 |
| Fiber 未找到 | 场景或 Fiber 名称 |
| 未找到测试 | 类名、`PackageType` 前缀、测试目录 |
| Editor 测试未匹配 | `Name` 正则、类是否继承 `ET.Test.ATestHandler`、是否在 `Scripts/Editor/Test/` |
| 找不到 `UnityTestRunRequest` | Unity Editor 是否打开、UnityBridge 是否在线、是否执行过 `Refresh` |
| 配置不存在 | 测试是否自己用代码构造最小 Config 数据 |
