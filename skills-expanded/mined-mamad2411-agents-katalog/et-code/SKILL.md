---
name: et-code
description: ET framework C# code authoring and review workflow. Use when creating or modifying Entity, Component, System, Helper, message handlers, package dependencies, assemblies, module analyzer boundaries, C# file placement, .meta handling, ECS layering, or component contract logic in WOW/ET packages.
---

# et-code - ET Code 入口

## 何时使用

- 新建或修改 `Entity`、`Component`、`System`、`Helper`
- 新建或修改 `MessageLocationHandler`、`MessageHandler<T>`、`MessageSessionHandler`
- 新建或移动 C# 文件，检查 `.meta`、程序集与包内落点
- 新增消息、模块、程序集或包依赖
- 处理 ECS 分层、组件存在性契约、Module analyzer、分析器报错

## 不要加载

- 只是执行测试、导出配置或操作 Excel
- 只做 Unity 编辑器操作（用 `et-unitybridge`）

## 默认动作

1. 先确认改动所在 package、程序集层级和包内 `AGENTS.md` 规则。
2. 检查代码是否位于 `Packages/cn.etetet.*`，并确认是否需要关注 `packagegit.json`、`PackageType.cs`。
3. 先判断 Entity / System 分离、Handler `Run` 规范、包依赖单向、Module analyzer、禁止 hard code 是否受影响。
4. 新增组件或判空前先确认组件存在性契约；按设计必然存在的组件不要偷偷兜底创建。
5. 涉及 `async` / `await` / `ETTask` / `EntityRef` 时，叠加 `../et-async/SKILL.md`。
6. 新建类前优先复用现有结构；默认一类一文件。
7. 严禁 AI 手工生成 `.meta` 或手工修改 `.csproj`；移动 C# 文件时必须同步移动对应 `.meta` 以保留 GUID。
8. 严禁为了注册表、缓存、映射关系随手新增静态可变字段；先确认生命周期与 owner。

## 快速分流

- 文件、`.meta`、包落点、包层级：补读 `references/et-code-rules.md`
- ECS 数据/逻辑边界、组件契约、Module analyzer：补读 `references/et-code-rules.md`
- `await` 后 Entity 访问、`EntityRef<T>`、`NewContext(...)`：叠加 `et-async`
- 编译或分析器验证：转 `et-build`

## 输出要求

- 说明代码落点、包依赖、程序集层次是否正确
- 说明是否影响 `.meta`、`.csproj`、Unity 刷新或工程文件生成
- 说明是否影响 `EntityRef` / `await` 安全、Handler `Run` 规范
- 说明是否引入新的 analyzer 风险、静态状态风险或模块边界问题
