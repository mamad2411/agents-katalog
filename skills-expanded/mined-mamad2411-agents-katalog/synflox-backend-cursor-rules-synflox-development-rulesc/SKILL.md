---
alwaysApply: true
---
# SYNFLOX Development Rules & Architecture Guide

## Project Overview

**SYNFLOX** is a **Central Licensing System** designed to manage and control licensing for multiple external enterprise products (ERP, CRM, POS, HR, Inventory systems, etc.).

## Architecture Pattern

SYNFLOX follows **Clean Architecture** principles with a 4-layer structure:

```
┌─────────────────────────────────────┐
│         WebAPI (Presentation)        │  ← Controllers, Middleware, Configuration
├─────────────────────────────────────┤
│      Application (Business Logic)   │  ← DTOs, Service Interfaces, Mappings
├─────────────────────────────────────┤
│      Domain (Core Business)         │  ← Entities, Interfaces, Enums, Exceptions
├─────────────────────────────────────┤
│   Infrastructure (External Concerns)│  ← EF Core, Repositories, Services, Auth
└─────────────────────────────────────┘
```

### Layer Responsibilities

1. **Domain Layer**: Core business entities, interfaces, enums, exceptions. NO dependencies on other layers.
2. **Application Layer**: Business logic interfaces, DTOs, AutoMapper profiles. Depends ONLY on Domain.
3. **Infrastructure Layer**: Data access, external services, implementations. Depends on Domain and Application.
4. **WebAPI Layer**: Controllers, middleware, configuration. Depends on all other layers.

## Project Structure

```
SYNFLOX/
├── Domain/
│   ├── Entities/
│   │   ├── Authentication/        # Admin, AdminType, RefreshToken
│   │   ├── Licensing/             # Company
│   │   └── Common/                # AuditEntity, IBaseEntity
│   ├── Enums/                     # LicenseStatus
│   ├── Interfaces/                # Repository interfaces
│   └── Exceptions/                # Custom exceptions
│
├── Application/
│   ├── DTOs/
│   │   ├── Admin/                 # Admin DTOs
│   │   ├── Licensing/             # Company DTOs
│   │   └── Responses/             # ApiResponse, PaginationDto
│   ├── Services Interfaces/       # Service interfaces (ILicensingService, etc.)
│   └── Mapping/                   # AutoMapper profiles
│
├── Infrastructure/
│   ├── Repositories/              # Repository implementations
│   ├── Services/                  # Service implementations
│   ├── Configurations/            # EF Core configurations
│   ├── Context/                   # ApplicationDBContext
│   ├── Settings/                  # Configuration classes
│   ├── Resources/                 # Localization (.resx files)
│   └── InfrastructureServiceRegistration.cs
│
└── WebAPI/
    ├── Controllers/               # API controllers
    ├── Middleware/                # Custom middleware
    ├── Configurations/            # Swagger, CORS, etc.
    └── appsettings.json
```

## SOLID Principles

### Single Responsibility Principle (SRP)
**CRITICAL**: Each class should have only ONE reason to change.

#### ❌ WRONG - Violates SRP:
```csharp
// BAD: LicensingService handles both company management AND licensing
public interface ILicensingService
{
    // Company Management (WRONG - should be in ICompanyService)
    Task<CompanyDto> CreateCompanyAsync(CreateCompanyDto dto);
    Task<CompanyDto> UpdateCompanyAsync(Guid id, UpdateCompanyDto dto);
    
    // Licensing Operations (CORRECT)
    Task<CompanyDto> ActivateCompanyAsync(Guid id, DateTime expiryDate);
    Task<CompanyDto> SuspendCompanyAsync(Guid id);
}
```

#### ✅ CORRECT - Follows SRP:
```csharp
// GOOD: Separate services for separate responsibilities
public interface ICompanyService
{
    // Company Management ONLY
    Task<CompanyDto> CreateCompanyAsync(CreateCompanyDto dto);
    Task<CompanyDto> UpdateCompanyAsync(Guid id, UpdateCompanyDto dto);
    Task<CompanyDto?> GetCompanyByIdAsync(Guid id);
    Task<bool> DeleteCompanyAsync(Guid id);
}

public interface ILicensingService
{
    // Licensing Operations ONLY
    Task<CompanyDto> ActivateCompanyAsync(Guid id, DateTime expiryDate);
    Task<CompanyDto> SuspendCompanyAsync(Guid id);
    Task<CompanyStatusResponse> CheckCompanyStatusAsync(Guid id);
    Task<string> GenerateLicenseKeyAsync(Guid companyId);
    
    // Can use ICompanyService to get company data
}
```

### Separation of Concerns:
- **Entity Management** (CRUD) → Separate Service/Controller
- **Business Operations** (Activate, Suspend, etc.) → Separate Service/Controller
- **Cross-cutting concerns** (License Keys, Status) → Can depend on entity service

### Example Structure:
```
CompanyController + ICompanyService
├── POST /api/companies - Create
├── GET /api/companies - List
├── GET /api/companies/{id} - Get
├── PUT /api/companies/{id} - Update
└── DELETE /api/companies/{id} - Delete

LicensingController + ILicensingService
├── PUT /api/licensing/{id}/activate - Activate
├── PUT /api/licensing/{id}/suspend - Suspend
├── PUT /api/licensing/{id}/resume - Resume
├── PUT /api/licensing/{id}/extend - Extend
├── GET /api/licensing/{id}/status - Status
└── POST /api/licensing/{id}/license-key/generate - Generate Key
```

**Rule**: If a service handles both entity CRUD AND business operations, split it into two services.

## Rules for Creating New Features

### 1. Feature Implementation Checklist

When implementing a new feature, follow this exact order:

#### Step 1: Domain Layer
- [ ] Create entity in `Domain/Entities/{FeatureName}/`
- [ ] Entity MUST extend `AuditEntity<Guid>` or `AuditEntity<int>`
- [ ] Add data annotations (`[Required]`, `[StringLength]`, etc.)
- [ ] Create enum in `Domain/Enums/` if needed
- [ ] Create repository interface in `Domain/Interfaces/`
  - Interface MUST extend `IBaseRepository<Guid, EntityName>` or `IBaseRepository<int, EntityName>`
  - Add custom query methods if needed

#### Step 2: Application Layer
- [ ] Create DTOs in `Application/DTOs/{FeatureName}/`:
  - `Create{Entity}Dto` - For creation
  - `Update{Entity}Dto` - For updates (nullable properties)
  - `{Entity}Dto` - For responses
  - Request/Response DTOs as needed
- [ ] Add validation attributes to DTOs (`[Required]`, `[EmailAddress]`, etc.)
- [ ] Create service interface in `Application/Services Interfaces/`
  - Name: `I{Feature}Service`
  - Add XML documentation comments
  - Define all business logic methods
- [ ] Create AutoMapper profile in `Application/Mapping/`
  - Map Entity → DTO with ID encryption using `EncryptGuidConverter`
  - Map CreateDto → Entity (ignore Id, audit fields)
  - Map UpdateDto → Entity (conditional mapping)

#### Step 3: Infrastructure Layer
- [ ] Create repository implementation in `Infrastructure/Repositories/`
  - Implement interface
  - Extend `BaseRepository<Guid, Entity>` or `BaseRepository<int, Entity>`
  - Implement custom query methods
  - Always filter by `!IsDeleted` in custom queries
- [ ] Create service implementation in `Infrastructure/Services/`
  - Implement service interface
  - Inject: Repository, IMapper, ILocalizationService, IUnitOfWork, IIdEncryptionService (if needed)
  - Use `_localizer["Key"]` for all messages
  - Throw `BadRequestException` or `NotFoundException` with localized messages
- [ ] Create EF Core configuration in `Infrastructure/Configurations/`
  - Implement `IEntityTypeConfiguration<Entity>`
  - Add indexes (unique, composite, filtered)
  - Configure string lengths
- [ ] Register in `InfrastructureServiceRegistration.cs`:
  - Repository: `services.AddScoped<I{Entity}Repository, {Entity}Repository>();`
  - Service: `services.AddScoped<I{Feature}Service, {Feature}Service>();`
  - AutoMapper: Already registered via assembly scanning
- [ ] Add DbSet to `ApplicationDBContext.cs`:
  ```csharp
  public DbSet<Entity> Entities { get; set; }
  ```

#### Step 4: WebAPI Layer
- [ ] Create controller in `WebAPI/Controllers/`
  - Name: `{Feature}Controller`
  - Route: `[Route("api/{feature}")]`
  - Inject: Service, ILocalizationService, IIdEncryptionService
- [ ] Implement endpoints:
  - `POST /api/{feature}` - Create (SuperAdminOnly)
  - `GET /api/{feature}` - List with pagination (SuperAdminOnly)
  - `GET /api/{feature}/{id}` - Get by ID (SuperAdminOnly)
  - `PUT /api/{feature}/{id}` - Update (SuperAdminOnly)
  - `DELETE /api/{feature}/{id}` - Delete (SuperAdminOnly)
- [ ] Add authorization attributes:
  - `[Authorize(Policy = "SuperAdminOnly")]` for management endpoints
  - `[AllowAnonymous]` only for public endpoints (like status checks)
- [ ] Add validation:
  - `if (!ModelState.IsValid) return BadRequest(ModelState);` on POST/PUT
- [ ] Decrypt IDs in requests:
  - `var decryptedId = _idEncryption.Decrypt(id);`
- [ ] Use consistent response format:
  - `new ApiResponse<T>(statusCode, message, data)`
  - Use `_localizer["Key"]` for all messages

#### Step 5: Localization
- [ ] Add localization keys to `Infrastructure/Resources/SharedResource.resx` (English)
- [ ] Add same keys to `Infrastructure/Resources/SharedResource.ar.resx` (Arabic)
- [ ] Use prefix: `{Feature}.{Action}` (e.g., `Licensing.CompanyCreated`)
- [ ] Ensure proper Arabic translations

## ID Encryption Rules

### When to Encrypt IDs:
- ✅ **ALWAYS** encrypt IDs in GET responses (via AutoMapper `EncryptGuidConverter`)
- ✅ **ALWAYS** decrypt IDs in POST/PUT/DELETE requests (in Controller)
- ✅ **ALWAYS** encrypt IDs in response DTOs that contain entity IDs

### Implementation:
```csharp
// In AutoMapper Profile:
CreateMap<Entity, EntityDto>()
    .ForMember(d => d.Id,
        opt => opt.ConvertUsing<EncryptGuidConverter, Guid>(s => s.Id));

// In Controller:
var decryptedId = _idEncryption.Decrypt(id);
var result = await _service.GetByIdAsync(decryptedId);
```

## Authorization Rules

### Policies:
- `SuperAdminOnly` - Only SuperAdmin can access
- `AdminOrSuperAdmin` - Both Admin and SuperAdmin can access
- `AllowAnonymous` - Public endpoint (use sparingly, only for status checks)

### Usage:
```csharp
[HttpPost("companies")]
[Authorize(Policy = "SuperAdminOnly")]
public async Task<IActionResult> CreateCompany([FromBody] CreateCompanyDto request)
```

## Validation Rules

### DTO Validation:
- Use data annotations: `[Required]`, `[StringLength]`, `[EmailAddress]`, etc.
- Add `ErrorMessage` to attributes for better error messages

### Controller Validation:
- Always check `ModelState.IsValid` on POST/PUT endpoints
- Return `BadRequest(ModelState)` if invalid

### Service Validation:
- Validate business rules in service layer
- Throw `BadRequestException` for validation errors
- Throw `NotFoundException` for missing resources
- Always use localized messages: `_localizer["Key"]`

## Error Handling Rules

### Exception Types:
- `BadRequestException` - Validation errors, business rule violations
- `NotFoundException` - Resource not found
- Use localized messages: `throw new BadRequestException(_localizer["Key"]);`

### Controller Error Handling:
```csharp
try
{
    var result = await _service.MethodAsync();
    return Ok(new ApiResponse<T>(200, _localizer["Success"], result));
}
catch (Exception ex)
{
    return BadRequest(new ApiResponse<string>(400, ex.Message));
}
```

## Localization Rules

### Key Naming:
- Format: `{Feature}.{Action}` (e.g., `Licensing.CompanyCreated`, `Company.CompanyCreated`)
- Use descriptive names
- Keep consistent across EN and AR

### Usage:
- Always use `_localizer["Key"]` instead of hardcoded strings
- Add keys to both `SharedResource.resx` (EN) and `SharedResource.ar.resx` (AR)
- Ensure proper Arabic translations

### Frontend Language Selection (2025 Best Practices):

The backend supports **3 ways** for frontend to specify language (in priority order):

1. **Accept-Language Header** (Recommended - Most RESTful) ⭐: `Accept-Language: ar`
   - Standard HTTP header (RFC 7231) for content negotiation
   - RESTful API best practice
   - Example: `GET /api/companies` with header `Accept-Language: ar`
   - Frontend: `axios.defaults.headers.common['Accept-Language'] = 'ar'`

2. **Custom Header** (Recommended for SPAs): `X-Language: ar` or `X-Language: en`
   - Explicit control, clean URLs
   - Example: Header `X-Language: ar`
   - Frontend: `axios.defaults.headers.common['X-Language'] = 'ar'`

3. **Query Parameter** (Fallback - Not Recommended): `?lang=ar` or `?lang=en`
   - Supported for compatibility but not ideal
   - Clutters URLs, especially for POST/PUT/DELETE
   - Example: `GET /api/companies?lang=ar`

**Default:** English (`en`) if no language specified

**Frontend Implementation (Recommended):**
- Store user's language preference in localStorage
- Set `Accept-Language` header in axios defaults or interceptor
- Header automatically included in all requests
- Backend automatically detects and uses the correct language

**Why Headers > Query Parameters:**
- ✅ RESTful (standard HTTP for content negotiation)
- ✅ Semantically correct (language is metadata)
- ✅ Clean URLs (no clutter)
- ✅ Standard practice (GitHub, Stripe, AWS APIs use headers)

## Database Rules

### Entity Configuration:
- Create `{Entity}Configuration` class implementing `IEntityTypeConfiguration<Entity>`
- Add indexes for frequently queried fields
- Add unique indexes where needed
- Configure string lengths
- Use filtered indexes for nullable fields: `.HasFilter("[Field] IS NOT NULL")`

### Soft Delete:
- All entities extend `AuditEntity<Guid>` which includes `IsDeleted`
- Always filter by `!IsDeleted` in custom repository queries
- Use `DeleteAsync` method which performs soft delete

### Audit Fields:
- `CreatedTimestamp` - Set automatically on creation
- `UpdatedTimestamp` - Set automatically on update
- `DeletedTimestamp` - Set automatically on soft delete
- `IsDeleted` - Soft delete flag

## Service Implementation Rules

### Dependency Injection:
- Always inject through constructor
- Use interfaces, not concrete classes
- Required dependencies:
  - Repository
  - IMapper
  - ILocalizationService
  - IUnitOfWork
  - IIdEncryptionService (if working with IDs)

### Unit of Work:
- Always use `_unitOfWork.SaveChangesAsync()` after repository operations
- Don't call `SaveChangesAsync()` on repository directly

### Business Logic:
- Keep business logic in service layer, not in controllers
- Controllers should only handle HTTP concerns
- Use repository for data access only

## Code Quality Rules

### Naming Conventions:
- **Entities**: PascalCase, singular (e.g., `Company`, `Admin`)
- **DTOs**: PascalCase with suffix (e.g., `CompanyDto`, `CreateCompanyDto`)
- **Services**: PascalCase with prefix `I` for interfaces (e.g., `ILicensingService`)
- **Repositories**: PascalCase with suffix `Repository` (e.g., `CompanyRepository`)
- **Controllers**: PascalCase with suffix `Controller` (e.g., `LicensingController`)

### File Organization:
- One class per file
- File name matches class name
- Group related files in folders

### Documentation:
- Add XML documentation comments to public interfaces and methods
- Document complex business logic
- Add summary comments to classes

## What NOT to Do

### ❌ DO NOT:
- **Violate SRP**: Mix entity management (CRUD) with business operations in same service/controller
- Create User entities or OTP features (removed from system)
- Register email/SMS services (removed, not needed)
- Add email/OTP configurations to appsettings.json
- Mix business logic in controllers
- Access database directly from controllers
- Use hardcoded strings instead of localization
- Skip ID encryption/decryption
- Skip ModelState validation
- Skip authorization attributes
- Create entities that don't extend AuditEntity
- Forget to filter by `!IsDeleted` in queries
- Forget to use `_unitOfWork.SaveChangesAsync()`
- Put entity CRUD and business operations in the same service interface

## Example: Complete Feature Implementation

See the **Licensing** module as a reference implementation:
- `Domain/Entities/Licensing/Company.cs`
- `Application/DTOs/Licensing/*.cs`
- `Application/Services Interfaces/ILicensingService.cs`
- `Infrastructure/Repositories/CompanyRepository.cs`
- `Infrastructure/Services/LicensingService.cs`
- `Infrastructure/Configurations/CompanyConfiguration.cs`
- `WebAPI/Controllers/LicensingController.cs`

## Testing Checklist

Before considering a feature complete:
- [ ] All layers implemented (Domain, Application, Infrastructure, WebAPI)
- [ ] All DTOs created with validation
- [ ] Service interface and implementation complete
- [ ] Repository interface and implementation complete
- [ ] EF Core configuration added
- [ ] Service registrations added
- [ ] Controller endpoints implemented
- [ ] Authorization policies applied
- [ ] ID encryption/decryption working
- [ ] ModelState validation added
- [ ] Localization keys added (EN + AR)
- [ ] Error handling implemented
- [ ] Build successful (0 errors)
- [ ] Follows Clean Architecture principles

## Additional Notes

- The system uses **JWT authentication** for Admin access only
- All management endpoints require **SuperAdminOnly** authorization
- Public endpoints (like status checks) use **AllowAnonymous**
- The system supports **multi-language** responses (English + Arabic)
- All IDs are **encrypted** in responses and **decrypted** in requests
- The system uses **soft delete** pattern (IsDeleted flag)
- All timestamps are managed automatically via `AuditEntity`

---

**Last Updated:** 2025
**Project:** SYNFLOX Central Licensing System

