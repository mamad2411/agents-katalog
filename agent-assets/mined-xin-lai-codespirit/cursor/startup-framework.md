---
description: CodeSpirit 统一启动框架规范 - API项目配置标准化
globs: "**/Configuration/*ApiConfiguration.cs,**/Program.cs"
alwaysApply: false
---

# 统一启动框架规范

## 快速开始

### Program.cs（标准模板）
```csharp
using CodeSpirit.ExamApi.Configuration;
using CodeSpirit.Shared.Startup;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;

var builder = WebApplication.CreateBuilder(args);

// 1. 注册服务
builder.AddCodeSpiritApi<ExamApiConfiguration>();

var app = builder.Build();

try
{
    // 2. 配置中间件和初始化数据库
    await app.UseCodeSpiritApiAsync<ExamApiConfiguration>();
    app.Run();
}
catch (Exception ex)
{
    var logger = app.Services.GetRequiredService<ILogger<Program>>();
    logger.LogError(ex, "服务启动过程中发生错误");
}
```

> ⚠️ **规范**：不要在 `Program.cs` 中添加额外配置，所有配置放在 API 配置类中。

---

## API 配置类

### 位置和命名
- **位置**：`{ProjectName}/Configuration/` 文件夹
- **命名**：`{ApiName}Configuration`（如 `ExamApiConfiguration`）
- **继承**：`BaseApiConfiguration`

### 最小配置类
```csharp
namespace CodeSpirit.ExamApi.Configuration;

public class ExamApiConfiguration : BaseApiConfiguration
{
    /// <summary>服务名称，用于 Aspire 服务发现</summary>
    public override string ServiceName => "exam";
    
    /// <summary>数据库连接字符串键名</summary>
    public override string ConnectionStringKey => "exam-api";
}
```

---

## 核心方法

### ConfigureServices - 服务注册

#### 简化配置方式（推荐）

使用扩展方法简化配置，减少重复代码：

```csharp
public override void ConfigureServices(IServiceCollection services, IConfiguration configuration)
{
    // ⚠️ 必须调用基类方法（初始化路径前缀配置）
    base.ConfigureServices(services, configuration);
    
    // 配置标准数据库服务（多数据库支持、仓储模式）
    this.ConfigureStandardDatabaseServices<ExamDbContext, MySqlExamDbContext, SqlServerExamDbContext>(
        services, configuration);
    
    // 配置标准基础设施服务（事件总线、HTTP客户端）+ 可选组件（多租户、设置管理）
    this.ConfigureStandardInfrastructureServices(services, configuration, (s, c) =>
    {
        s.AddCodeSpiritMultiTenant(c);
        s.AddSettingsManagerWithDatabase(c);
    });
    
    // 只配置特定业务服务
    services.AddLLMServices();
    AddExamSpecificServices(services);
}
```

#### 传统配置方式

如果需要更多控制，可以使用传统方式：

```csharp
public override void ConfigureServices(IServiceCollection services, IConfiguration configuration)
{
    // ⚠️ 必须调用基类方法（初始化路径前缀配置）
    base.ConfigureServices(services, configuration);
    
    // 配置多数据库支持（推荐方式）
    DatabaseMigrationHelper.ConfigureMultiDatabaseDbContext<
        ExamDbContext, MySqlExamDbContext, SqlServerExamDbContext>(
        services, configuration, ConnectionStringKey);
    
    // 注册仓储模式
    services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
    
    // 添加多租户支持
    services.AddCodeSpiritMultiTenant(configuration);
    
    // 其他服务注册...
}
```

#### 常用服务注册方法
| 方法 | 说明 |
|------|------|
| `services.AddCodeSpiritMultiTenant(configuration)` | 多租户支持 |
| `services.AddEventBus()` | 事件总线 |
| `services.AddCodeSpiritCaching(configuration)` | 统一缓存服务 |
| `services.AddLLMServices()` | LLM 服务 |
| `services.AddAiFormFillEndpoints()` | AI 表单填充端点 |
| `services.AddSettingsManagerWithDatabase(configuration)` | 设置管理 |
| `services.AddScheduledTasks()` | 定时任务 |
| `services.AddChartServices()` | 图表服务 |

#### 线程池配置（可选）
```csharp
// 高并发服务
ThreadPoolConfiguration.ConfigureThreadPool(
    ThreadPoolConfiguration.ServiceTier.High, 
    expectedInstances: 3, 
    logger);

// 服务等级：Low, Medium, High
```

---

### 中间件配置

#### 1. ConfigurePreAuthenticationMiddlewareAsync - 认证前
在认证之前执行，用于租户解析等：
```csharp
public override Task ConfigurePreAuthenticationMiddlewareAsync(WebApplication app)
{
    app.UseCodeSpiritMultiTenant();
    return Task.CompletedTask;
}
```

#### 2. ConfigurePreControllerMiddlewareAsync - 控制器前
在控制器映射之前执行：
```csharp
public override Task ConfigurePreControllerMiddlewareAsync(WebApplication app)
{
    // 通常审计由网关处理，API 服务不需要
    return Task.CompletedTask;
}
```

#### 3. ConfigureMiddlewareAsync - 自定义中间件
在通用中间件之后执行：

**简化配置方式（推荐）：**

```csharp
public override async Task ConfigureMiddlewareAsync(WebApplication app)
{
    // 配置标准中间件（聚合器）+ 可选组件（多租户、AI表单填充）
    await this.ConfigureStandardMiddlewareAsync(app, a =>
    {
        a.UseCodeSpiritMultiTenant();
        a.UseAiFormFillEndpoints();
    });
    
    // 只配置特定中间件
    app.MapHub<ExamHub>("/exam-hub");
}
```

**传统配置方式：**

```csharp
public override async Task ConfigureMiddlewareAsync(WebApplication app)
{
    // 多租户中间件
    app.UseCodeSpiritMultiTenant();
    
    // 聚合器中间件
    app.UseCodeSpiritAggregator();
    
    // AI 表单填充端点
    app.UseAiFormFillEndpoints();
    
    // SignalR Hub 映射
    app.MapHub<ExamHub>("/exam-hub");
    
    await Task.CompletedTask;
}
```

---

### InitializeDatabaseAsync - 数据库初始化

**简化配置方式（推荐）：**

```csharp
public override async Task InitializeDatabaseAsync(WebApplication app)
{
    // 使用标准数据库初始化方法
    // 自动应用迁移和初始化种子数据（如果 DbContext 实现了 IInitializableDbContext）
    await this.InitializeStandardDatabaseAsync<ExamDbContext, MySqlExamDbContext, SqlServerExamDbContext>(
        app, "ExamApi");
}
```

**传统配置方式：**

```csharp
public override async Task InitializeDatabaseAsync(WebApplication app)
{
    using var scope = app.Services.CreateScope();
    var services = scope.ServiceProvider;
    var logger = services.GetRequiredService<ILogger<ExamApiConfiguration>>();
    var configuration = services.GetRequiredService<IConfiguration>();
    
    try
    {
        // 1. 自动应用数据库迁移
        await DatabaseMigrationHelper.ApplyDatabaseMigrationsAsync<
            MySqlExamDbContext, 
            SqlServerExamDbContext>(
            services, configuration, logger, "ExamApi");
        
        // 2. 初始化种子数据
        var context = services.GetRequiredService<ExamDbContext>();
        await context.InitializeDatabaseAsync();
        
        logger.LogInformation("数据库初始化完成");
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "初始化数据库时发生错误：{Message}", ex.Message);
        throw;
    }
}
```

**注意：** 如果 DbContext 实现了 `IInitializableDbContext` 接口，标准初始化方法会自动调用 `InitializeDatabaseAsync()` 方法。

---

## 中间件执行顺序

```
请求 ──▶ CORS
         ↓
     ApplicationId 中间件
         ↓
  ┌──────────────────────────────────────┐
  │ ConfigurePreAuthenticationMiddlewareAsync │ ← 插入点1（认证前）
  │ 示例：多租户解析                          │
  └──────────────────────────────────────┘
         ↓
     Authentication & Authorization
         ↓
  ┌──────────────────────────────────────┐
  │ ConfigurePreControllerMiddlewareAsync    │ ← 插入点2（控制器前）
  │ 示例：审计日志                           │
  └──────────────────────────────────────┘
         ↓
     Controller Mapping
         ↓
     AMIS UI / Authorization / Navigation
         ↓
  ┌──────────────────────────────────────┐
  │ ConfigureMiddlewareAsync                 │ ← 插入点3（自定义）
  │ 示例：聚合器、SignalR Hub                │
  └──────────────────────────────────────┘
         ↓
     响应
```

---

## 统一框架自动配置

无需手动配置，框架自动完成：
- ✅ Aspire 服务默认配置（OpenTelemetry、健康检查等）
- ✅ Scrutor 自动依赖注入（`IScopedDependency` 等）
- ✅ JWT 认证配置
- ✅ Redis 分布式缓存
- ✅ AutoMapper 自动扫描
- ✅ CORS 配置
- ✅ 控制器配置（路径前缀路由约定）
- ✅ 仓储模式注册
- ✅ 异常处理中间件
- ✅ 数据库迁移应用

---

## 路径前缀配置

### PathPrefixOptions 属性
```csharp
// 基类已定义，从配置文件自动读取
public virtual PathPrefixOptions PathPrefixOptions { get; protected set; }
```

配置文件 `appsettings.json`：
```json
{
  "PathPrefix": {
    "Enabled": true,
    "Prefix": "/exam"
  }
}
```

---

## 完整配置类示例

### 简化配置示例（推荐）

```csharp
using CodeSpirit.ExamApi.Data;
using CodeSpirit.Shared.Performance;
using CodeSpirit.Shared.Startup;

namespace CodeSpirit.ExamApi.Configuration;

public class ExamApiConfiguration : BaseApiConfiguration
{
    public override string ServiceName => "exam";
    public override string ConnectionStringKey => "exam-api";
    
    public override void ConfigureServices(IServiceCollection services, IConfiguration configuration)
    {
        // 线程池配置（可选）
        var logger = services.BuildServiceProvider()
            .GetService<ILoggerFactory>()?.CreateLogger<ExamApiConfiguration>();
        ThreadPoolConfiguration.ConfigureThreadPool(
            ThreadPoolConfiguration.ServiceTier.High, 
            expectedInstances: 3, 
            logger);
        
        // 调用基类（初始化路径前缀）
        base.ConfigureServices(services, configuration);
        
        // 配置标准数据库服务（多数据库支持、仓储模式）
        this.ConfigureStandardDatabaseServices<ExamDbContext, MySqlExamDbContext, SqlServerExamDbContext>(
            services, configuration);
        
        // 配置标准基础设施服务（事件总线、HTTP客户端）+ 可选组件（多租户、设置管理）
        this.ConfigureStandardInfrastructureServices(services, configuration, (s, c) =>
        {
            s.AddCodeSpiritMultiTenant(c);
            s.AddSettingsManagerWithDatabase(c);
        });
        
        // 只配置特定业务服务
        services.AddLLMServices();
    }
    
    public override async Task ConfigureMiddlewareAsync(WebApplication app)
    {
        // 配置标准中间件（聚合器）+ 可选组件（多租户、AI表单填充）
        await this.ConfigureStandardMiddlewareAsync(app, a =>
        {
            a.UseCodeSpiritMultiTenant();
            a.UseAiFormFillEndpoints();
        });
    }
    
    public override async Task InitializeDatabaseAsync(WebApplication app)
    {
        // 使用标准数据库初始化方法
        await this.InitializeStandardDatabaseAsync<ExamDbContext, MySqlExamDbContext, SqlServerExamDbContext>(
            app, "ExamApi");
    }
}
```

### 传统配置示例

```csharp
using CodeSpirit.Aggregator;
using CodeSpirit.AiFormFill;
using CodeSpirit.ExamApi.Data;
using CodeSpirit.MultiTenant.Extensions;
using CodeSpirit.Shared.Data;
using CodeSpirit.Shared.Performance;
using CodeSpirit.Shared.Repositories;
using CodeSpirit.Shared.Startup;

namespace CodeSpirit.ExamApi.Configuration;

public class ExamApiConfiguration : BaseApiConfiguration
{
    public override string ServiceName => "exam";
    public override string ConnectionStringKey => "exam-api";
    
    public override void ConfigureServices(IServiceCollection services, IConfiguration configuration)
    {
        // 线程池配置
        var logger = services.BuildServiceProvider()
            .GetService<ILoggerFactory>()?.CreateLogger<ExamApiConfiguration>();
        ThreadPoolConfiguration.ConfigureThreadPool(
            ThreadPoolConfiguration.ServiceTier.High, 
            expectedInstances: 3, 
            logger);
        
        // 调用基类（初始化路径前缀）
        base.ConfigureServices(services, configuration);
        
        // 数据库配置
        DatabaseMigrationHelper.ConfigureMultiDatabaseDbContext<
            ExamDbContext, MySqlExamDbContext, SqlServerExamDbContext>(
            services, configuration, ConnectionStringKey);
        
        // 仓储模式
        services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
        
        // 多租户
        services.AddCodeSpiritMultiTenant(configuration);
        
        // 事件总线
        services.AddEventBus();
    }
    
    public override async Task ConfigureMiddlewareAsync(WebApplication app)
    {
        app.UseCodeSpiritMultiTenant();
        app.UseCodeSpiritAggregator();
        app.UseAiFormFillEndpoints();
        await Task.CompletedTask;
    }
    
    public override async Task InitializeDatabaseAsync(WebApplication app)
    {
        using var scope = app.Services.CreateScope();
        var services = scope.ServiceProvider;
        var logger = services.GetRequiredService<ILogger<ExamApiConfiguration>>();
        var configuration = services.GetRequiredService<IConfiguration>();
        
        try
        {
            await DatabaseMigrationHelper.ApplyDatabaseMigrationsAsync<
                MySqlExamDbContext, SqlServerExamDbContext>(
                services, configuration, logger, "ExamApi");
            
            var context = services.GetRequiredService<ExamDbContext>();
            await context.InitializeDatabaseAsync();
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "初始化数据库失败：{Message}", ex.Message);
            throw;
        }
    }
}
```

---

## 注意事项

| 规则 | 说明 |
|------|------|
| ✅ 调用 `base.ConfigureServices()` | 必须调用以初始化路径前缀配置 |
| ✅ 使用扩展方法简化配置 | 推荐使用 `ConfigureStandardDatabaseServices`、`ConfigureStandardInfrastructureServices` 等扩展方法 |
| ✅ 使用回调委托配置可选组件 | 通过委托参数显式配置可选组件，避免反射调用 |
| ✅ 使用 `DatabaseMigrationHelper` | 简化多数据库配置 |
| ✅ 实现 `IInitializableDbContext` | 如果 DbContext 需要初始化种子数据，实现此接口 |
| ✅ 异步方法返回 `Task` | 所有中间件配置方法都是异步的 |
| ❌ 在 Program.cs 添加配置 | 所有配置放在 API 配置类中 |
| ❌ 重复注册框架已有服务 | 检查自动配置列表避免重复 |
| ❌ 使用反射调用扩展方法 | 反射调用失去编译时类型安全，且性能较差 |

---

## 可选组件配置最佳实践

### ❌ 错误方式：使用反射调用

```csharp
// ❌ 不推荐：使用反射动态调用扩展方法
private static void TryInvokeExtensionMethod(IServiceCollection services, 
    string namespaceName, string className, string methodName, IConfiguration configuration)
{
    var assembly = AppDomain.CurrentDomain.GetAssemblies()
        .FirstOrDefault(a => a.GetTypes().Any(t => t.Namespace == namespaceName));
    var type = assembly.GetType($"{namespaceName}.{className}");
    var method = type.GetMethod(methodName, BindingFlags.Public | BindingFlags.Static);
    method?.Invoke(null, new object[] { services, configuration });
}
```

**问题**：
- ❌ 编译时无法检测方法签名变更
- ❌ 运行时性能损耗
- ❌ IDE 无法追踪引用关系
- ❌ 错误被默默吞掉，不易察觉
- ❌ 重构时容易遗漏

### ✅ 正确方式：使用回调委托

```csharp
// ✅ 推荐：通过回调委托配置可选组件
public static void ConfigureStandardInfrastructureServices(
    this BaseApiConfiguration config,
    IServiceCollection services,
    IConfiguration configuration,
    Action<IServiceCollection, IConfiguration>? additionalConfiguration = null)
{
    // 核心服务（必需）
    services.AddEventBus();
    services.AddHttpClient();
    
    // 可选组件通过委托配置
    additionalConfiguration?.Invoke(services, configuration);
}
```

**调用示例**：

```csharp
// 显式配置需要的可选组件
this.ConfigureStandardInfrastructureServices(services, configuration, (s, c) =>
{
    s.AddCodeSpiritMultiTenant(c);        // 多租户支持
    s.AddSettingsManagerWithDatabase(c);  // 设置管理
});
```