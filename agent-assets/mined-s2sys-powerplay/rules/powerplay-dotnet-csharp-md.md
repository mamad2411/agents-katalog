---
name: dotnet-csharp
description: .NET and C# standards (applies to **/*.cs files)
globs: ["**/*.cs"]
alwaysApply: false
---

# .NET / C# Standards

Applied to all `.cs` files. Enforces ASP.NET Core 8 best practices.

## Controllers

**ALWAYS**:
- Include `[ApiController]` attribute
- Use `[Route("api/v1/[controller]")]` for versioning
- Return `IActionResult` or `ActionResult<T>`
- No business logic (only validation + delegation)
- Validate input with FluentValidation

**Example**:
```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class UsersController : ControllerBase
{
  private readonly IUserService _userService;
  private readonly IValidator<CreateUserRequest> _validator;
  private readonly ILogger<UsersController> _logger;

  public UsersController(
    IUserService userService,
    IValidator<CreateUserRequest> validator,
    ILogger<UsersController> logger)
  {
    _userService = userService;
    _validator = validator;
    _logger = logger;
  }

  [HttpPost]
  public async Task<ActionResult<UserResponse>> CreateUserAsync(
    [FromBody] CreateUserRequest request,
    CancellationToken cancellationToken)
  {
    var validationResult = await _validator.ValidateAsync(request, cancellationToken);
    if (!validationResult.IsValid)
      return BadRequest(validationResult.ToDictionary());

    var result = await _userService.CreateUserAsync(request, cancellationToken);
    return CreatedAtAction(nameof(GetUserAsync), new { id = result.Id }, result);
  }
}
```

**NEVER**:
- Put business logic in controllers
- Return `dynamic` or `object`
- Skip validation
- Use positional parameters (use `[FromBody]`, `[FromRoute]`, etc.)

## Services

**STRUCTURE**:
- Interface + implementation
- Scoped lifetime (not Singleton)
- Dependency injection for all dependencies
- All methods async with `CancellationToken`

**Example**:
```csharp
public interface IUserService
{
  Task<UserResponse> GetUserByIdAsync(int id, CancellationToken cancellationToken);
  Task<UserResponse> CreateUserAsync(CreateUserRequest request, CancellationToken cancellationToken);
  Task DeleteUserAsync(int id, CancellationToken cancellationToken);
}

public class UserService(IUserRepository repository, ILogger<UserService> logger)
  : IUserService
{
  public async Task<UserResponse> GetUserByIdAsync(int id, CancellationToken cancellationToken)
  {
    var user = await repository.GetByIdAsync(id, cancellationToken);
    if (user is null)
      throw new NotFoundException($"User {id} not found");

    return UserResponse.FromDomain(user);
  }

  // ... other methods
}
```

**ALWAYS**:
- Use primary constructors (C# 12)
- Accept `CancellationToken` in every async method
- Throw specific exceptions (not generic `Exception`)
- Map domain models to DTOs

**NEVER**:
- Use `ServiceLocator` pattern
- Have static dependencies
- Ignore `CancellationToken`

## Repositories

**PATTERN**: Dapper + parameterized queries

**Example**:
```csharp
public interface IUserRepository
{
  Task<User?> GetByIdAsync(int id, CancellationToken cancellationToken);
  Task<List<User>> GetAllAsync(CancellationToken cancellationToken);
  Task<int> CreateAsync(User user, CancellationToken cancellationToken);
  Task UpdateAsync(User user, CancellationToken cancellationToken);
  Task DeleteAsync(int id, CancellationToken cancellationToken);
}

public class UserRepository(IDbConnection connection, ILogger<UserRepository> logger)
  : IUserRepository
{
  public async Task<User?> GetByIdAsync(int id, CancellationToken cancellationToken)
  {
    const string sql = """
      SELECT UserId, Email, FirstName, LastName, CreatedDate
      FROM Users
      WHERE UserId = @UserId
    """;

    var user = await connection.QuerySingleOrDefaultAsync<User>(sql, new { UserId = id });
    return user;
  }

  public async Task<int> CreateAsync(User user, CancellationToken cancellationToken)
  {
    const string sql = """
      INSERT INTO Users (Email, FirstName, LastName, CreatedDate)
      VALUES (@Email, @FirstName, @LastName, @CreatedDate);
      SELECT SCOPE_IDENTITY();
    """;

    var id = await connection.ExecuteScalarAsync<int>(sql, user);
    return id;
  }
}
```

**ALWAYS**:
- Use parameterized queries (@parameter syntax)
- Use multi-line raw strings (""" """) for SQL
- Accept `CancellationToken` (though Dapper may not use it)
- Return domain models (not DTOs)

**NEVER**:
- String concatenation in SQL
- Sync methods (no `.Wait()`, always `async`)
- Mix business logic with data access

## Validation

**PATTERN**: FluentValidation

**Example**:
```csharp
public class CreateUserRequestValidator : AbstractValidator<CreateUserRequest>
{
  public CreateUserRequestValidator()
  {
    RuleFor(x => x.Email)
      .NotEmpty().WithMessage("Email is required")
      .EmailAddress().WithMessage("Invalid email format")
      .MaximumLength(100).WithMessage("Email must be ≤ 100 characters");

    RuleFor(x => x.FirstName)
      .NotEmpty().WithMessage("First name is required")
      .MaximumLength(50).WithMessage("First name must be ≤ 50 characters");

    RuleFor(x => x.Password)
      .NotEmpty().WithMessage("Password is required")
      .MinimumLength(8).WithMessage("Password must be ≥ 8 characters")
      .Matches(@"[A-Z]").WithMessage("Password must contain uppercase")
      .Matches(@"[0-9]").WithMessage("Password must contain digit");
  }
}
```

**ALWAYS**:
- One validator per request DTO
- Descriptive error messages
- Specific rules (length, format, pattern)

**NEVER**:
- Mix validation logic with services
- Validate in database
- Skip fluent validator

## Error Handling

**PATTERN**: ProblemDetails (RFC 7807)

**Example**:
```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class ExceptionHandlingMiddleware
{
  private readonly RequestDelegate _next;
  private readonly ILogger<ExceptionHandlingMiddleware> _logger;

  public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
  {
    _next = next;
    _logger = logger;
  }

  public async Task InvokeAsync(HttpContext context)
  {
    try
    {
      await _next(context);
    }
    catch (Exception ex)
    {
      _logger.LogError(ex, "Unhandled exception");
      await HandleExceptionAsync(context, ex);
    }
  }

  private static Task HandleExceptionAsync(HttpContext context, Exception exception)
  {
    context.Response.ContentType = "application/json";

    var problem = exception switch
    {
      NotFoundException => new ProblemDetails
      {
        Status = StatusCodes.Status404NotFound,
        Title = "Not Found",
        Detail = exception.Message,
      },
      ValidationException => new ProblemDetails
      {
        Status = StatusCodes.Status400BadRequest,
        Title = "Bad Request",
        Detail = exception.Message,
      },
      _ => new ProblemDetails
      {
        Status = StatusCodes.Status500InternalServerError,
        Title = "Internal Server Error",
        Detail = "An unexpected error occurred",
      }
    };

    context.Response.StatusCode = problem.Status ?? StatusCodes.Status500InternalServerError;
    return context.Response.WriteAsJsonAsync(problem);
  }
}
```

**ALWAYS**:
- Return `ProblemDetails` on error
- Log full exception with context
- Return user-friendly error messages
- Include error code for tracing

**NEVER**:
- Return raw exceptions
- Expose stack traces to clients
- Use 200 OK for errors

## Logging

**ALWAYS**:
- Use `ILogger<T>` injected via DI
- Use semantic logging (structured properties)
- Log at appropriate level (Error, Warning, Information, Debug)
- Include correlation IDs

**Example**:
```csharp
logger.LogInformation("User {UserId} created. Email: {Email}",
  user.Id, user.Email);

logger.LogError("Failed to create user. Email: {Email}. Error: {ErrorCode}",
  request.Email, ErrorCode.DuplicateEmail);
```

**NEVER**:
- Log passwords, tokens, API keys
- Use string interpolation in log messages
- Create new logger instances (inject ILogger)

## Async / Await

**ALWAYS**:
- Use `async`/`await` keyword
- Accept `CancellationToken` parameter
- Propagate cancellation token
- Avoid `.Wait()` and `.Result`

**Example**:
```csharp
public async Task<User> GetUserAsync(int id, CancellationToken cancellationToken)
{
  var user = await _repository.GetByIdAsync(id, cancellationToken);
  return user ?? throw new NotFoundException($"User {id} not found");
}
```

**NEVER**:
- Mix async and sync code
- Block on async calls (`.Wait()`)
- Ignore `CancellationToken`
- Use `async void` (except event handlers)

## Nullable Reference Types

**ALWAYS**:
- Enable `#nullable enable` in every file
- Annotate return types and parameters
- Use `T?` for nullable types
- Use null coalescing operators

**Example**:
```csharp
#nullable enable

public class User
{
  public int Id { get; set; }
  public string Email { get; set; } = string.Empty; // Non-nullable
  public string? PhoneNumber { get; set; }           // Nullable
}

public string GetDisplayName(User user)
{
  return user.PhoneNumber ?? "No phone";
}
```

**NEVER**:
- Use `#nullable disable`
- Leave return types unannotated
- Suppress warnings with `!` operator

## XML Documentation

**ALWAYS**:
- Document all public types and methods
- Include `<summary>`, `<param>`, `<returns>`
- Add `<exception>` for methods that throw
- Add `<example>` for utility methods

**Example**:
```csharp
/// <summary>
/// Gets a user by their ID.
/// </summary>
/// <param name="id">The user ID to retrieve.</param>
/// <param name="cancellationToken">Cancellation token.</param>
/// <returns>The user if found; throws NotFoundException otherwise.</returns>
/// <exception cref="NotFoundException">Thrown when user is not found.</exception>
public async Task<User> GetUserAsync(int id, CancellationToken cancellationToken)
{
  var user = await _repository.GetByIdAsync(id, cancellationToken);
  return user ?? throw new NotFoundException($"User {id} not found");
}
```

## Dependency Injection

**PROGRAM.CS**:
```csharp
var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IValidator<CreateUserRequest>, CreateUserRequestValidator>();

// Add controllers
builder.Services.AddControllers();

var app = builder.Build();
app.UseRouting();
app.UseEndpoints(e => e.MapControllers());
app.Run();
```

**ALWAYS**:
- Register interfaces (not implementations)
- Use appropriate lifetime (Transient/Scoped/Singleton)
- Register in `Program.cs` (not scattered)
- Inject only what's needed

---

**Last Updated**: 2026-04-09

