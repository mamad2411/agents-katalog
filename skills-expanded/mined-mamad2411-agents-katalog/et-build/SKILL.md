---
name: et-build
description: ET build, analyzer, proto export, server startup, and publish workflow. Use when compiling WOW with dotnet build ET.sln, exporting Proto to C#, starting ET.App, publishing, or validating analyzer/build results.
---

# et-build - ET Build 入口

## 何时使用

- 编译项目（唯一命令：`dotnet build ET.sln`）
- 导出 Proto 文件（`.proto` -> C#）
- 启动服务器
- 发布版本

## 不要加载

- 只是改代码、写测试，还没到编译或导出环节
- 只是导出 Luban 配置（用 `et-luban`）
- 只是查询架构规范或包依赖（用 `et-code`）

## 默认动作

1. 编译和分析器验证统一使用 `dotnet build ET.sln`，不单独编译包或 IDE 私有方案。
2. 服务器必须在 Unity 项目根目录启动，不在 `Bin/` 目录启动。
3. 运行服务器前先清理旧 `Logs/`，方便排查。
4. Model / Hotfix 程序集不能用 IDE 编译，必须走项目规定的 Unity / ET 编译入口。

## 优先入口

- 编译：`dotnet build ET.sln`
- Proto 导出：`dotnet ./Bin/ET.Proto2CS.dll`
- 启动服务器：`dotnet ./Bin/ET.App.dll --Console=1`
- 发布：`pwsh -ExecutionPolicy Bypass -File ./Scripts/Publish.ps1`

## 按需补读

- `references/et-build-commands.md`：命令、前置条件、常见排查
- `../et-luban/SKILL.md`：Luban 配置导出
- `../../../cn.etetet.test/AGENTS.md`：测试执行路由
