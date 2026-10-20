---
description: CodeSpirit 项目配置规范 - 目标框架、SDK类型、集中式包管理
globs: *.csproj
alwaysApply: false
---

# csproj 项目配置规范

## 目标框架

- **必须使用 .NET 10**: `<TargetFramework>net10.0</TargetFramework>`
- 添加或更新包时，必须与当前解决方案的包版本保持一致

## SDK 类型选择

| 项目类型 | SDK |
|---------|-----|
| API 服务 | `Microsoft.NET.Sdk.Web` |
| 组件库 / 类库 | `Microsoft.NET.Sdk` |
| AppHost | `Aspire.AppHost.Sdk/13.0.2` |

## PropertyGroup 配置规范

### 通用配置

```xml
<PropertyGroup>
  <TargetFramework>net10.0</TargetFramework>
  <ImplicitUsings>enable</ImplicitUsings>
</PropertyGroup>
```

### Web API 项目

```xml
<PropertyGroup>
  <TargetFramework>net10.0</TargetFramework>
  <ImplicitUsings>enable</ImplicitUsings>
  <Nullable>disable</Nullable>
  <UserSecretsId>{生成的GUID}</UserSecretsId>
  <DockerDefaultTargetOS>Linux</DockerDefaultTargetOS>
  <DockerfileContext>..\..</DockerfileContext>
</PropertyGroup>
```

### AppHost 项目

```xml
<PropertyGroup>
  <OutputType>Exe</OutputType>
  <TargetFramework>net10.0</TargetFramework>
  <ImplicitUsings>enable</ImplicitUsings>
  <Nullable>enable</Nullable>
  <IsAspireHost>true</IsAspireHost>
</PropertyGroup>
```

### 测试项目

```xml
<PropertyGroup>
  <TargetFramework>net10.0</TargetFramework>
  <ImplicitUsings>enable</ImplicitUsings>
  <IsPackable>false</IsPackable>
</PropertyGroup>

<ItemGroup>
  <Using Include="Xunit" />
</ItemGroup>
```

### 需要生成文档的组件库

```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
```

## 集中式包管理（Central Package Management）

> ✅ **重要**: 项目已启用集中式包管理，所有包版本在 `Directory.Packages.props` 中统一管理

### 包引用规范

1. **添加新包时**：
   - 首先在 `Directory.Packages.props` 中添加 `<PackageVersion Include="PackageName" Version="x.y.z" />`
   - 然后在项目文件中添加 `<PackageReference Include="PackageName" />`（**不指定 Version**）

2. **项目文件中的包引用**：
   ```xml
   <!-- ✅ 正确：不指定版本，由 Directory.Packages.props 管理 -->
   <PackageReference Include="Newtonsoft.Json" />
   
   <!-- ❌ 错误：不要指定版本 -->
   <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
   ```

3. **版本覆盖（特殊情况）**：
   - 仅在必要时使用 `VersionOverride`，并添加注释说明原因
   - 例如：使用 `Aspire.Microsoft.EntityFrameworkCore.SqlServer` 的项目需要 EF Core 10.0.0
   ```xml
   <!-- 注意：Aspire.Microsoft.EntityFrameworkCore.SqlServer 13.0.2 需要 EF Core 10.0.0 -->
   <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" VersionOverride="10.0.0" />
   ```

4. **查看所有包版本**：
   - 查看 `Directory.Packages.props` 文件
   - 包按功能分类组织（Aspire、EF Core、Extensions 等）

### 核心框架包版本

所有包版本在 `Directory.Packages.props` 中定义，主要版本如下：

| 包类别 | 版本 |
|--------|------|
| Aspire.* (大部分) | `13.0.2` |
| Aspire.Hosting.Elasticsearch | `13.1.0` |
| Aspire.Elastic.Clients.Elasticsearch | `13.1.0` |
| Microsoft.Extensions.* | `10.0.0` |
| Microsoft.AspNetCore.* | `10.0.0` |
| Microsoft.EntityFrameworkCore.* | `9.0.9` (默认) / `10.0.0` (使用 Aspire EF Core 集成) |
| Pomelo.EntityFrameworkCore.MySql | `9.0.0` |
| OpenTelemetry.* | `1.11.1` |
| StackExchange.Redis | `2.9.32` |
| Newtonsoft.Json | `13.0.3` |
| AutoMapper | `13.0.1` |
| FluentValidation | `11.11.0` |
| Scrutor | `4.2.2` |
| LinqKit.Core | `1.2.8` |
| Polly | `8.5.2` |

### 测试包版本

| 包 | 版本 |
|---|------|
| Microsoft.NET.Test.Sdk | `17.13.0` |
| xunit | `2.9.3` |
| xunit.runner.visualstudio | `3.0.2` |
| Moq | `4.20.72` |
| coverlet.collector | `6.0.4` |
| Microsoft.EntityFrameworkCore.InMemory | `9.0.9` |
| FluentAssertions | `7.0.0` |
| NBomber | `6.2.0-beta.4` |

## 项目引用路径

- 使用相对路径 `..\..\` 格式
- 路径分隔符使用反斜杠 `\`

### 示例

```xml
<ItemGroup>
  <ProjectReference Include="..\..\CodeSpirit.Core\CodeSpirit.Core.csproj" />
  <ProjectReference Include="..\..\CodeSpirit.Shared\CodeSpirit.Shared.csproj" />
</ItemGroup>
```

## 工具包配置

对于仅作为开发工具使用的包，需添加资产限制：

```xml
<PackageReference Include="Microsoft.EntityFrameworkCore.Tools">
  <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
  <PrivateAssets>all</PrivateAssets>
</PackageReference>
```

## 迁移文件夹

API 项目如需 EF 迁移，应创建按数据库类型分离的迁移目录：

```xml
<ItemGroup>
  <Folder Include="Data\Migrations\MySql\" />
  <Folder Include="Data\Migrations\SqlServer\" />
</ItemGroup>
```

## 传递依赖处理

### 避免冗余引用

以下包通过项目引用传递可用，通常不需要显式引用：

- **通过 `CodeSpirit.Shared` 传递**：
  - `Newtonsoft.Json`
  - `Microsoft.EntityFrameworkCore.SqlServer`
  - `Pomelo.EntityFrameworkCore.MySql`
  - `LinqKit.Core`
  - `Microsoft.EntityFrameworkCore`
  - `RabbitMQ.Client`
  - `Aspire.RabbitMQ.Client`

- **通过 `CodeSpirit.ServiceDefaults` 传递**：
  - `Aspire.Seq`
  - `Aspire.StackExchange.Redis.DistributedCaching`

- **通过 `FrameworkReference` 提供**：
  - `Microsoft.AspNetCore.Http.Abstractions`（.NET 10）
  - `Microsoft.AspNetCore.Mvc.Core`（.NET 10）

如果项目确实需要这些包，应添加注释说明原因。

## 禁止事项

- ❌ **不要在 PackageReference 中指定 Version**（使用集中式包管理）
- ❌ 不要混用不同版本的同一包
- ❌ 不要使用 `<LangVersion>` 指定语言版本（使用框架默认）
- ❌ 不要在 PackageReference 中使用浮动版本 (如 `*`)
- ❌ 不要使用绝对路径引用项目
- ❌ 不要添加通过传递依赖已可用的包引用（除非有特殊需求）