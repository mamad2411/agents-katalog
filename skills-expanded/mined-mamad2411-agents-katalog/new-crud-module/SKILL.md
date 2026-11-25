---
name: new-crud-module
description: 新增 CRUD 模块端到端流程 — 从 Entity 到前端页面的完整步骤
globs: "**/*.cs,**/*.ts,**/*.vue"
---

# 新增 CRUD 模块 — 端到端操作指南

> 本 Skill 指导你为 PMS 项目新增一个完整的 CRUD 业务模块。
> 按照以下 8 步顺序执行，每步完成后标记 todo。

## 前置条件
- 已读 `AGENTS.md` 和 `memory-bank/architecture.md`
- 已明确模块名称（如 `Equipment`）、核心字段、是否需要数据范围过滤

## Step 1: 创建 Entity（领域层）

文件：`PMS.Domain/Entities/{Module}Entity.cs`

```csharp
namespace PMS.Domain.Entities;

public class {Module}Entity
{
    public long Id { get; set; }
    // 业务字段...
    public string CreatedAt { get; set; } = "";
    public string UpdatedAt { get; set; } = "";
}
```

**规则**：Entity 不引用 Infrastructure，不含业务逻辑。

## Step 2: 创建 DTO（应用层）

文件：`PMS.Application/Models/{Module}/{Module}Dto.cs`

```csharp
namespace PMS.Application.Models.{Module};

public class {Module}ItemDto { /* 列表展示字段 */ }
public class {Module}Upsert { /* 新增/编辑输入字段 */ }
public class {Module}Query
{
    public string? Keyword { get; set; }
    public int Page { get; set; } = 1;
    public int Size { get; set; } = 20;
    // 数据范围字段（如需）
    public List<string>? AccessibleHospitalNames { get; set; }
    public List<string>? AccessiblePersonnelNames { get; set; }
}
public class {Module}SummaryDto { /* 统计汇总 */ }
```

## Step 3: 创建 Service 接口（应用层）

文件：`PMS.Application/Contracts/{Module}/I{Module}Service.cs`

```csharp
using PMS.Application.Models;
using PMS.Application.Models.{Module};

namespace PMS.Application.Contracts.{Module};

public interface I{Module}Service
{
    Task<{Module}SummaryDto> GetSummaryAsync(CancellationToken ct = default);
    Task<PagedResult<{Module}ItemDto>> QueryAsync({Module}Query query, CancellationToken ct = default);
    Task<{Module}ItemDto?> GetByIdAsync(long id, CancellationToken ct = default);
    Task<{Module}ItemDto> CreateAsync({Module}Upsert input, CancellationToken ct = default);
    Task<{Module}ItemDto?> UpdateAsync(long id, {Module}Upsert input, CancellationToken ct = default);
    Task<bool> DeleteAsync(long id, CancellationToken ct = default);
}
```

## Step 4: 创建 Service 实现（基础设施层）

文件：`PMS.Infrastructure/Services/InMemory{Module}Service.cs`

遵循 `PMS.Infrastructure/Services/.instructions.md` 中的模式：
- `SqliteTableStore.LoadAll<T>` 静态初始化
- `lock (SyncRoot)` 保护读写
- LINQ 查询链 + 分页
- 私有 `MapToDto` 方法

标杆参考：`InMemoryWorkHoursService.cs`

## Step 5: 注册 DI

文件：`PMS.API/Program.cs`

在其他服务注册行附近添加：
```csharp
builder.Services.AddSingleton<I{Module}Service, InMemory{Module}Service>();
```

## Step 6: 创建 Controller（API 层）

文件：`PMS.API/Controllers/{Module}/{Module}Controller.cs`

遵循 `PMS.API/Controllers/.instructions.md` 中的模式：
- primary constructor 注入
- `ApiResponse<T>` 包装
- `HospitalScopeHelper` 数据隔离（如需）
- 标准端点：GET summary, GET list, GET {id}, POST, PUT {id}, DELETE {id}

标杆参考：`WorkHours/WorkHoursController.cs`

## Step 7: 创建前端类型 + API 客户端

类型文件：`pms-web/src/types/{module}.ts`
```typescript
export interface {Module}Item { id: number; /* ... */ }
export interface {Module}Upsert { /* ... */ }
export interface {Module}Query { keyword?: string; page?: number; size?: number; }
export interface {Module}Summary { total: number; /* ... */ }
```

API 文件：`pms-web/src/api/modules/{module}.ts`

遵循 `pms-web/src/api/.instructions.md` 中的模式：
- `fetchXxxSummary`, `fetchXxxList`, `createXxx`, `updateXxx`, `deleteXxx`

标杆参考：`modules/workhours.ts`

## Step 8: 创建前端页面

文件：`pms-web/src/views/{module}/{Module}View.vue`

遵循 `pms-web/src/views/.instructions.md` 中的模式：
- `.page-shell` 结构
- 统计卡片 + 筛选区 + 数据表格 + 分页
- 权限按钮守卫

别忘了在 `pms-web/src/router/` 中注册路由。

标杆参考：`workhours/WorkHoursView.vue`

## 验证清单

- [ ] `dotnet build PMS.slnx` 通过
- [ ] `cd pms-web && npm run build` 通过
- [ ] 新模块的 CRUD 端点在 Swagger 中可见
- [ ] 列表页正常加载、筛选生效
- [ ] 新增/编辑/删除操作正常
- [ ] 数据范围过滤生效（非 manager 角色看不到越权数据）
- [ ] 更新 `memory-bank/progress.md`
