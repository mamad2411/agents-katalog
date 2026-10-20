---
name: test-standards
description: Unit testing standards (applies to **/*Tests.cs, **/*.spec.ts files)
globs: ["**/*Tests.cs", "**/*.spec.ts"]
alwaysApply: false
---

# Testing Standards

Applied to all test files. Enforces quality and consistency in unit tests.

## Naming Convention

**Pattern**: `MethodName_Scenario_ExpectedResult`

```csharp
[Fact]
public async Task GetUserByIdAsync_WithValidId_ReturnsUser()
{
  // Arrange
  var userId = 1;

  // Act
  var result = await _service.GetUserByIdAsync(userId);

  // Assert
  Assert.NotNull(result);
  Assert.Equal("john@example.com", result.Email);
}

[Fact]
public async Task GetUserByIdAsync_WithInvalidId_ThrowsNotFoundException()
{
  // Arrange
  var userId = 99999;

  // Act & Assert
  var exception = await Assert.ThrowsAsync<NotFoundException>(
    () => _service.GetUserByIdAsync(userId)
  );
  Assert.Equal("User 99999 not found", exception.Message);
}
```

## Test Structure (AAA Pattern)

```
Arrange → Setup test data and mocks
Act     → Execute the method being tested
Assert  → Verify the results
```

```csharp
[Fact]
public async Task CreateUserAsync_WithValidRequest_CreatesAndReturnsUser()
{
  // ═══════════ ARRANGE ═════════════
  var request = new CreateUserRequest
  {
    Email = "john@example.com",
    FirstName = "John",
    LastName = "Doe",
    Password = "SecurePass123!"
  };

  var mockRepository = new Mock<IUserRepository>();
  mockRepository
    .Setup(r => r.CreateAsync(It.IsAny<User>(), It.IsAny<CancellationToken>()))
    .ReturnsAsync(1);  // Return new user ID

  var service = new UserService(mockRepository.Object, _logger);

  // ═══════════ ACT ═════════════
  var result = await service.CreateUserAsync(request, CancellationToken.None);

  // ═══════════ ASSERT ═════════════
  Assert.NotNull(result);
  Assert.Equal("john@example.com", result.Email);
  mockRepository.Verify(
    r => r.CreateAsync(It.IsAny<User>(), It.IsAny<CancellationToken>()),
    Times.Once
  );
}
```

## Coverage Requirements

**ALWAYS TEST**:
- ✅ Happy path (normal flow)
- ✅ Edge cases (boundary values, empty collections)
- ✅ Null inputs (null checks)
- ✅ Exception handling (invalid data throws expected exception)
- ✅ Integration points (mocked dependencies are called correctly)

**EXAMPLE — COMPREHENSIVE TEST SUITE**:

```csharp
public class UserServiceTests
{
  private readonly Mock<IUserRepository> _repositoryMock;
  private readonly ILogger<UserService> _logger;
  private readonly UserService _service;

  public UserServiceTests()
  {
    _repositoryMock = new Mock<IUserRepository>();
    _logger = TestUtilities.CreateMockLogger<UserService>();
    _service = new UserService(_repositoryMock.Object, _logger);
  }

  // ═══════════════════════════════════════════════════════
  // HAPPY PATH TESTS
  // ═══════════════════════════════════════════════════════

  [Fact]
  public async Task GetUserByIdAsync_WithValidId_ReturnsUser()
  {
    // Arrange
    var userId = 1;
    var expected = new User { Id = 1, Email = "john@example.com" };
    _repositoryMock.Setup(r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()))
      .ReturnsAsync(expected);

    // Act
    var result = await _service.GetUserByIdAsync(userId, CancellationToken.None);

    // Assert
    Assert.NotNull(result);
    Assert.Equal(expected.Email, result.Email);
    _repositoryMock.Verify(r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()), Times.Once);
  }

  // ═══════════════════════════════════════════════════════
  // EDGE CASE TESTS
  // ═══════════════════════════════════════════════════════

  [Theory]
  [InlineData(0)]
  [InlineData(-1)]
  [InlineData(int.MaxValue)]
  public async Task GetUserByIdAsync_WithVariousIds_ReturnsOrThrows(int userId)
  {
    // This test validates behavior across boundary values
    _repositoryMock.Setup(r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()))
      .ReturnsAsync((User)null);

    var exception = await Assert.ThrowsAsync<NotFoundException>(
      () => _service.GetUserByIdAsync(userId, CancellationToken.None)
    );

    Assert.NotNull(exception);
  }

  // ═══════════════════════════════════════════════════════
  // NULL INPUT TESTS
  // ═══════════════════════════════════════════════════════

  [Fact]
  public async Task CreateUserAsync_WithNullRequest_ThrowsArgumentNullException()
  {
    // Act & Assert
    var exception = await Assert.ThrowsAsync<ArgumentNullException>(
      () => _service.CreateUserAsync(null!, CancellationToken.None)
    );
    Assert.Equal("request", exception.ParamName);
  }

  // ═══════════════════════════════════════════════════════
  // EXCEPTION HANDLING TESTS
  // ═══════════════════════════════════════════════════════

  [Fact]
  public async Task GetUserByIdAsync_WithNonExistentId_ThrowsNotFound()
  {
    // Arrange
    _repositoryMock.Setup(r => r.GetByIdAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()))
      .ReturnsAsync((User)null);

    // Act & Assert
    await Assert.ThrowsAsync<NotFoundException>(
      () => _service.GetUserByIdAsync(999, CancellationToken.None)
    );
  }

  [Fact]
  public async Task GetUserByIdAsync_WhenRepositoryThrowsException_PropagatesException()
  {
    // Arrange
    var exception = new InvalidOperationException("Database error");
    _repositoryMock.Setup(r => r.GetByIdAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()))
      .ThrowsAsync(exception);

    // Act & Assert
    var thrown = await Assert.ThrowsAsync<InvalidOperationException>(
      () => _service.GetUserByIdAsync(1, CancellationToken.None)
    );
    Assert.Equal("Database error", thrown.Message);
  }
}
```

## Mocking Best Practices

**C# (Moq)**:
```csharp
// ✅ Mock dependencies
var repositoryMock = new Mock<IUserRepository>();
repositoryMock
  .Setup(r => r.GetByIdAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()))
  .ReturnsAsync(new User { Id = 1 });

// ✅ Verify calls
repositoryMock.Verify(
  r => r.GetByIdAsync(1, It.IsAny<CancellationToken>()),
  Times.Once
);

// ✅ Mock exceptions
repositoryMock
  .Setup(r => r.GetByIdAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()))
  .ThrowsAsync(new Exception("Error"));

// ✅ Use It.IsAny for flexibility
repositoryMock
  .Setup(r => r.CreateAsync(It.IsAny<User>(), It.IsAny<CancellationToken>()))
  .ReturnsAsync(1);
```

**TypeScript (Jasmine)**:
```typescript
// ✅ Mock service
const userServiceSpy = jasmine.createSpyObj('UserService', ['getUsers', 'getUserById']);
userServiceSpy.getUsers.and.returnValue(of([{ id: 1, name: 'John' }]));

// ✅ Verify calls
expect(userServiceSpy.getUsers).toHaveBeenCalled();
expect(userServiceSpy.getUserById).toHaveBeenCalledWith(1);

// ✅ Mock errors
userServiceSpy.getUserById.and.returnValue(
  throwError(() => new Error('Not found'))
);
```

## What NOT to Test

**NEVER TEST**:
- ❌ Private methods (test public behavior instead)
- ❌ Third-party libraries (assume they work)
- ❌ Framework code (Angular, ASP.NET Core internals)
- ❌ Configuration files (test the code that reads them)

**EXAMPLE — DON'T DO THIS**:
```csharp
// ❌ BAD: Testing private method
[Fact]
public void FormatEmail_WithInput_ReturnsFormatted()
{
  var reflection = typeof(UserService)
    .GetMethod("FormatEmail", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
  var result = (string)reflection.Invoke(_service, new object[] { "JOHN@EXAMPLE.COM" });
  Assert.Equal("john@example.com", result);
}

// ✅ GOOD: Test through public method
[Fact]
public void CreateUser_WithUppercaseEmail_NormalizesEmail()
{
  var result = _service.CreateUser(new CreateUserRequest { Email = "JOHN@EXAMPLE.COM" });
  Assert.Equal("john@example.com", result.Email);
}
```

## Test Fixtures & Setup

**REUSABLE SETUP**:
```csharp
public class UserServiceTestFixture : IDisposable
{
  public Mock<IUserRepository> RepositoryMock { get; }
  public ILogger<UserService> Logger { get; }
  public UserService Service { get; }

  public UserServiceTestFixture()
  {
    RepositoryMock = new Mock<IUserRepository>();
    Logger = TestUtilities.CreateMockLogger<UserService>();
    Service = new UserService(RepositoryMock.Object, Logger);
  }

  public void Dispose()
  {
    // Cleanup if needed
  }
}

[Collection("UserService Collection")]
public class UserServiceTests : IClassFixture<UserServiceTestFixture>
{
  private readonly UserServiceTestFixture _fixture;

  public UserServiceTests(UserServiceTestFixture fixture)
  {
    _fixture = fixture;
  }

  [Fact]
  public async Task GetUserByIdAsync_WithValidId_ReturnsUser()
  {
    // Use _fixture.Service, _fixture.RepositoryMock, etc.
  }
}
```

## Angular Testing

**COMPONENT TEST**:
```typescript
describe('UserListComponent', () => {
  let component: UserListComponent;
  let fixture: ComponentFixture<UserListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserListComponent],
      providers: [
        { provide: UserService, useValue: mockUserService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(UserListComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load users on init', fakeAsync(() => {
    // Arrange
    const mockUsers = [{ id: 1, name: 'John' }];
    spyOn(inject(UserService), 'getUsers').and.returnValue(of(mockUsers));

    // Act
    fixture.detectChanges();
    tick();

    // Assert
    expect(component.users$).toBeDefined();
  }));
});
```

## Guidelines

**ALWAYS**:
- Write tests for critical business logic
- Test error paths (exceptions, validation failures)
- Mock external dependencies (HTTP, DB, services)
- Use descriptive test names
- Keep tests focused and isolated
- Use Arrange/Act/Assert pattern

**NEVER**:
- Test implementation details
- Create test interdependencies
- Use real databases in unit tests
- Create brittle tests (avoid `Thread.Sleep`)
- Mock everything (sometimes real objects are better)

---

**Last Updated**: 2026-04-09

