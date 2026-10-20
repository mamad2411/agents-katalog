# Copilot instructions

This repository is set up to use Aspire. Aspire is an orchestrator for the entire application and will take care of configuring dependencies, building, and running the application. The resources that make up the application are defined in `apphost.cs` including application code and external dependencies.

## General recommendations for working with Aspire
1. Before making any changes always run the apphost using `aspire run` and inspect the state of resources to make sure you are building from a known state.
1. Changes to the _apphost.cs_ file will require a restart of the application to take effect.
2. Make changes incrementally and run the aspire application using the `aspire run` command to validate changes.
3. Use the Aspire MCP tools to check the status of resources and debug issues.

## Running the application
To run the application run the following command:

```
aspire run
```

If there is already an instance of the application running it will prompt to stop the existing instance. You only need to restart the application if code in `apphost.cs` is changed, but if you experience problems it can be useful to reset everything to the starting state.

## Checking resources
To check the status of resources defined in the app model use the _list resources_ tool. This will show you the current state of each resource and if there are any issues. If a resource is not running as expected you can use the _execute resource command_ tool to restart it or perform other actions.

## Listing integrations
IMPORTANT! When a user asks you to add a resource to the app model you should first use the _list integrations_ tool to get a list of the current versions of all the available integrations. You should try to use the version of the integration which aligns with the version of the Aspire.AppHost.Sdk. Some integration versions may have a preview suffix. Once you have identified the correct integration you should always use the _get integration docs_ tool to fetch the latest documentation for the integration and follow the links to get additional guidance.

## Debugging issues
IMPORTANT! Aspire is designed to capture rich logs and telemetry for all resources defined in the app model. Use the following diagnostic tools when debugging issues with the application before making changes to make sure you are focusing on the right things.

1. _list structured logs_; use this tool to get details about structured logs.
2. _list console logs_; use this tool to get details about console logs.
3. _list traces_; use this tool to get details about traces.
4. _list trace structured logs_; use this tool to get logs related to a trace

## Other Aspire MCP tools

1. _select apphost_; use this tool if working with multiple app hosts within a workspace.
2. _list apphosts_; use this tool to get details about active app hosts.

## Playwright MCP server

The playwright MCP server has also been configured in this repository and you should use it to perform functional investigations of the resources defined in the app model as you work on the codebase. To get endpoints that can be used for navigation using the playwright MCP server use the list resources tool.

## Updating the app host
The user may request that you update the Aspire apphost. You can do this using the `aspire update` command. This will update the apphost to the latest version and some of the Aspire specific packages in referenced projects, however you may need to manually update other packages in the solution to ensure compatibility. You can consider using the `dotnet-outdated` with the users consent. To install the `dotnet-outdated` tool use the following command:

```
dotnet tool install --global dotnet-outdated-tool
```

## Persistent containers
IMPORTANT! Consider avoiding persistent containers early during development to avoid creating state management issues when restarting the app.

## Aspire workload
IMPORTANT! The aspire workload is obsolete. You should never attempt to install or use the Aspire workload.

## Official documentation
IMPORTANT! Always prefer official documentation when available. The following sites contain the official documentation for Aspire and related components

1. https://aspire.dev
2. https://learn.microsoft.com/dotnet/aspire
3. https://nuget.org (for specific integration package details)

## BMAD AI 工作流

本项目已集成 BMAD (Breakthrough Method of Agile AI-Driven Development) 完整工作流，用于结构化的软件开发生命周期管理。

### 快速开始

1. **小型任务/Bug 修复** (Quick Flow):
   - `/quick-spec` - 创建技术规范
   - `/quick-dev` - 实现变更
   - `/code-review` - 代码审查

2. **完整功能开发** (Full Flow):
   - `/product-brief` - 产品需求简报
   - `/create-prd` - 创建 PRD
   - `/create-architecture` - 架构设计
   - `/create-epics-and-stories` - 拆分为 Epic 和 Story
   - `/sprint-planning` - Sprint 规划
   - `/dev-story` - 实现 Story
   - `/code-review` - 代码审查
   - `/retrospective` - 复盘

### 与 CodeSpirit 规范集成

BMAD 工作流已配置为自动遵循 CodeSpirit 的所有开发规范（位于 `.cursor/rules/`）。在使用 BMAD 时：

- PRD 会自动考虑多租户、多数据库、AI 功能等项目特性
- 架构设计会遵循依赖注入、缓存策略等规范
- Story 实现会应用正确的命名约定、DTO 设计、控制器规范等
- 代码审查会执行 CodeSpirit 特定的审查清单

### 获取帮助

任何时候，输入 `/bmad-help` 可获取上下文相关的指导。

详细使用指南请参考：
- **[BMAD 使用教程](Docs/bmad/bmad-tutorial.md)** - 完整的综合教程（推荐新手阅读）
- [BMAD 工作流指南](Docs/bmad/bmad-workflow-guide.md) - 详细的工作流使用指南
- [BMAD 团队培训指南](Docs/bmad/bmad-team-guide.md) - 团队培训材料
- [BMAD 集成技能](.cursor/skills/bmad-integration/SKILL.md) - BMAD 与 CodeSpirit 集成
- [项目上下文文档](project-context.md) - 项目上下文和规范引用