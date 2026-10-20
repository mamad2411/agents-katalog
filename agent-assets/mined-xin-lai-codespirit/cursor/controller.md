---
description: CodeSpirit 控制器开发规范 - API控制器特性、路由、响应格式和操作特性
globs: 
  - "*Controller.cs"
  - "**/Controllers/**/*.cs"
alwaysApply: false
---

# 控制器开发规范

> 📖 API 设计规范（RESTful、响应格式、状态码等）参见 [api-design.mdc](mdc:.cursor/rules/api-design.mdc)

## 基本要求

| 要求 | 说明 |
|-----|------|
| 继承基类 | 继承当前项目中的 `ApiControllerBase` |
| 控制器特性 | 必须添加 `[DisplayName]` 和 `[Navigation]` 特性 |
| Action 特性 | 所有方法必须添加 `[DisplayName]` 特性 |
| 返回类型 | 所有方法返回 `ActionResult<ApiResponse<T>>` |
| 异常处理 | 不在 Action 中捕获异常，由统一过滤器处理 |
| 多参数处理 | 多个参数应封装为 DTO 模型 |
| XML 注释 | 控制器类和公共方法应添加 XML 文档注释 |

## 控制器类型

### 1. 标准业务控制器

```csharp
using CodeSpirit.Core;
using CodeSpirit.Core.Attributes;
using CodeSpirit.Core.Enums;
using CodeSpirit.Navigation.Resources;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel;

namespace CodeSpirit.IdentityApi.Controllers;

/// <summary>
/// 用户管理控制器
/// </summary>
[DisplayName("用户管理")]
[Navigation(Icon = "fa-solid fa-users", 
    PlatformType = PlatformType.Tenant, 
    TitleResourceKey = "Controller.Users", 
    TitleResourceType = typeof(NavigationResources))]
public class UsersController : ApiControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    /// <summary>
    /// 获取用户列表
    /// </summary>
    [HttpGet]
    [DisplayName("获取用户列表")]
    public async Task<ActionResult<ApiResponse<PageList<UserDto>>>> GetUsers(
        [FromQuery] UserQueryDto queryDto)
    {
        PageList<UserDto> users = await _userService.GetUsersAsync(queryDto);
        return SuccessResponse(users);
    }
}
```

### 2. 设置页面控制器

用于用户设置、系统配置等场景：

```csharp
[DisplayName("用户设置")]
[Navigation(Icon = "fa-solid fa-user-cog", Order = 150, PlatformType = PlatformType.Tenant)]
[SettingsPage(Title = "用户设置", Description = "管理用户偏好和系统配置")]
public class UserSettingsController : ApiControllerBase { }
```

### 3. 内部 API 控制器

用于微服务间内部通信，不对外暴露：

```csharp
/// <summary>
/// 内部用户信息访问控制器
/// </summary>
[DisableAggregator]  // 禁用 API 聚合
[DisplayName("内部用户信息")]
[Module("default")]  // 指定模块
[Route("api/identity/internal/users")]  // 自定义路由
[NoAudit("内部 API 不需要审计")]
public class InternalUsersController : ControllerBase { }  // 继承 ControllerBase
```

### 4. 匿名访问控制器

无需认证的公开 API：

```csharp
[AllowAnonymous]
[Navigation(Hidden = true)]  // 隐藏导航
[NoAudit("授权控制器不需要审计")]
public class AuthController : ApiControllerBase { }
```

## 控制器特性详解

### Navigation 特性

配置导航菜单和权限：

| 属性 | 类型 | 说明 |
|-----|------|------|
| `Icon` | string | Font Awesome 图标类名 |
| `PlatformType` | PlatformType | 平台类型：`Tenant`（租户端）/ `System`（系统端）|
| `Order` | int | 菜单排序（数字越小越靠前）|
| `Hidden` | bool | 是否隐藏导航菜单 |
| `TitleResourceKey` | string | 多语言标题资源键 |
| `TitleResourceType` | Type | 多语言资源类型 |

```csharp
// 完整示例
[Navigation(
    Icon = "fa-solid fa-users",
    PlatformType = PlatformType.Tenant,
    Order = 100,
    TitleResourceKey = "Controller.Users",
    TitleResourceType = typeof(NavigationResources))]
```

### Audit 特性

控制审计日志记录：

```csharp
// 启用审计
[Audit(EntityName = nameof(Department), LogRequestParams = true, LogResponseData = true)]

// 禁用审计
[NoAudit("授权控制器不需要审计")]
```

### 其他控制器特性

| 特性 | 用途 |
|-----|------|
| `[Module("name")]` | 指定模块名称，用于路由分组 |
| `[DisableAggregator]` | 禁用 API 聚合，用于内部 API |
| `[SettingsPage]` | 标记为设置页面控制器 |
| `[AllowAnonymous]` | 允许匿名访问 |
| `[Authorize]` | 显式要求认证 |

## 操作特性

除标准 CRUD 操作外，其他操作应添加 `Operation` 或其派生特性：

### 操作特性类型

| 特性 | 用途 | 典型场景 |
|-----|------|---------|
| `[Operation]` | 基础操作 | 行级操作（解锁、禁用、删除等）|
| `[HeaderOperation]` | 表头操作 | 新增、导入、AI 生成 |
| `[CrudDialogOperation]` | CRUD 弹窗操作 | 编辑、查看详情（简化配置）|

> 💡 批量操作通过 `[Operation]` 的 `isBatch` 参数实现，设置为 `true` 即可。

### Operation 特性参数

```csharp
[Operation(
    label: "解锁",           // 按钮文本
    actionType: "ajax",      // 操作类型：ajax, form, dialog, aiForm
    dialog: null,            // 弹窗配置（可选）
    confirmText: "确定要解除用户锁定吗？",  // 确认提示
    visibleOn: "lockoutEnd != null",       // 显示条件表达式
    // 多语言支持
    LabelResourceKey = "Operations.Unlock",
    LabelResourceType = typeof(OperationsResources),
    ConfirmTextResourceKey = "Operations.ConfirmUnlock",
    ConfirmTextResourceType = typeof(OperationsResources),
    // 图标
    Icon = "fa-solid fa-unlock")]
```

### 操作类型说明

| actionType | 说明 | 适用场景 |
|-----------|------|---------|
| `ajax` | 直接发送请求 | 简单操作（删除、状态切换）|
| `form` | 弹出表单 | 需要输入参数的操作 |
| `dialog` | 弹出对话框 | 复杂内容展示 |
| `aiForm` | AI 长任务表单 | AI 生成、批量处理 |

### 完整操作示例

#### 行级 Ajax 操作

```csharp
[HttpPut("{id}/unlock")]
[Operation("解锁", "ajax", null, "确定要解除用户锁定吗？", "lockoutEnd != null",
    LabelResourceKey = "Operations.Unlock",
    LabelResourceType = typeof(OperationsResources),
    ConfirmTextResourceKey = "Operations.ConfirmUnlock",
    ConfirmTextResourceType = typeof(OperationsResources),
    Icon = "fa-solid fa-unlock")]
[DisplayName("解锁用户")]
public async Task<ActionResult<ApiResponse>> UnlockUser(long id)
{
    await _userService.UnlockUserAsync(id);
    return SuccessResponse("用户已成功解锁。");
}
```

#### 带反馈结果的操作

```csharp
[HttpPost("{id}/resetRandomPassword")]
[Operation("重置密码", "ajax", null, "确定要重置密码吗？", "isActive == true", 
    LabelResourceKey = "Operations.ResetPassword",
    LabelResourceType = typeof(OperationsResources),
    FeedbackTitle = "重置密码结果",
    FeedbackBodyTpl = @"{
        'type': 'form',
        'body': [
            { 'type': 'button', 'label': '${newPassword}', 'icon': 'fa fa-copy', 
              'actionType': 'copy', 'content': '${newPassword}' }
        ]
    }")]
[DisplayName("重置随机密码")]
public async Task<ActionResult<ApiResponse>> ResetRandomPassword(long id)
{
    string newPassword = await _userService.ResetRandomPasswordAsync(id);
    return Ok(new { message = "密码已重置成功！", data = new { newPassword } });
}
```

#### 带重定向的操作

```csharp
[HttpPost("{id}/impersonate")]
[Operation("模拟登录", "ajax", null, "确定要模拟此用户登录吗？", "isActive == true",
    LabelResourceKey = "Operations.ImpersonateLogin",
    LabelResourceType = typeof(OperationsResources),
    Redirect = "/impersonate?token=${token}&tenantId=${tenantId}")]
[DisplayName("模拟用户登录")]
public async Task<ActionResult<ApiResponse<object>>> ImpersonateUser(long id) { }
```

#### AI 长任务操作

```csharp
[HttpPost("ai/generate")]
[HeaderOperation("AI生成题目", "aiForm",
    Icon = "fa-solid fa-magic",
    StatusApi = "/exam/api/Questions/ai/task-status",  // 状态查询 API
    PollingInterval = 2000,                            // 轮询间隔（毫秒）
    MaxPollingTime = 300000)]                          // 最大轮询时间
[DisplayName("AI生成题目")]
public async Task<ActionResult<ApiResponse<string>>> GenerateQuestionsAsync(
    [FromBody] GenerateQuestionsRequest request)
{
    var taskId = await _service.GenerateQuestionsAsync(request);
    return SuccessResponse(taskId);
}
```

#### 批量操作

```csharp
[HttpPost("batch/delete")]
[Operation("批量删除", "ajax", null, "确定要批量删除?", null, true,  // isBatch = true
    LabelResourceKey = "Common.BatchDelete",
    LabelResourceType = typeof(SharedResources),
    ConfirmTextResourceKey = "Common.ConfirmBatchDelete",
    ConfirmTextResourceType = typeof(SharedResources))]
[DisplayName("批量删除用户")]
public async Task<ActionResult<ApiResponse>> BatchDelete([FromBody] BatchOperationDto<long> request)
{
    var (successCount, failedIds) = await _userService.BatchDeleteAsync(request.Ids);
    return SuccessResponse($"成功删除 {successCount} 个用户！");
}
```

## 构造函数注入

```csharp
public class UsersController : ApiControllerBase
{
    private readonly IUserService _userService;
    private readonly IAuthService _authService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(
        IUserService userService,
        IAuthService authService,
        ILogger<UsersController> logger)
    {
        _userService = userService;
        _authService = authService;
        _logger = logger;
    }
}
```

> 💡 推荐使用主构造函数（C# 12+）简化注入代码。

## 注意事项

1. **无需添加 `[ApiController]` 和 `[Route]` 特性**：基类已包含默认配置
2. **路由自动推断**：默认按 `/{service-name}/api/[controller]` 格式
3. **Action 返回 DTO**：不要直接返回实体类
4. **异步方法**：所有 I/O 操作使用 `async/await`
5. **操作特性 Icon**：使用 Font Awesome 图标，格式为 `fa-solid fa-xxx`

## 参考文件

- 控制器基类: [ApiControllerBase.cs](mdc:Src/CodeSpirit.Shared/Controllers/ApiControllerBase.cs)
- 导航特性: [NavigationAttribute.cs](mdc:Src/CodeSpirit.Core/Attributes/NavigationAttribute.cs)
- 操作特性: [OperationAttribute.cs](mdc:Src/Components/CodeSpirit.Amis/Attributes/Buttons/OperationAttribute.cs)
- 用户控制器示例: [UsersController.cs](mdc:Src/CodeSpirit.IdentityApi/Controllers/UsersController.cs)
- API 设计规范: [api-design.mdc](mdc:.cursor/rules/api-design.mdc)
