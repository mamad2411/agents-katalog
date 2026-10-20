---
description: CodeSpirit 服务类开发规范 - 服务接口、实现、生命周期和依赖注入
globs: 
  - "*Service.cs"
  - "**/Services/**/*.cs"
alwaysApply: false
---

# 服务（Service）类规则

## 基本要求

1. 确保服务类实现正确的接口和基类
2. 添加构造函数注释和 XML 文档注释
3. 服务类必须实现 [BaseCRUDIService.cs](mdc:Src/CodeSpirit.Shared/Services/BaseCRUDIService.cs) 或 [BaseCRUDService.cs](mdc:Src/CodeSpirit.Shared/Services/BaseCRUDService.cs)，应实现常见的查询逻辑
4. 服务接口必须实现 [IBaseCRUDIService.cs](mdc:Src/CodeSpirit.Shared/Services/IBaseCRUDIService.cs) 或 [IBaseCRUDService.cs](mdc:Src/CodeSpirit.Shared/Services/IBaseCRUDService.cs)
5. 服务类必须实现生命周期标记接口（IScopedDependency / ITransientDependency / ISingletonDependency）

## 服务类示例

```csharp
/// <summary>
/// 用户服务接口
/// </summary>
public interface IUserService : IBaseCRUDService<User, long, CreateUserDto, UpdateUserDto, UserQueryDto>
{
    /// <summary>
    /// 根据用户名获取用户
    /// </summary>
    /// <param name="username">用户名</param>
    /// <returns>用户信息</returns>
    Task<UserDto> GetByUsernameAsync(string username);
}

/// <summary>
/// 用户服务实现
/// </summary>
public class UserService : BaseCRUDService<User, long, CreateUserDto, UpdateUserDto, UserQueryDto>, 
    IUserService, IScopedDependency
{
    /// <summary>
    /// 初始化用户服务
    /// </summary>
    /// <param name="repository">用户仓储</param>
    /// <param name="mapper">对象映射器</param>
    public UserService(IRepository<User> repository, IMapper mapper) 
        : base(repository, mapper)
    {
    }
    
    public async Task<UserDto> GetByUsernameAsync(string username)
    {
        // 实现逻辑
    }
}
```

## 生命周期选择

- **IScopedDependency**: Scoped 生命周期（推荐大多数业务服务）
- **ITransientDependency**: Transient 生命周期（推荐无状态工具类）
- **ISingletonDependency**: Singleton 生命周期（推荐配置和缓存服务）

## 设置服务最佳实践

使用 `ISettingsService` 时，推荐使用 `[SettingsDto]` 特性简化 API 调用：

```csharp
// 1. 定义设置 DTO 并添加特性
using CodeSpirit.Settings.Attributes;

[SettingsDto("ThirdPartyLogin", "WeChat")]
public class WeChatLoginSettingsDto
{
    public string AppId { get; set; } = string.Empty;
    public string AppSecret { get; set; } = string.Empty;
}

// 2. 在服务中使用简化 API（无需手动传入 module/key）
public class AuthService : IScopedDependency
{
    private readonly ISettingsService _settingsService;
    
    public async Task<WeChatLoginSettingsDto> GetWeChatConfigAsync(string tenantId)
    {
        // 简化版 API：自动从 DTO 特性获取 module/key
        return await _settingsService.GetTenantSettingAsync<WeChatLoginSettingsDto>(tenantId) 
            ?? new WeChatLoginSettingsDto();
    }
    
    public async Task SaveWeChatConfigAsync(WeChatLoginSettingsDto dto, string tenantId)
    {
        // 简化版 API：自动从 DTO 特性获取 module/key
        await _settingsService.SetTenantSettingAsync(dto, tenantId, "更新微信配置");
    }
}
```

**优势：**
- 类型安全，编译时检查
- 避免模块名/配置键字符串不一致
- 配置键集中管理，修改只需改一处
- 反射结果自动缓存，性能优化

## 参考文件

- 服务基类: [BaseCRUDService.cs](mdc:Src/CodeSpirit.Shared/Services/BaseCRUDService.cs)
- 服务接口: [IBaseCRUDService.cs](mdc:Src/CodeSpirit.Shared/Services/IBaseCRUDService.cs)
- 依赖注入规范: [dependency-injection.mdc](mdc:.cursor/rules/dependency-injection.mdc)
- 设置组件文档: [codespirit-settings-guide-zh-CN.md](mdc:Docs/03-Core-Components/codespirit-settings-guide-zh-CN.md)
