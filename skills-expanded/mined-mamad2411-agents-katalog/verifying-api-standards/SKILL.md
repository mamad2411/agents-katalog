---
name: verifying-api-standards
description: Use when checking, auditing, or reviewing newly created or modified API endpoints, controllers, services, DTOs, or database transaction patterns in the Hackathon .NET backend
---

# Verifying API Standards Skill

## Overview

Use this skill to audit code modifications, pull requests, or newly created API endpoints to ensure they conform perfectly to the project's standards.

**Base rules are defined in `create-api-skill/SKILL.md`.** This skill builds on top of those rules to check compliance. Always verify against BOTH sets of rules.

## Auditing Checklist

When auditing API changes, verify each of the following points:

### 1. Controller Layer Standards
- **Inheritance & Attributes**: The controller must use `[ApiController]` and route template matching the module.
- **RESTful Endpoints**:
  - The endpoints must be designed using **RESTful patterns** (use plural nouns for resource naming, e.g., `/api/events`, `/api/users`).
  - Do NOT use verbs in basic CRUD endpoints (e.g., avoid `/api/events/delete-event/{id}` or `/api/events/get-events`).
  - Correct HTTP methods must be mapped to actions (GET for read, POST for create, PUT/PATCH for update, DELETE for delete).
- **Pattern Matching**: The controller template must match `AuthController.cs` (constructor injection of service interface, endpoints call service methods).
- **Direct Queries**: The controller **must NOT** query the database or DbContext directly.
- **Response Wrapper**: 
  - Regular APIs: Action must wrap the service result in `ApiResponseFactory.Base(result, traceId: HttpContext.TraceIdentifier)`.
  - Paginated APIs: Action must return `Ok(result)` directly.
- **PascalCase Response Envelope**: The root wrapper properties of both success responses and error responses must be PascalCase (e.g. `IsSuccess`, `IsFailed`, `Status`, `Error`, `TraceId`, `TimestampUtc`, `Data`, `Message`). Middleware error response properties are exactly: `Title`, `Status`, `Message` (not `Detail`), `MessageCode`, `Errors`, `TraceId`, `TimestampUtc`.
- **Documentation Error Codes Table**: Ensure markdown API specification documents standard tables for error codes. `messageCode` must contain the exact C# custom exception `MessageCode` value, and `message/detail` must contain the exact string returned in the exception `Message` instead of arbitrary localized translations.
- **GUID Constraints**: Any route parameter representing GUID must include the `:guid` constraint (e.g. `[HttpGet("{id:guid}")]`).

### 2. Service & Interface Layer Standards
- **Interface Segregation**: Every service method must be declared in `IService.cs` before implementing it in `Service.cs`.
- **Database Context Usage**: The database context must be injected and queried ONLY inside the Service layer.
- **Exceptions**: Use existing project-defined exception classes (e.g. `NotFoundException`, `BadRequestException`, `ConflictException`) instead of generic exceptions.
- **Transactions**: Any state mutation (Create, Update, Delete) or multi-step database action **must be wrapped in a database transaction** using `await _dbContext.Database.BeginTransactionAsync()` inside the Service layer.
- **Null Safety** (see `create-api-skill/SKILL.md` Null Safety Rules):
  - **NotFound check**: Every `FirstOrDefaultAsync()` that looks up an entity MUST have a null check immediately after — throw `NotFoundException` if null. Không được để NullReferenceException → 500.
  - **Empty list**: Nếu query không tìm thấy kết quả nào, trả về list rỗng (paginated: `totalCount = 0`), không throw exception.
  - **`?.` + LINQ chain**: Nếu dùng `?.` để truy cập property rồi gọi LINQ method, PHẢI có `?.` ở MỖI bước LINQ. Pattern `obj?.Prop.Where(...)` là **BUG** vì `obj?.Prop` → null → `.Where()` throw `ArgumentNullException`.
  - **Include trước khi truy cập navigation**: Entity có navigation property collection mà không Include → có thể null → crash. Luôn kiểm tra xem đã Include đủ chưa hoặc thêm null check.

### 3. Request & Response DTOs
- **Entity Exposure**: Never return Entity Framework database models directly to the controller or client. Always project them to a specific DTO in `Response.cs`.
- **FluentValidation**: Request validation must be performed in dedicated validator classes under `Hackathon.Service/Validations/<Module>/` using **FluentValidation** (e.g. `ChangePasswordRequestValidator.cs` or similar validators inheriting from `AbstractValidator<T>`).
- **No DataAnnotations Validation**: Do not use validation attributes (like `[Required]`, `[EmailAddress]`, `[Range]`, `[Compare]`) directly on Request DTO classes. Request DTO properties should remain clean.

### 4. Pagination Standards
- **Use PaginationRequest Class**: All paginated APIs and endpoints must utilize the shared `PaginationRequest` class (defined in `Hackathon.Service.Models`).
  - Search/List DTO classes (e.g. `GetEventsRequest`) **must inherit** from `PaginationRequest`.
  - Controller actions that accept page index and page size in query parameters **must bind** them as `[FromQuery] PaginationRequest paginationRequest`.
- **Return Type**: The service method for a paginated query must return `Task<BasePaginationResponse>` directly.
- **Page Limits**: Ensure pagination parameters from `PaginationRequest` are sanitized:
  ```csharp
  var pageIndex = paginationRequest.PageIndex <= 0 ? 1 : paginationRequest.PageIndex;
  var pageSize = paginationRequest.PageSize <= 0 ? 10 : Math.Min(paginationRequest.PageSize, 100);
  ```
- **Skip & Take implementation**: Use `.Skip((pageIndex - 1) * pageSize).Take(pageSize)` correctly after retrieving the total count.
- **Factory Return**: The service must wrap and return the paged result via:
  ```csharp
  return ApiResponseFactory.BasePagination(items, pageIndex, pageSize, totalCount);
  ```

---

## Standard Reference Files

Use these files in the repository to compare patterns:
- **Controller Template**: `Hackathon.Api/Controllers/AuthController.cs`
- **Service Template**: `Hackathon.Service/Auths/Service.cs` (ChangePassword method)
- **Validation Reference**: `Hackathon.Service/Validations/Auth/ChangePasswordRequestValidator.cs`

---

## Common Violations and How to Suggest Fixes

| Violation Symptom | Correct Suggestion / Action |
| --- | --- |
| Controller calling `_dbContext.Users` or `_dbContext.EmailVerifications` | Instruct to move query logic to `Service.cs` and inject service interface in controller |
| Controller wrapping paginated response in `BasePagination` again | Change controller return to `Ok(result)` and wrap inside the Service instead |
| Request DTO classes containing DataAnnotations validation attributes | Request DTO properties must be clean. Suggest moving the validation rules to a dedicated FluentValidation class under `Hackathon.Service/Validations/<Module>/` |
| Service method mutating DB state without `BeginTransactionAsync()` | Wrap the save operations in `try-catch` block with transaction commit & rollback |
| Route parameter `[HttpGet("events/{eventId}")]` missing guid check | Suggest changing to `[HttpGet("events/{eventId:guid}")]` |
| Service registering is missing in DI | Add `builder.Services.AddScoped<IService, Service>();` in `Program.cs` |
| `FirstOrDefaultAsync()` không có null check → truy cập property trên null → 500 | Thêm `if (entity == null) throw new NotFoundException("...");` ngay sau dòng query |
| `obj?.Collection.Where(...)` — `?.` chỉ bảo vệ property, `.Where()` vẫn gọi trên null → 500 | Thêm `?.` ở MỖI bước LINQ: `?.Where()`, `?.Select()`, `?.FirstOrDefault()`, v.v. |
| Navigation property collection bị null vì thiếu `.Include()` → 500 | Thêm `.Include(x => x.Collection)` vào query hoặc null check trước khi truy cập |

## Reporting Template

When auditing, structure your feedback using this format:

1. **Overview**: Summary of the changes and general assessment.
2. **Violations Found**: Bulleted list of violations grouped by layer (Controller, Service, DTO). Detail exactly what is wrong and what is missing.
3. **DI Registrations Check**: Verify if the service needs registration in `Program.cs`.
4. **Corrected Code**: Provide code snippets showing exactly how the files must be written to follow standard.
