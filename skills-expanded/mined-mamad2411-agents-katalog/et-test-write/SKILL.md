---
name: et-test-write
description: ET test authoring workflow for WOW. Use when writing or modifying ATestHandler tests, choosing test package placement, naming test classes, creating test-only model types, preparing deterministic coroutine-style assertions, handling ObjectWait, constructing test config data, and enforcing EntityRef safety in tests.
---

# et-test-write - 测试编写入口

## 何时使用

- 编写新的 `ATestHandler` 测试用例。
- 修改现有测试用例。
- 补 `Test.md` 或最小验证清单。

## 不要加载

- 只是执行测试或查看日志：用 `et-test-run`。
- 只是做完整 TDD 流程编排：用 `et-tdd`。

## 落点与命名

1. 测试优先放在被测功能自己的 package 内：`Packages/cn.etetet.{被测包}/Scripts/Hotfix/Test/`。
2. 测试专用的数据结构、Entity、Component、BT 节点或辅助模型类型必须放在被测包的 `Scripts/Model/Test/`。
3. `Scripts/Model/Share/` 只放运行时或配置编译需要的公共模型，不放只为测试声明的类型。
4. `Scripts/Hotfix/Test/` 只放测试入口和测试流程代码，不放测试专用模型数据结构。
5. `cn.etetet.test` 只承载测试框架、公共测试基础设施，以及测试 test 包自身代码的测试；功能包测试和跨包集成测试不要临时放到 test 包。
6. 跨包集成测试必须放到拥有该集成场景的业务包；若确实是多业务编排，放到发起该编排的更高层业务包。
7. 类名遵守 `{PackageType}_{TestName}_Test`，并与所在包 `PackageType` 常量匹配。
8. 移动测试专用 C# 文件时同步移动 `.meta`，并通过 UnityBridge `RegenProject` 或项目既有流程刷新工程引用。

## 编写规则

1. 测试必须是协程式、逻辑确定的验证：按真实时序 `await` 消费事件、消息返回或明确完成信号。
2. 禁止用固定时间等待、sleep、轮询、`WaitMatch` 或无序过滤来等待状态出现。
3. ObjectWait 必须按真实时序逐个消费事件；事件桥接器只做转发，不写业务过滤。
4. 含 `await` 的测试必须在 `await` 后通过 `EntityRef` 重新获取 Entity。
5. 测试需要的 Config 数据必须由测试自己用代码构造，不要修改已有 Excel、配置文件或导出的配置代码。
6. 成功返回 `ErrorCode.ERR_Success`；失败直接返回唯一数字错误码，不污染正式 `ErrorCode.cs`。
7. 测试失败用 `Log.Console`，普通信息用 `Log.Debug`，日志统一英文。

## 常见错误

- 把功能包自己的测试或跨包集成测试写到 `cn.etetet.test`。
- 把测试专用数据结构、Entity、Component、BT 节点或辅助模型类型放到 `Scripts/Model/Share/` 或 `Scripts/Hotfix/Test/`。
- 测试类名前缀与所在包 `PackageType` 不一致。
- `await` 后直接访问旧 Entity。
- 不同失败分支返回相同错误码。
- 用 `Log.Error` 代替 `Log.Console`。
- 修改已有配置文件、Excel 表或导出的配置代码准备测试数据。
- 使用固定时间等待某种状态出现。
- 使用睡眠轮询、`WaitMatch` 或无序过滤跳过事件。
- 在正式包 `ErrorCode.cs` 里定义测试专用错误码。
